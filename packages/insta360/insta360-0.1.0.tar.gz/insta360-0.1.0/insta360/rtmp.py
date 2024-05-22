"""
rtmp module for insta360 allows real-time communication with the camera based on a TCP socket.

Classes:
    Client: Client for interacting with the camera using the rtmp protocol.
    CommandFailedException: Exception raised when a command fails.
    CameraNotConnectedException: Exception raised when the camera is not connected.
"""

import logging
import os
import select
import signal
import socket
import struct
import subprocess
import sys
import time
import threading
import typing as t

from google.protobuf import json_format
import requests

from .utils.utilities import (
    bytes_to_hex,
    bytes_to_hexascii,
    protobuf_to_dict
)

from .pb2 import capture_state_pb2
from .pb2 import current_capture_status_pb2
from .pb2 import error_pb2
from .pb2 import get_current_capture_status_pb2
from .pb2 import get_file_list_pb2
from .pb2 import get_options_pb2
from .pb2 import get_photography_options_pb2
from .pb2 import set_options_pb2
from .pb2 import set_photography_options_pb2
from .pb2 import start_capture_pb2
from .pb2 import start_live_stream_pb2
from .pb2 import stop_capture_pb2
from .pb2 import stop_live_stream_pb2
from .pb2 import storage_pb2
from .pb2 import storage_update_pb2
from .pb2 import take_picture_pb2


class CommandFailedException(Exception):
    pass


class CameraNotConnectedException(Exception):
    pass


CAMERA_WIFI_NOT_CONNECTED_ERROR_MESSAGE = 'This device is not connected to the camera wifi'


class Client:
    """
    Client for interacting with the camera using the rtmp protocol.

    Parameters:
        host: The IP address of the camera (usually always 192.168.42.1).
        port: The port of the camera (usually alwaays 6666).
        logger: A custom logger to use.
        callback: A callback function to call when a message is received.
        output_filepath: The output file path for saving the video stream.

    Methods:
        check_connected_to_camera_wifi: Check if the device is connected to the camera wifi.
        open: Open a TCP socket to the camera.
        close: Close the TCP socket.
        sync_local_time_to_camera: Sync the local time to the camera.
        get_camera_info: Get updated data about the camera, battery, storage, etc.
        get_camera_type: Get the camera type.
        take_picture: Take a picture.
        get_serial_number: Get the camera serial number.
        get_camera_files_list: Get the list of files on the camera.
        set_normal_video_options: Set the normal video options.
        get_normal_video_options: Get the normal video options.
        start_capture: Start capturing video.
        stop_capture: Stop capturing video.
        get_exposure_settings: Get the exposure settings.
        set_exposure_settings: Set the exposure settings.
        set_capture_settings: Set the capture settings.
        get_capture_settings: Get the capture settings.
        start_live_stream: Start the live stream.
        start_preview_stream: Start the preview stream.
        stop_live_stream: Stop the live stream.
        stop_preview_stream: Stop the preview stream.
        convert_livestream_raw_to_mp4: Convert the live stream raw file to mp4.
        get_camera_uuid: Get the camera UUID.
        get_capture_current_status: Get the current capture status.
        set_time_lapse_option: Set the time lapse option.
        start_time_lapse: Start the time lapse.
        stop_time_lapse: Stop the time lapse.
        is_camera_connected: Check if the camera is connected.
        get_battery_status: Get the battery status.
        get_storage_state: Get the storage state.

    Classes:
        KeepAliveTimer: Timer to call the KeepAlive function.
    """

    # Socket timing parameters.
    SOCKET_TIMEOUT_SEC = 5.0           # Default timeout for the socket
    PKT_COMPLETE_TIMEOUT_SEC = 4.0     # Timeout for receiving a complete data packet

    KEEPALIVE_INTERVAL_SEC = 2.0
    IS_CONNECTED_TIMEOUT_SEC = 10.0
    RECONNECT_TIMEOUT_SEC = 30.0

    PKT_SYNC = bytearray(b'\x06\x00\x00syNceNdinS')
    PKT_KEEPALIVE = bytearray(b'\x05\x00\x00')

    PHONE_COMMAND_BEGIN = 0
    PHONE_COMMAND_START_LIVE_STREAM = 1
    PHONE_COMMAND_STOP_LIVE_STREAM = 2
    PHONE_COMMAND_TAKE_PICTURE = 3
    PHONE_COMMAND_START_CAPTURE = 4
    PHONE_COMMAND_STOP_CAPTURE = 5
    PHONE_COMMAND_CANCEL_CAPTURE = 6
    PHONE_COMMAND_SET_OPTIONS = 7
    PHONE_COMMAND_GET_OPTIONS = 8
    PHONE_COMMAND_SET_PHOTOGRAPHY_OPTIONS = 9
    PHONE_COMMAND_GET_PHOTOGRAPHY_OPTIONS = 10
    PHONE_COMMAND_GET_FILE_EXTRA = 11
    PHONE_COMMAND_DELETE_FILES = 12
    PHONE_COMMAND_GET_FILE_LIST = 13
    PHONE_COMMAND_GET_CURRENT_CAPTURE_STATUS = 15

    RESPONSE_CODE_OK = 200
    RESPONSE_CODE_ERROR = 500

    CAMERA_NOTIFICATION_BATTERY_LOW = 8196
    CAMERA_NOTIFICATION_STORAGE_UPDATE = 8198
    CAMERA_NOTIFICATION_STORAGE_FULL = 8199
    CAMERA_NOTIFICATION_CAPTURE_STOPPED = 8201
    CAMERA_NOTIFICATION_CURRENT_CAPTURE_STATUS = 8208

    # For each message code there is a specific protobuf message class.
    pb_msg_class = {
        PHONE_COMMAND_SET_OPTIONS: set_options_pb2.SetOptions(),
        PHONE_COMMAND_GET_OPTIONS: get_options_pb2.GetOptions(),
        PHONE_COMMAND_TAKE_PICTURE: take_picture_pb2.TakePicture(),
        PHONE_COMMAND_GET_FILE_LIST: get_file_list_pb2.GetFileList(),
        PHONE_COMMAND_SET_PHOTOGRAPHY_OPTIONS: set_photography_options_pb2.SetPhotographyOptions(),
        PHONE_COMMAND_GET_PHOTOGRAPHY_OPTIONS: get_photography_options_pb2.GetPhotographyOptions(),
        PHONE_COMMAND_START_CAPTURE: start_capture_pb2.StartCapture(),
        PHONE_COMMAND_STOP_CAPTURE: stop_capture_pb2.StopCapture(),
        PHONE_COMMAND_START_LIVE_STREAM: start_live_stream_pb2.StartLiveStream(),
        PHONE_COMMAND_STOP_LIVE_STREAM: stop_live_stream_pb2.StopLiveStream(),
        PHONE_COMMAND_GET_CURRENT_CAPTURE_STATUS: get_current_capture_status_pb2.CameraCaptureStatus()
    }

    def __init__(
        self,
        host: str = '192.168.42.1',
        port: int = 6666,
        logger: t.Optional[logging.Logger] = None,
        callback: t.Optional[t.Callable[[t.Dict], t.Any]] = None,
        output_filepath: t.Optional[str] = None
    ):
        if logger is None:
            self.logger = logging.getLogger(None)
        else:
            self.logger = logger

        self.connect_host = host
        self.check_connected_to_camera_wifi()
        self.connect_port = port

        self.callback_handler = callback
        self.camera_socket = None
        self.timer_keepalive = None
        self.message_seq = 0
        self.sent_messages_codes = {}
        self.rcv_thread = None
        self.rcv_buffer = b''
        self.socket_lock = None
        self.is_connected = False
        self.reconnect_time = time.time()
        self.last_pkt_sent_time = time.time()
        self.last_pkt_recv_time = time.time()
        self.program_killed = False
        signal.signal(signal.SIGTERM, self._signal_handler)
        signal.signal(signal.SIGINT, self._signal_handler)
        # Enable async receiving function.
        self.rcv_thread = threading.Thread(target=self._receive_packet, daemon=True)
        self.rcv_thread.start()

        if output_filepath:
            self.raw_file_path = 'output/dump.raw'
            self.dump_fp = open(self.raw_file_path, 'wb')
            self.output_filepath = output_filepath
        else:
            self.raw_file_path = None
            self.dump_fp = None
            self.output_filepath = None
        
        self.live_stream_started = False
        self.capture_started = False

    def check_connected_to_camera_wifi(self):
        """
        Check if the device is connected to the camera wifi.
        """

        camera_info_url = f'http://{self.connect_host}/osc/info'
        try:
            r = requests.get(camera_info_url, timeout=20)
            if r.status_code != 200:
                self.logger.error(CAMERA_WIFI_NOT_CONNECTED_ERROR_MESSAGE)
                raise CameraNotConnectedException(CAMERA_WIFI_NOT_CONNECTED_ERROR_MESSAGE)
        except requests.ConnectionError:
            self.logger.error(CAMERA_WIFI_NOT_CONNECTED_ERROR_MESSAGE)
            raise CameraNotConnectedException(CAMERA_WIFI_NOT_CONNECTED_ERROR_MESSAGE)

    def _signal_handler(self, signum: int, _frame):
        """
        Handle Stop Signals.

        Parameters:
            signum: The signal number.

        Note:
            This is an internal method and should not be called directly.
        """

        self.logger.info('Received signal %d, exiting' % (signum,))

        if self.live_stream_started:
            self.logger.info('Stopping live stream')
            self.stop_live_stream()
            self.live_stream_started = False
            self.logger.info('Live stream stopped')

        if self.capture_started:
            self.logger.info('Stopping capture')
            self.stop_capture()
            self.capture_started = False
            self.logger.info('Capture stopped')

        self.program_killed = True
        self.close()
        sys.stderr = open(os.devnull, "w")
        sys.exit(signum)

    def open(self):
        """
        Opens a TCP socket to the camera.
        """

        self.close()
        self.reconnect_time = time.time()
        self.logger.info('Connecting socket to host %s:%d' % (self.connect_host, self.connect_port))
        try:
            self.camera_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.camera_socket.settimeout(self.SOCKET_TIMEOUT_SEC)
            self.camera_socket.connect((self.connect_host, self.connect_port))
            self.logger.debug('Socket opened')
        except Exception as ex:
            self.logger.error('Exception in socket.connect(): %s' % (ex,))
            self.camera_socket = None
        if not self.program_killed:
            # Mutex lock for socket send/receive.
            self.socket_lock = threading.Lock()
            # Send the first packets.
            self._send_packet(self.PKT_SYNC)
            self._send_packet(self.PKT_KEEPALIVE)
            seq = self.sync_local_time_to_camera()
            # Enable async timers.
            self.timer_keepalive = self.KeepAliveTimer(self.KEEPALIVE_INTERVAL_SEC, self._keep_alive)
            self.timer_keepalive.start()
            self._check_if_command_successful(seq)

    def _check_if_command_successful(self, seq: int, wait_for_seconds: int = 20):
        """
        Check if a command was successful.

        Parameters:
            seq: The sequence number of the command.
            wait_for_seconds: The number of seconds to wait for the command to succeed.

        Note:
            This is an internal method and should not be called directly.
        """

        sleep_time = 0.1
        loop_range = int(wait_for_seconds / sleep_time)
        for _ in range(loop_range):
            if seq not in self.sent_messages_codes:
                self.logger.debug('Command seq %s succeeded' % seq)
                return
            time.sleep(sleep_time)
        raise CommandFailedException(f'Command seq {seq} did not succeed in {wait_for_seconds} seconds')

    def close(self):
        """
        Stops the keep alive timer and closes the TCP socket.
        """
        self.logger.debug('Stopping keepalive timer and closing socket')
        if self.timer_keepalive is not None:
            self.timer_keepalive.cancel()
            self.timer_keepalive = None
        if self.camera_socket is not None:
            self.camera_socket.shutdown(socket.SHUT_RDWR)
            self.camera_socket.close()
            self.camera_socket = None
        self.is_connected = False
        self.message_seq = 0
        self.sent_messages_codes = {}

    class KeepAliveTimer(threading.Timer):
        """
        Timer to call the KeepAlive function.
        """

        def run(self):
            while not self.finished.wait(self.interval):
                self.function(*self.args, **self.kwargs)

    def _send_message(self, message: t.Dict[t.Any, t.Any], message_code: int) -> int:
        """
        Converts a dictionary into the corresponding protobuf message and sends it.

        Parameters:
            message: The payload to parse and send to the camera.
            message_code: The message code to find the protobuf message class.

        Returns:
            The sequence number of the sent message.

        Note:
            This is an internal method and should not be called directly.
        """
        with self.socket_lock:
            seq_number = self.message_seq
            self.message_seq += 1
        protobuf_msg = self.pb_msg_class[message_code]
        proto_module = protobuf_msg.__class__.__module__
        proto_name = protobuf_msg.__class__.__name__
        self.logger.info('Sending message #%d: "%s.%s()"' % (seq_number, proto_module, proto_name))
        self.sent_messages_codes[seq_number] = message_code
        try:
            json_format.ParseDict(message, protobuf_msg)
            header = b'\x04\x00\x00'
            header += message_code.to_bytes(2, 'little')
            header += b'\x02'
            header += struct.pack('<i', seq_number)[0:3]
            header += b'\x80\x00\x00'
            packet = header + protobuf_msg.SerializeToString()
            self._send_packet(packet)
        except Exception as ex:
            self.logger.error('Exception in SendMessage(): %s' % (ex,))
            del self.sent_messages_codes[seq_number]
        return seq_number

    def _keep_alive(self):
        """
        Keeps the TCP socket alive to send packets regularly.

        Note:
            This is an internal method and should not be called directly.
        """

        if self.is_connected:
            if (time.time() - self.last_pkt_recv_time) > self.IS_CONNECTED_TIMEOUT_SEC:
                self.logger.info('Timeout expecting packet: assuming disconnected')
                self.is_connected = False
            elif (time.time() - self.last_pkt_sent_time) > self.KEEPALIVE_INTERVAL_SEC:
                self.logger.debug('Sending KeepAlive')
                self._send_packet(self.PKT_KEEPALIVE)
                self.last_pkt_sent_time = time.time()
        else:
            # Try a new connection.
            if time.time() - self.reconnect_time > self.RECONNECT_TIMEOUT_SEC:
                self.logger.info('KeepAlive: Not connected: trying re-connect')
                self.open()

    def _parse_protobuf_message(self, message_class: t.Any, message_bytes: bytes) -> t.Any:
        """
        Parses a protobuf message using the given class.

        Parameters:
            message_class: The protobuf message response class.
            message_bytes: The protobuf message bytes received.

        Returns:
            The protobuf message parsed using the protobuf class.

        Note:
            This is an internal method and should not be called directly.
        """

        proto_module = message_class.__class__.__module__
        proto_name = message_class.__class__.__name__
        try:
            message = message_class
            message.ParseFromString(message_bytes)
            self.logger.info('Parsed protobuf message "%s.%s()":\n%s' % (proto_module, proto_name, message))
        except Exception as ex:
            self.logger.error('Cannot parse message as "%s.%s()": %s' % (proto_module, proto_name, ex))
            message = None
        return message

    def _send_packet(self, pkt_payload):
        """
        Sends pkt_data (bytearray) to the socket, prepending the overall length.
        
        Parameters:
            pkt_payload: The payload to send to the camera.

        Note:
            This is an internal method and should not be called directly.
        """

        if self.camera_socket is not None:
            pkt_data = bytearray(struct.pack('<i', len(pkt_payload) + 4))
            pkt_data.extend(pkt_payload)
            self.logger.info(
                "Sending packet: b'%s%s'" % (bytes_to_hex(pkt_payload[:12]), bytes_to_hexascii(pkt_payload[12:]))
            )
            self._socket_send(pkt_data)
            time.sleep(0.1)     # Actually 0.02 should suffice.

    def _socket_send(self, pkt_data):
        """
        Sends the bytearray pkt_data to socket.

        Parameters:
            pkt_data: The data to send to the socket.

        Returns:
            True on success or False on error.

        Note:
            This is an internal method and should not be called directly.
        """

        try:
            with self.socket_lock:
                self.camera_socket.sendall(pkt_data)
        except Exception as ex:
            self.logger.error('Exception in socket.sendall(): %s' % (ex,))
            return False
        return True

    def _receive_packet(self):
        """
        Receives data from socket and assemble full packets.

        Note:
            This is an internal method and should not be called directly.
        """

        # Wait for the main thread to eventually open the socket.
        time.sleep(0.12)
        # Start an infinite loop to receive packets.
        while True:
            self.logger.debug('Loop receive_packet() thread')
            if self.camera_socket is None:
                time.sleep(1.0)
                continue
            pkt_len = None
            pkt_data = b''
            t0 = time.time()
            poller = select.poll()
            poller.register(self.camera_socket, select.POLLIN)
            # Loop waiting a packet to be complete.
            while True:
                self.logger.debug("Receiving buffer: ")
                if pkt_len is None and len(self.rcv_buffer) >= 4:
                    pkt_len = int.from_bytes(self.rcv_buffer[0:4], byteorder='little')
                    self.logger.debug('Received begin of packet, length = %d' % (pkt_len,))
                if pkt_len is not None and len(self.rcv_buffer) >= pkt_len:
                    self.logger.debug('Packet is complete, len(rcv_buffer): %s' % (len(self.rcv_buffer,)))
                    pkt_data = self.rcv_buffer[4:pkt_len]
                    self.rcv_buffer = self.rcv_buffer[pkt_len:]
                    break
                # Packet is not complete wait data from the socket.
                try:
                    self.logger.debug('Polling socket for data')
                    evts = poller.poll(int(self.PKT_COMPLETE_TIMEOUT_SEC * 1000))
                    for sock, evt in evts:
                        if evt and select.POLLIN:
                            if self.camera_socket is not None and sock == self.camera_socket.fileno():
                                self.rcv_buffer += self.camera_socket.recv(4096)
                except Exception as ex:
                    self.logger.error('Exception in receive_packet(): %s' % (ex,))
                if time.time() - t0 > self.PKT_COMPLETE_TIMEOUT_SEC:
                    self.logger.warning(
                        "Timeout in receive_packet(). Discarding buffer: b'%s'" % (bytes_to_hexascii(self.rcv_buffer),)
                    )
                    break
            # The packet is complete or receiving complete packet timeout.
            self._parse_packet(pkt_data)

    def _parse_packet(self, pkt_data):
        """
        Parses a received packet.

        Parameters:
            pkt_data: The packet data to parse.  

        Note:
            This is an internal method and should not be called directly. 
        """

        if len(pkt_data) == 0:
            return
        self.last_pkt_recv_time = time.time()
        if pkt_data == self.PKT_SYNC:
            self.is_connected = True
            return
        if pkt_data == self.PKT_KEEPALIVE:
            return
        if len(pkt_data) < 12:
            return

        header = pkt_data[:12]
        body = pkt_data[12:]
        self.logger.info("Received packet: b'%s%s'" % (bytes_to_hex(header), bytes_to_hexascii(body)))
        # Responses to messages (header is [:10], protobuf is at [12:])
        # b'\x04\x00\x00\xc8\x00\x02\x1d\x00\x00\x80\x00\x00'  # GetOptionsResp 'LOCAL_TIME', 'TIME_ZONE'
        # b'\x04\x00\x00\xc8\x00\x02\x1e\x00\x00\x80\x3f\x00'
        #               GetOptionsResp BATTERY_STATUS, STORAGE_STATE, CAMERA_TYPE, FIRMWAREREVISION
        # b'\x04\x00\x00\xc8\x00\x02\x1f\x00\x00\x80\x00\x00'  # GetFileList
        # Response seq = 3 with error message:
        # b'\x04\x00\x00\xf4\x01\x02\x03\x00\x00\x80\x00\x00\x12\x0fcamera is busy.'
        # Response seq = 5 with error message:
        # b'\x04\x00\x00\xf4\x01\x02\x05\x00\x00\x80\x00\x0b\x12\x10msg execute err.'
        # Message out of sequence number: code = \x10\x20 = 8208 = CAMERA_NOTIFICATION_CURRENT_CAPTURE_STATUS
        # b'\x04\x00\x00\x10\x20\x02\xff\x8a\x43\xf4\x00\x00\x08\x01\x10\x00\x1a\x00'

        body = pkt_data[12:]
        response_type = pkt_data[0:3]  # b'\x04\x00\x00'
        # Response code:
        #  b'\xc8\x00' = 200  = OK
        #  b'\xf4\x01' = 500  = ERROR
        #  b'\x10\x20' = 8208 = CAMERA_NOTIFICATION_CURRENT_CAPTURE_STATUS
        response_code = struct.unpack('<H', pkt_data[3:5])[0]
        _ = pkt_data[5:6]     # unknown_1: b'\x02'
        # Sequence number: 24 bit unsigned int, the same of the request packet.
        response_seq = struct.unpack('<I', pkt_data[6:9] + b'\x00')[0]
        _ = pkt_data[9:10]    # unknown_2: b'\x80'
        _ = pkt_data[10:11]   # unknown_3: 3f, bf, 63, 00, 40, 41, 76, 58, 31
        _ = pkt_data[11:12]   # unknown_4 00, ee, ff, 85, 6b, d8, d0, f4, 5c, 0b, 34

        self.logger.info(
            "Received message: type: b'%s', code: %d, seq: %d" %
            (bytes_to_hex(response_type), response_code, response_seq)
        )

        if response_type == b'\x01\x00\x00' and self.dump_fp is not None :
            self.dump_fp.write(body)

        if response_code == self.RESPONSE_CODE_ERROR:
            message = self._parse_protobuf_message(error_pb2.Error(), body)
            if message is not None:
                err_message = message.message
                err_code = error_pb2.Error.ErrorCode.Name(message.code)
                self.logger.error('Message #%d raised %s "%s"' % (response_seq, err_code, err_message))
            if response_seq in self.sent_messages_codes:
                del self.sent_messages_codes[response_seq]
            return

        # TODO: Handle the CAMERA_NOTIFICATION_CAPTURE_STOPPED response code (SD full, etc.)

        if response_code == self.CAMERA_NOTIFICATION_CURRENT_CAPTURE_STATUS:
            message = self._parse_protobuf_message(current_capture_status_pb2.CaptureStatus(), body)
            if message is not None:
                msg_state = capture_state_pb2.CameraCaptureState.Name(message.state)
                msg_time = message.capture_time
                self.logger.info('Capture state notification: %s, time: %d' % (msg_state, msg_time))
                if self.callback_handler is not None:
                    self.callback_handler(protobuf_to_dict(message, response_code=response_code))
            return

        if response_code == self.CAMERA_NOTIFICATION_STORAGE_UPDATE:
            message = self._parse_protobuf_message(storage_update_pb2.NotificationCardUpdate(), body)
            if message is not None:
                msg_state = storage_pb2.CardState.Name(message.state)
                msg_location = storage_pb2.CardLocation.Name(message.location)
                self.logger.info('Storage update notification: %s, location: %s' % (msg_state, msg_location))
                if self.callback_handler is not None:
                    self.callback_handler(protobuf_to_dict(message, response_code=response_code))
            return

        # If response sequence is not into the sent list, do not parse the response.
        if response_seq not in self.sent_messages_codes:
            return

        # Parse the protobuf message using the proper message type.
        sent_msg_code = self.sent_messages_codes[response_seq]
        sent_msg_class = self.pb_msg_class[sent_msg_code]
        proto_module = sent_msg_class.__class__.__module__
        proto_name = sent_msg_class.__class__.__name__
        self.logger.info('Received response #%d to message "%s.%s()"' % (response_seq, proto_module, proto_name))

        message = None
        if sent_msg_code == self.PHONE_COMMAND_GET_OPTIONS:
            message = self._parse_protobuf_message(get_options_pb2.GetOptionsResp(), body)
            # TODO: Save some options into self object properties.
        elif sent_msg_code == self.PHONE_COMMAND_SET_OPTIONS:
            message = self._parse_protobuf_message(set_options_pb2.SetOptionsResp(), body)
        elif sent_msg_code == self.PHONE_COMMAND_GET_FILE_LIST:
            message = self._parse_protobuf_message(get_file_list_pb2.GetFileListResp(), body)
        elif sent_msg_code == self.PHONE_COMMAND_STOP_CAPTURE:
            message = self._parse_protobuf_message(stop_capture_pb2.StopCaptureResp(), body)
        elif sent_msg_code == self.PHONE_COMMAND_TAKE_PICTURE:
            message = self._parse_protobuf_message(take_picture_pb2.TakePictureResponse(), body)
        elif sent_msg_code == self.PHONE_COMMAND_GET_PHOTOGRAPHY_OPTIONS:
            message = self._parse_protobuf_message(get_photography_options_pb2.GetPhotographyOptionsResp(), body)
        elif sent_msg_code == self.PHONE_COMMAND_GET_CURRENT_CAPTURE_STATUS:
            message = self._parse_protobuf_message(get_current_capture_status_pb2.GetCurrentCaptureStatusResp(), body)

        # Remove the sequence number from the dictionary of sent messages.
        del self.sent_messages_codes[response_seq]

        # Execute the callback function to notify the received message.
        if message is not None and self.callback_handler is not None:
            self.callback_handler(
                protobuf_to_dict(
                    message,
                    response_code=self.RESPONSE_CODE_OK,
                    message_code=sent_msg_code
                )
            )

    def sync_local_time_to_camera(
        self,
        timestamp: t.Optional[int] = None,
        seconds_from_gmt: t.Optional[int] = None
    ) -> int:
        """
        Sync the local time and timezone to the camera.

        Parameters:
            timestamp: The epoch timestamp to set.
            seconds_from_gmt: The timezone offset from GMT in seconds.

        Returns:
            The sequence number of the sent message.
        """

        if timestamp is None:
            timestamp = int(time.time())
        if seconds_from_gmt is None:
            seconds_from_gmt = 0
        message = {
            'optionTypes': [
                'LOCAL_TIME',
                'TIME_ZONE'
            ],
            'value': {
                'local_time': timestamp,
                'time_zone_seconds_from_GMT': seconds_from_gmt
            }
        }
        return self._send_message(message, self.PHONE_COMMAND_SET_OPTIONS)

    def get_camera_info(self) -> int:
        """
        Get updated data about the camera, battery, storage, etc.

        Returns:
            The sequence number of the sent message.
        """

        # Data retrieved with this function maybe used also by
        # GetBatteryStatus, GetSerialNumber, GetCameraUUID,
        # GetStorageState and GetCameraType.
        #
        # WARNING: The value returned by asking for option_types: VIDEO_RESOLUTION,
        # e.g. value: { video_resolution: RES_3840_2160P60 }, does not match the one
        # selected on the camera. Ask for GetPhotographyOptions() instead.
        #
        # Options actually returned by the Insta360 ONE RS:
        # [x] BATTERY_STATUS
        # [x] SERIAL_NUMBER
        # [x] UUID
        # [x] STORAGE_STATE
        # [x] FIRMWAREREVISION
        # [x] CAMERA_TYPE
        # [ ] LED_SWITCH
        # [x] VIDEO_FOV
        # [x] STILL_FOV
        # [x] TEMP_VALUE
        # [x] VIDEO_RESOLUTION (not the actual resolution selected)
        # [ ] CAPTURE_TIME_LIMIT
        # [ ] REMAINING_PICTURES
        # [x] BUTTON_PRESS_OPTIONS
        # [ ] GAMMA_MODE
        # [ ] MCTF_ENABLE
        # [ ] AUTHORIZATION_ID
        # [ ] STANDBY_DURATION
        # [ ] QUICK_CAPTURE_ENABLE
        # [ ] TELEVISION_SYSTEM
        # [ ] PTZ_CTRL
        # [ ] CAMERA_POSTURE
        # [ ] OFFSET_STATES
        # [ ] OPTIONS_NUM
        message = {
            'optionTypes': [
                'BATTERY_STATUS',
                'SERIAL_NUMBER',
                'UUID',
                'STORAGE_STATE',
                'FIRMWAREREVISION',
                'CAMERA_TYPE',
                'TEMP_VALUE',
                'CAMERA_POSTURE',
                'OPTIONS_NUM'
            ]
        }
        return self._send_message(message, self.PHONE_COMMAND_GET_OPTIONS)

    def get_camera_type(self):
        """
        Get the camera type.
        """

        raise NotImplementedError()

    def take_picture(self) -> int:
        """
        Take a picture.

        Returns:
            The sequence number of the sent message.
        """
        message = {'mode': 'NORMAL'}
        return self._send_message(message, self.PHONE_COMMAND_TAKE_PICTURE)

    def get_serial_number(self):
        """
        Get the camera serial number.
        """
        raise NotImplementedError()

    def get_camera_files_list(self) -> int:
        """
        Get the list of files on the camera.

        Returns:
            The sequence number of the sent message.
        """
        message = {
            'media_type': 'VIDEO_AND_PHOTO',
            'limit': 500
        }
        return self._send_message(message, self.PHONE_COMMAND_GET_FILE_LIST)

    def set_normal_video_options(
        self,
        record_resolution: t.Optional[str] = None,
        fov_type: t.Optional[str] = None,
        focal_length_value: t.Optional[float] = None,
        gamma_mode: t.Optional[str] = None,
        white_balance: t.Optional[str] = None,
        white_balance_value: t.Optional[float] = None,
        function_mode: str = 'FUNCTION_MODE_NORMAL_VIDEO'
    ) -> int:
        """
        Set the normal video options.

        Parameters:
            record_resolution: The recording resolution to set in the camera.
            fov_type: The FOV type to set in the camera.
            focal_length_value: The focal length value to set in the camera.
            gamma_mode: The gamma mode to set in the camera.
            white_balance: The white balance mode to set in the camera.
            white_balance_value: The white balance value to set in the camera.
            function_mode: The function mode to set in the camera.

        Returns:
            The sequence number of the sent message.
        """

        # Labels on camera display are not updated.
        # Request message example:
        # message = {
        #     'optionTypes': [
        #         'EXPOSURE_BIAS',
        #         'WHITE_BALANCE_VALUE',
        #         'VIDEO_GAMMA_MODE',
        #         'VIDEO_EXPOSURE_OPTIONS',
        #         'VIDEO_ISO_TOP_LIMIT',
        #         'RECORD_RESOLUTION',
        #         'FOV_TYPE',
        #         'FOCAL_LENGTH_VALUE'],
        #     'value': {
        #         'gamma_mode': 'VIVID',
        #         'video_exposure': {
        #             'iso': 400,
        #             'shutter_speed': 0.03333333333333333 },
        #         'record_resolution': 'RES_1920_1080P30',
        #         'fov_type': 'FOV_ULTRAWIDE',
        #         'focal_length_value': 17.4 },
        #     'function_mode': 'FUNCTION_MODE_NORMAL_VIDEO'
        # }

        message = {'optionTypes': [], 'value': {}, 'function_mode': function_mode}
        if record_resolution is not None:
            message['optionTypes'].append('RECORD_RESOLUTION')
            message['value']['record_resolution'] = record_resolution
        if fov_type is not None:
            message['optionTypes'].append('FOV_TYPE')
            message['value']['fov_type'] = fov_type
        if focal_length_value is not None:
            message['optionTypes'].append('FOCAL_LENGTH_VALUE')
            message['value']['focal_length_value'] = focal_length_value
        if gamma_mode is not None:
            message['optionTypes'].append('VIDEO_GAMMA_MODE')
            message['value']['gamma_mode'] = gamma_mode
        if white_balance is not None:
            message['optionTypes'].append('WHITE_BALANCE')
            message['value']['white_balance'] = white_balance
        if white_balance_value is not None:
            message['optionTypes'].append('WHITE_BALANCE_VALUE')
            message['value']['white_balance_value'] = white_balance_value
        self.logger.info('Sending message: %s' % (message,))
        return self._send_message(message, self.PHONE_COMMAND_SET_PHOTOGRAPHY_OPTIONS)

    def get_normal_video_options(self) -> int:
        """
        Get the normal video options.

        Returns:
            The sequence number of the sent message.
        """

        # WARNING: Sometimes, when the camera display is off (power saving),
        # changes to the FOCAL_LENGTH_VALUE will not result in the subsequent
        # PHONE_COMMAND_GET_PHOTOGRAPHY_OPTIONS requests. Sometimes FOV_WIDE
        # is not returned at all. The same happens when asking for VIDEO_FOV
        # using PHONE_COMMAND_GET_OPTIONS.
        # It seems that closing and re-opening the socket connection will
        # restore the correct reported value.
        message = {
            'option_types': [
                'EXPOSURE_BIAS',
                'WHITE_BALANCE',
                'WHITE_BALANCE_VALUE',
                'VIDEO_GAMMA_MODE',
                'VIDEO_EXPOSURE_OPTIONS',
                'VIDEO_ISO_TOP_LIMIT',
                'RECORD_RESOLUTION',
                'FOV_TYPE',
                'FOCAL_LENGTH_VALUE'],
            'function_mode': 'FUNCTION_MODE_NORMAL_VIDEO'
        }
        return self._send_message(message, self.PHONE_COMMAND_GET_PHOTOGRAPHY_OPTIONS)

    def start_capture(self) -> int:
        """
        Start capturing video.
        
        Returns:
            The sequence number of the sent message.
        """

        message = {
            'mode': 'Capture_MODE_NORMAL'
        }
        self.capture_started = True
        return self._send_message(message, self.PHONE_COMMAND_START_CAPTURE)

    def stop_capture(self) -> int:
        """
        Stop capturing video.

        Returns:
            The sequence number of the sent message.
        """

        message = {}
        return self._send_message(message, self.PHONE_COMMAND_STOP_CAPTURE)

    def get_exposure_settings(self):
        """
        Get exposure settings from the camera.
        """

        raise NotImplementedError()

    def set_exposure_settings(self):
        """
        Set exposure settings to the camera.
        """

        raise NotImplementedError()

    def set_capture_settings(self, record_resolution=None, fov_type=None, focal_length_value=None, gamma_mode=None):
        """
        Set capture settings to the camera.
        """

        raise NotImplementedError()

    def get_capture_settings(self):
        """
        Get capture settings from the camera.
        """

        raise NotImplementedError()

    def start_live_stream(self) -> int:
        """
        Start a high resolution live stream.
        
        Parameters:
            None

        Returns:
            The Sequence number of the sent message

        Note:
            You can start recording simultaneously but the live stream will glitch.

        Example:
            ```py
            from insta360.rtmp import Client

            client = Client()
            client.open()

            client.start_live_stream()
            ```
        """

        seq = self.set_normal_video_options(
            record_resolution='RES_2560_1280P30',
            function_mode='FUNCTION_MODE_LIVE_STREAM'
        )

        try:
            self._check_if_command_successful(seq)
        except CommandFailedException:
            self.logger.warning('Set Video Options command failed')

        message = {
            'enableVideo': True,
            'videoBitrate': 40,
            'resolution': 'RES_2560_1280P30',
            'enableGyro': True,
            'videoBitrate1': 40,
            'resolution1': 'RES_480_240P30',
            'isForLive': True
        }
        seq = self._send_message(message, self.PHONE_COMMAND_START_LIVE_STREAM)
        self._check_if_command_successful(seq)
        self.live_stream_started = True
        return seq
    
    def start_preview_stream(self) -> int:
        """
        Starts a low resolution preview stream.
        
        Returns:
            The Sequence number of the sent message
        
        Note:
            1. The stream is low resolution.
            2. You can start recording simultaneously without any glitches.

        Example:
            ```py
            from insta360.rtmp import Client

            client = Client()
            client.open()

            client.start_preview_stream()

            # Optionally, start recording
            client.start_capture()
            ```
        """

        message = {
            'enableVideo': True,
            'audioSampleRate': 48000,     
            'enableGyro': True,
            'resolution': 'RES_1440_720P30',
            'resolution1': 'RES_424_240P15',
        }

        seq = self._send_message(message, self.PHONE_COMMAND_START_LIVE_STREAM)
        self._check_if_command_successful(seq)
        self.live_stream_started = True
        
        return seq
    
    def stop_preview_stream(self) -> int:
        """
        Stops the preview stream.
        
        Returns:
            The Sequence number of the sent message

        Note:
            Internally, command for stopping preview stream is same as stopping live stream. Hence, this function is a wrapper around `stop_live_stream()` function.
            
        Example:
            ```py
            import time
            from insta360.rtmp import Client

            client = Client()
            client.open()

            client.start_preview_stream()
            time.sleep(10)

            client.stop_preview_stream()
            ```
        """

        return self.stop_live_stream()

    def stop_live_stream(self) -> int:
        """
        Stop the live stream.

        Returns:
            The Sequence number of the sent message
        """

        message = {}
        seq = self._send_message(message, self.PHONE_COMMAND_STOP_LIVE_STREAM)
        try:
            self._check_if_command_successful(seq)
        except CommandFailedException:
            self.logger.error('Failed to stop live stream')

        if self.dump_fp and self.output_filepath:
            self.convert_livestream_raw_to_mp4()

        return seq

    def convert_livestream_raw_to_mp4(self):
        """
        Convert the raw video stream file to mp4 format.
        """

        if self.output_filepath:
            subprocess.run(
                [
                    'ffmpeg',
                    '-i', self.raw_file_path,
                    '-vf', 'v360=dfisheye:e:ih_fov=193:iv_fov=193',
                    '-y',
                    self.output_filepath
                ],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.STDOUT
            )

    def get_camera_uuid(self):
        """
        Get the camera UUID.
        """

        raise NotImplementedError()

    def get_capture_current_status(self) -> int:
        """
        Get the current capture status from the camera.

        Returns:
            The sequence number of the sent message
        """

        message = {}
        return self._send_message(message, self.PHONE_COMMAND_GET_CURRENT_CAPTURE_STATUS)

    def set_time_lapse_option(self):
        """
        Set time-lapse options in the camera.
        """

        raise NotImplementedError()

    def start_time_lapse(self):
        """
        Start time-lapse in the camera.
        """

        raise NotImplementedError()

    def stop_time_lapse(self):
        """
        Stop time-lapse in the camera.
        """

        raise NotImplementedError()

    def is_camera_connected(self):
        """
        Check if the camera is connected.
        """

        raise NotImplementedError()

    def get_battery_status(self):
        """
        Get the battery status from the camera.
        """

        raise NotImplementedError()

    def get_storage_state(self):
        """
        Get the storage state from the camera.
        """

        raise NotImplementedError()
