import logging
import math
import os
from multiprocessing import Process
from typing import Any, Callable, Dict, Optional, Tuple
from urllib.parse import urljoin

import socketio
import ujson
from engineio.payload import Payload
from flask import Flask

from era_5g_interface.channels import COMMAND_ERROR_EVENT, CONTROL_NAMESPACE, DATA_NAMESPACE, CallbackInfoServer
from era_5g_interface.dataclasses.control_command import ControlCommand
from era_5g_interface.interface_helpers import MIDDLEWARE_ADDRESS
from era_5g_interface.server_channels import ServerChannels

logger = logging.getLogger(__name__)

# Middleware Network Application ID (task ID, NETAPP_ID).
MIDDLEWARE_TASK_ID = str(
    os.getenv("MIDDLEWARE_TASK_ID", os.getenv("NETAPP_ID", "00000000-0000-0000-0000-000000000000"))
)
# NETAPP_ID used for compatibility.
NETAPP_ID = MIDDLEWARE_TASK_ID
NETAPP_ID_ROS = NETAPP_ID.replace("-", "_")

NETAPP_NAME = str(os.getenv("NETAPP_NAME", "Unknown"))

# Used for Network Application heartbeat.
MAX_LATENCY = float(os.getenv("NETAPP_MAX_LATENCY", 100))

if MIDDLEWARE_ADDRESS.endswith("/status/netapp"):
    NETAPP_STATUS_ADDRESS = MIDDLEWARE_ADDRESS
else:
    NETAPP_STATUS_ADDRESS = urljoin(MIDDLEWARE_ADDRESS, "status/netapp")


def generate_application_heartbeat_data(
    avg_latency: float,
    queue_size: int,
    queue_occupancy: float,
    current_robot_count: int,
) -> Dict:
    """Generate application heartbeat JSON data.

    Args:
        avg_latency (float): Average latency.
        queue_size (int): Queue size.
        queue_occupancy (float): Queue occupancy.
        current_robot_count (int): Current robot count.
    """

    # Latency can change over time, so reporting just the simple que occupancy can be misleading.
    # Instead, it is better to report occupancy in terms of:
    #  'total time estimated to be needed to process everything in the queue' / 'required max latency'
    processing_time_occupancy = queue_size * avg_latency / MAX_LATENCY

    if queue_size == 0:
        # If the queue is empty then no estimate can be made about robot count limit,
        # but most likely at least one more robot can be added.
        hard_robot_count_limit = current_robot_count + 1
        optimal_robot_count_limit = current_robot_count + 1
    elif avg_latency == 0:
        # If there are no latency measurements, the maximum number of robots cannot be estimated
        # using processing_time_occupancy, but we can still try to use queue_occupancy.
        hard_robot_count_limit = math.floor(current_robot_count / queue_occupancy)
        optimal_robot_count_limit = math.floor(hard_robot_count_limit * 0.8)
    else:
        hard_robot_count_limit = math.floor(current_robot_count / processing_time_occupancy)
        optimal_robot_count_limit = math.floor(hard_robot_count_limit * 0.8)

    data = {
        "id": MIDDLEWARE_TASK_ID,  # String
        "name": NETAPP_NAME,  # Optional, string
        "currentRobotsCount": current_robot_count,  # Nullable, integer
        "optimalLimit": optimal_robot_count_limit,  # Integer
        "hardLimit": hard_robot_count_limit,  # Integer
    }
    return data


class NetworkApplicationServer(Process):
    """Basic implementation of the 5G-ERA Network Application server.

    It creates websocket server and bind callbacks from the 5G-ERA Network Application.
    How to send data? E.g.:
        client.send_image(frame, "image", ChannelType.H264, timestamp, encoding_options=h264_options, sid=sid)
        client.send_image(frame, "image", ChannelType.JPEG, timestamp, metadata, sid)
        client.send_data({"message": "message text"}, "event_name", sid=sid)
        client.send_data({"message": "message text"}, "event_name", ChannelType.JSON_LZ4, sid=sid)
    How to create callbacks_info? E.g.:
        {
            "results": CallbackInfoServer(ChannelType.JSON, results_callback),
            "image": CallbackInfoServer(ChannelType.H264, image_callback, error_callback)
        }
    Callbacks have sid and data parameter: e.g. def image_callback(sid: str, data: Dict[str, Any]):
    Image data dict including decoded frame (data["frame"]) and send timestamp (data["timestamp"]).
    """

    def __init__(
        self,
        port: int,
        callbacks_info=Dict[str, CallbackInfoServer],
        *args,
        command_callback: Optional[Callable[[ControlCommand, str], Tuple[bool, str]]] = None,
        disconnect_callback: Optional[Callable[[str], None]] = None,
        back_pressure_size: Optional[int] = 5,
        recreate_coder_attempts_count: int = 5,
        disconnect_on_unhandled: bool = True,
        stats: bool = False,
        extended_measuring: bool = False,
        host: str = "0.0.0.0",
        async_handlers: bool = False,
        max_message_size: float = 5,
        **kwargs,
    ) -> None:
        """Constructor.

        Args:
            port (int): The port number on which the websocket server should run.
            callbacks_info (Dict[str, CallbackInfoServer]): Callbacks Info dictionary, key is custom event name.
            *args: Process arguments.
            command_callback (Callable[[ControlCommand, str], None], optional): On control command callback.
            disconnect_callback (Callable[[str], None], optional): On data namespace disconnect callback.
            back_pressure_size (int, optional): Back pressure size - max size of eio.sockets[eio_sid].queue.qsize().
            recreate_coder_attempts_count (int): How many times try to recreate the frame encoder/decoder.
            disconnect_on_unhandled (bool): Whether to call self._sio.disconnect(...) if unhandled exception occurs.
            stats (bool): Store output data sizes.
            extended_measuring (bool): Enable logging of measuring.
            host (str): The IP address of the interface, where the websocket server should run. Defaults to "0.0.0.0".
            async_handlers (bool): Specify, if the incoming messages. Defaults to False.
            max_message_size (float): The maximum size of the message to be passed in MB. Defaults to 5.
            **kwargs: Process arguments.
        """

        super().__init__(*args, **kwargs)

        # To get rid of ValueError: Too many packets in payload.
        # (see https://github.com/miguelgrinberg/python-engineio/issues/142)
        Payload.max_decode_packets = 50

        # Create Socket.IO Client.
        # The max_http_buffer_size parameter defines the max size of the message to be passed.
        self._sio = socketio.Server(
            async_mode="threading",
            async_handlers=async_handlers,
            max_http_buffer_size=max_message_size * (1024**2),
            json=ujson,
        )
        self._app = Flask(__name__)
        self._app.wsgi_app = socketio.WSGIApp(self._sio, self._app.wsgi_app)  # type: ignore

        # Create channels - custom callbacks and send functions including encoding.
        # NOTE: DATA_NAMESPACE is assumed to be or will be a connected namespace.
        self._channels = ServerChannels(
            self._sio,
            callbacks_info=callbacks_info,
            disconnect_callback=self._sio.disconnect if disconnect_on_unhandled else None,
            back_pressure_size=back_pressure_size,
            recreate_coder_attempts_count=recreate_coder_attempts_count,
            stats=stats,
            extended_measuring=extended_measuring,
        )

        # Save custom command and disconnect callbacks.
        self._command_callback = command_callback
        self._disconnect_callback = disconnect_callback

        # Register connect, disconnect a command callbacks.
        self._sio.on("connect", self.data_connect_callback, namespace=DATA_NAMESPACE)
        self._sio.on("connect", self.control_connect_callback, namespace=CONTROL_NAMESPACE)

        self._sio.on("command", self.control_command_callback, namespace=CONTROL_NAMESPACE)

        self._sio.on("disconnect", self.data_disconnect_callback, namespace=DATA_NAMESPACE)
        self._sio.on("disconnect", self.control_disconnect_callback, namespace=CONTROL_NAMESPACE)

        # Store host and port.
        self._port = port
        self._host = host

        # Substitute send function calls.
        self.send_image = self._channels.send_image
        self.send_data = self._channels.send_data

    def run_server(self) -> None:
        """Run server."""

        self._app.run(port=self._port, host=self._host)

    def get_sid_of_namespace(self, eio_sid: str, namespace: str) -> str:
        """Get namespace sid.

        Args:
            eio_sid (str): Client sid.
            namespace (str): Namespace.

        Returns:
            Namespace sid.
        """

        return str(self._sio.manager.sid_from_eio_sid(eio_sid, namespace))

    def get_eio_sid_of_namespace(self, sid: str, namespace: str) -> str:
        """Get client eio sid.

        Args:
            sid (str): Namespace sid.
            namespace (str): Namespace.

        Returns:
            Client eio sid.
        """

        return self._channels.get_client_eio_sid(sid, namespace)

    def get_sid_of_data(self, eio_sid: str) -> str:
        """Get DATA_NAMESPACE sid.

        Args:
            eio_sid (str): Client sid.

        Returns:
            DATA_NAMESPACE sid.
        """

        return self.get_sid_of_namespace(eio_sid, DATA_NAMESPACE)

    def get_sid_of_control(self, eio_sid: str) -> str:
        """Get CONTROL_NAMESPACE sid.

        Args:
            eio_sid (str): Client sid.

        Returns:
            CONTROL_NAMESPACE sid.
        """

        return self.get_sid_of_namespace(eio_sid, CONTROL_NAMESPACE)

    def get_eio_sid_of_data(self, sid: str) -> str:
        """Get client eio sid of DATA_NAMESPACE.

        Args:
            sid (str): Namespace sid.

        Returns:
            Client eio sid of DATA_NAMESPACE.
        """

        return self._channels.get_client_eio_sid(sid, DATA_NAMESPACE)

    def get_eio_sid_of_control(self, sid: str) -> str:
        """Get client eio sid of CONTROL_NAMESPACE.

        Args:
            sid (str): Namespace sid.

        Returns:
            Client eio sid of CONTROL_NAMESPACE.
        """

        return self._channels.get_client_eio_sid(sid, CONTROL_NAMESPACE)

    def disconnect(self, sid: str) -> None:
        """Disconnects the client from DATA_NAMESPACE by sid.

        Args:
            sid (str): Namespace sid.
        """

        self._sio.disconnect(sid, DATA_NAMESPACE)

    def send_command_error(self, message: str, sid: str):
        """Send control command error message to client.

        Args:
            message (str): Error message.
            sid (str): Namespace sid.
        """

        self._sio.emit(COMMAND_ERROR_EVENT, {"error": message}, namespace=CONTROL_NAMESPACE, to=sid)

    def data_connect_callback(self, sid: str, environ: Dict) -> None:
        """On connect to DATA_NAMESPACE namespace callback.

        Args:
            sid (str): Namespace sid.
            environ (Dict): WSGI environ dictionary.
        """

        logger.info(
            f"Client {self._channels.get_client_eio_sid(sid, DATA_NAMESPACE)} connected to {DATA_NAMESPACE} "
            f"namespace {sid}, environ {environ}"
        )
        self._sio.send(f"You are connected to {DATA_NAMESPACE} namespace {sid}", namespace=DATA_NAMESPACE)

    def control_connect_callback(self, sid: str, environ: Dict) -> None:
        """On connect to CONTROL_NAMESPACE namespace callback.

        Args:
            sid (str): Namespace sid.
            environ (Dict): WSGI environ dictionary.
        """

        logger.info(
            f"Client {self._channels.get_client_eio_sid(sid, CONTROL_NAMESPACE)} connected to {CONTROL_NAMESPACE} "
            f"namespace {sid}, environ {environ}"
        )
        self._sio.send(f"You are connected to {CONTROL_NAMESPACE} namespace {sid}", namespace=CONTROL_NAMESPACE)

    def control_command_callback(self, sid: str, data: Dict[str, Any]) -> Tuple[bool, str]:
        """Control command callback, parses control command data and call custom callback.

        Args:
            sid (str): Namespace sid.
            data (Dict[str, Any]): Received control command data.

        Returns:
            (properly parsed and processed (bool), message (str)): If False, parsing or processing failed.
        """

        try:
            control_command = ControlCommand(**data)
        except TypeError as e:
            logger.error(f"Could not parse Control Command. {repr(e)}")
            self._sio.emit(
                COMMAND_ERROR_EVENT,
                {"error": f"Could not parse Control Command. {repr(e)}"},
                namespace=CONTROL_NAMESPACE,
                to=sid,
            )
            return False, f"Could not parse Control Command. {repr(e)}"

        logger.info(
            f"Control command {control_command.cmd_type} parsed, "
            f"eio_sid {self.get_eio_sid_of_control(sid)}, sid {sid}"
        )

        if self._command_callback:
            return self._command_callback(control_command, sid)
        else:
            return self.command_callback(control_command, sid)

    def data_disconnect_callback(self, sid: str) -> None:
        """On disconnect from DATA_NAMESPACE namespace callback.

        Args:
            sid (str): Namespace sid.
        """

        if self._disconnect_callback:
            self._disconnect_callback(sid)
        else:
            self.disconnect_callback(sid)
        logger.info(
            f"Client with eio_sid {self.get_eio_sid_of_data(sid)} disconnected from {DATA_NAMESPACE} "
            f"namespace, sid {sid}"
        )

    def control_disconnect_callback(self, sid: str) -> None:
        """On disconnect from CONTROL_NAMESPACE namespace callback.

        Args:
            sid (str): Namespace sid.
        """

        logger.info(
            f"Client with eio_sid {self.get_eio_sid_of_control(sid)} disconnected from {CONTROL_NAMESPACE} "
            f"namespace, sid {sid}"
        )

    def command_callback(self, control_command: ControlCommand, sid: str) -> Tuple[bool, str]:
        """Control command callback with parsed command.

        Args:
            control_command (ControlCommand): Control command.
            sid (str): Namespace sid.

        Returns:
            (success (bool), message (str)): If False, control command callback failed.
        """

        return True, "Control command callback applied"

    def disconnect_callback(self, sid: str) -> None:
        """Custom disconnect callback on DATA_NAMESPACE.

        Args:
            sid (str): Namespace sid.
        """

        return
