"""
osc module for Insta360 is based on [Open Spherical Camera API](https://developers.google.com/streetview/open-spherical-camera) specification.

Classes:
    Client: osc (open spherical camera) client to interact with the camera.
"""

import requests
import logging
import base64

from enum import Enum
from pydantic import BaseModel


class ListFileType(Enum):
    """
    Enum for listing file types.
    
    Attributes:
        IMAGE: Image files.
        VIDEO: Video files.
        ALL: All files.
    """

    IMAGE: str = 'image'
    VIDEO: str = 'video'
    ALL: str = 'all'


class Thumbnail(BaseModel):
    """
    Model for thumbnail of a file.
    
    Attributes:
        base64: Base64 encoded thumbnail.
        content: Decoded content of the thumbnail.
    """

    def __init__(self, **data):
        super().__init__(**data)
        self.base64: str | None = data.get('thumbnail', None)
        self.content: bytes | None = None

        if self.base64 == "":
            self.base64 = None

        if self.base64:
            thumbnail_bytes = self.base64.encode()
            self.content = base64.b64decode(thumbnail_bytes)


    class Config:
        extra = 'allow'


class Entry(BaseModel):
    """
    Model for file entries in list files response.
    
    Attributes:
        name: Name of the file.
        fileUrl: URL of the file.
        localFileUrl: Local URL of the file.
        size: Size of the file.
        width: Width of the file.
        height: Height of the file.
        dateTimeZone: Date time zone of the file.
        dateTime: Date time of the file.
        thumbnailSize: Thumbnail size of the file.
        isProcessed: Is the file processed.
        previewUrl: URL of the preview.
        thumbnail: Thumbnail object.
    """

    name: str
    fileUrl: str
    size: int
    width: int
    height: int
    dateTimeZone: str
    isProcessed: bool
    previewUrl: str

    def __init__(self, **data):
        super().__init__(**data)
        self.localFileUrl: str | None = data.get('_localFileUrl', None)
        self.dateTime: str | None = data.get('_dateTime', None)
        self.thumbnailSize: int | None = data.get('_thumbnailSize', None)
        self.thumbnail: Thumbnail = Thumbnail(**data)


    class Config:
        extra = 'allow'


class ListFilesResults(BaseModel):
    """
    Model for results of list files response.
    
    Attributes:
        entries: List of file entries.
        totalEntries: Total number of entries.
    """

    entries: list[Entry]
    totalEntries: int


class DeleteFilesResults(BaseModel):
    """
    Model for results of delete files response.
    
    Attributes:
        fileUrls: List of file URLs.
    """

    fileUrls: list[str]


class OSCResponse(BaseModel):
    """
    Model for list files response.
    
    Attributes:
        name: Name of the response.
        state: State of the response.
    """

    name: str
    state: str


class Error(BaseModel):
    """
    Model for osc error.
    
    Attributes:
        code: Error code.
        message: Error message.
    """

    code: str
    message: str


class ErrorResponse(BaseModel):
    """
    Model for osc error response.
    
    Attributes:
        error: osc error.
    """

    error: Error


class ListFilesResponse(OSCResponse):
    """
    Model for list files response.
    
    Attributes:
        results: List files results.
    """

    results: ListFilesResults


class DeleteFilesResponse(OSCResponse):
    """
    Model for delete files response.
    
    Attributes:
        results: Delete files results.
    """

    results: DeleteFilesResults


class Client:
    """ 
    Client for interacting with the camera using osc API specification.
        
    Parameters:
        host: IP address of the camera.
        timeout_sec: Timeout in seconds for requests.
        logger: Logger for logging messages.

    Methods:
        execute_command: Execute a command on the camera.
        list_files: List files on the camera.
        delete_files: Delete files on the camera.
        download_file: Download a file from the camera.
    """

    def __init__(self, host: str = '192.168.42.1', timeout_sec: float = 10.0, logger: logging.Logger | None = None) -> None:
        self.host = host
        self.timeout_sec = timeout_sec
        self.logger = logger if logger else logging.getLogger(__name__)

    def execute_command(self, body: dict) -> requests.Response:
        """
        Execute a command on the camera.
        
        Parameters:
            body: Command to execute as python dictionary.
        
        Returns:
            Deserialized JSON response from the camera.

        Note:
            This method is used internally by other methods to execute commands on the camera.
        """
        url = f'http://{self.host}/osc/commands/execute'
        return requests.post(url, json=body, timeout=self.timeout_sec)

    def list_files(self, file_type: ListFileType = ListFileType.ALL, start_position: int = 0, entry_count: int = 10, max_thumb_size: int | None = None) -> ListFilesResponse | ErrorResponse:
        """
        List files on the camera.

        Parameters:
            file_type: Type of files to list.
            start_position: Start position of the list.
            entry_count: Number of entries to list after start position.
            max_thumb_size: Maximum thumbnail size.
        
        Returns:
            List files response.

        Note:
            1. **`start_position`** will have no effect if the file type is **`ListFileType.ALL`**
            2. Less than 20 entries should be requested at a time to avoid large responses that camera may not be able to handle.

        Example:
            ```py
            from insta360.osc import Client

            client = Client()
            files = client.list_files(entry_count=2)
            print(files.model_dump())
            ```
        """

        body = {
            'name': 'camera.listFiles',
            'parameters': {
                'fileType': file_type.value,
                'entryCount': entry_count,
                'maxThumbSize': max_thumb_size,
                'startPosition': start_position
            }
        }

        response = self.execute_command(body)
        response_json = response.json()

        if response.status_code == 200:
            if 'error' in response_json:
                return ErrorResponse(**response_json)
            return ListFilesResponse(**response_json)
        
        return ErrorResponse(**response_json)


    def delete_files(self, file_urls: list[str]) -> DeleteFilesResponse | ErrorResponse:
        """
        Delete files on the camera.

        Parameters:
            file_urls: URLs of the files to delete.
        
        Returns:
            Delete files response.

        Tip:
            **`file_urls`** can be obtained from ListFilesResponse.
    
        Example:
            ```py
            from insta360.osc import Client

            client = Client()
            response = client.delete_files([
                "http://192.168.42.1:80/DCIM/Camera01/VID_20240413_051305_00_031.insv",
                "http://192.168.42.1:80/DCIM/Camera01/VID_20240413_051251_00_030.insv"
            ])
            print(response.model_dump())
            ```
        """

        body = {
            'name': 'camera.delete',
            'parameters': {
                'fileUrls': file_urls
            }
        }

        response = self.execute_command(body)
        response_json = response.json()

        if response.status_code == 200:
            if 'error' in response_json:
                return ErrorResponse(**response_json)
            return DeleteFilesResponse(**response_json)
        
        return ErrorResponse(**response_json)

    def download_file(self, file_url: str, save_path: str) -> bool:
        """
        Download a file from the camera.

        Parameters:
            file_url: URL of the file to download.
            save_path: Path to save the file.
        
        Returns:
            True if the download was successful, False otherwise.

        Tip:
            **`file_urls`** can be obtained from ListFilesResponse.

        Example:
            ```py
            from insta360.osc import Client

            client = Client()
            result = client.DownloadCameraFile(
                "http://192.168.42.1:80/DCIM/Camera01/LRV_20240411_074704_11_029.lrv",
                "C:/Users/username/Downloads/LRV_20240411_074704_11_029.lrv"
            )
            print(result)
            ```
        """

        response = requests.get(file_url, timeout=self.timeout_sec)
        
        if response.status_code == 200:
            with open(save_path, 'wb') as file:
                file.write(response.content)
            return True
        
        return False
