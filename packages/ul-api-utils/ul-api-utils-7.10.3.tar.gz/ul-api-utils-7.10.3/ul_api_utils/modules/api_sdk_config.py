from enum import Enum
from typing import List, Optional, Callable, Union, Any

from pydantic import BaseModel, Extra, root_validator

from ul_api_utils.access import PermissionRegistry, PermissionDefinition
from ul_api_utils.modules.api_sdk_jwt import ApiSdkJwt


def join_route_paths(prev_sect: str, next_sect: str) -> str:
    return prev_sect.rstrip('/') + '/' + next_sect.lstrip('/')


class SocketAsyncModesEnum(Enum):
    THREADING = 'threading'
    GEVENT = 'gevent'
    EVENTLET = 'eventlet'
    GEVENT_UWSGI = 'gevent_uwsgi'


class ApiSdkIdentifyTypeEnum(Enum):
    DISABLED = 'DISABLED'
    CLIENT_IP = 'IP'
    JWT_USER_ID = 'JWT_USER_ID'

    def __repr__(self) -> str:
        return f'{type(self).__name__}.{self.name}'


class ApiSdkHttpAuth(BaseModel):
    realm: str = 'Hidden Zone'
    scheme: str = 'Basic'


class ApiSdkFlaskDebuggingPluginsEnabled(BaseModel):
    flask_monitoring_dashboard: bool = False


class SocketIOConfig(BaseModel):
    message_queue: str
    channel: Optional[str] = "flask-socketio"
    cors_allowed_origins: Optional[str] = "*"
    logs_enabled: Optional[bool] = False
    engineio_logs_enabled: Optional[bool] = False


class ApiSdkConfig(BaseModel):
    service_name: str
    permissions: Optional[Union[Callable[[], PermissionRegistry], PermissionRegistry]] = None
    permissions_check_enabled: bool = True  # GLOBAL CHECK OF ACCESS AND PERMISSIONS ENABLE
    permissions_validator: Optional[Callable[[ApiSdkJwt, PermissionDefinition], bool]] = None

    jwt_validator: Optional[Callable[[ApiSdkJwt], bool]] = None
    jwt_environment_check_enabled: bool = True

    http_auth: Optional[ApiSdkHttpAuth] = None

    static_url_path: Optional[str] = None
    server_socketio_config: Optional[SocketIOConfig] = None
    client_socketio_config: Optional[SocketIOConfig] = None
    web_error_template: Optional[str] = None

    rate_limit: Union[str, List[str]] = '100/minute'  # [count (int)] [per|/] [second|minute|hour|day|month|year][s]
    rate_limit_storage_uri: str = ''  # supports url of redis, memcached, mongodb
    rate_limit_identify: Union[ApiSdkIdentifyTypeEnum, Callable[[], str]] = ApiSdkIdentifyTypeEnum.DISABLED  # must be None if disabled

    cache_storage_uri: str = ''  # supports only redis
    cache_default_ttl: int = 60  # seconds

    flask_debugging_plugins: Optional[ApiSdkFlaskDebuggingPluginsEnabled] = None

    api_route_path_prefix: str = '/api'

    @staticmethod
    def validate_socketio(values: dict[str, Any]) -> None:
        """
        ApiSdk instance could be either a Socket.IO server or Socket.IO client.
        Client do not need the flask_app process attached to it, but server does.

        Client should use the same config as server (message_queue).
        Validate that ApiSdk instance couldn't be a server and a client simultaneously.
        """
        server_conf, client_conf = values.get("server_socketio_config"), values.get("client_socketio_config")
        service = values["service_name"]
        error_msg = f"Can't create ApiSdkConfig for {service}. ApiSdk cannot be a socketio server and client simultaneously"
        if all([server_conf, client_conf]):
            raise AssertionError(error_msg)

    @root_validator
    def validator(cls, values: dict[str, Any]) -> dict[str, Any]:
        cls.validate_socketio(values)
        return values

    class Config:
        extra = Extra.forbid
        allow_mutation = False
        frozen = True
        arbitrary_types_allowed = True
