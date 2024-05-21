from flask_socketio import SocketIO  # type: ignore

from ul_api_utils.modules.api_sdk_config import SocketIOConfig, SocketAsyncModesEnum


def init_socketio(server_config: SocketIOConfig | None, client_config: SocketIOConfig | None) -> SocketIO | None:
    socketio = None
    if server_config is not None:
        socketio = SocketIO()

    if client_config is not None:
        socketio = SocketIO(
            message_queue=client_config.message_queue,
            async_mode=SocketAsyncModesEnum.GEVENT.value,
            channel=client_config.channel,
            cors_allowed_origins=client_config.cors_allowed_origins,
            logger=client_config.logs_enabled,
            engineio_logger=client_config.engineio_logs_enabled,
        )
    return socketio
