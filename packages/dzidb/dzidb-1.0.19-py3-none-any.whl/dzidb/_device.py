import threading
from typing import Optional, Union

from ._safe_socket import PlistSocketProxy
from ._types import DeviceInfo
from ._proto import PROGRAM_NAME, LOCKDOWN_PORT
from ._usbmux import Usbmux
from ._utils import set_socket_timeout


class BaseDevice():
    def __init__(self,
                 udid: Optional[str] = None,
                 usbmux: Union[Usbmux, str, None] = None):
        if not usbmux:
            self._usbmux = Usbmux()
        elif isinstance(usbmux, str):
            self._usbmux = Usbmux(usbmux)
        elif isinstance(usbmux, Usbmux):
            self._usbmux = usbmux

        self._udid = udid
        self._info: DeviceInfo = None
        self._lock = threading.Lock()
        self._pair_record = None
    @property
    def name(self) -> str:
        return self.get_value("DeviceName", no_session=True)
    @property
    def product_type(self) -> str:
        return self.get_value("ProductType", no_session=True)
    @property
    def product_version(self) -> str:
        return self.get_value("ProductVersion", no_session=True)
    def get_value(self, key: str = '', domain: str = "", no_session: bool = False):
        """ key can be: ProductVersion
        Args:
            domain (str): com.apple.disk_usage
            no_session: set to True when not paired
        """
        request = {
            "Request": "GetValue",
            "Label": PROGRAM_NAME,
        }
        if key:
            request['Key'] = key
        if domain:
            request['Domain'] = domain

        if no_session:
            with self.create_inner_connection() as s:
                ret = s.send_recv_packet(request)
                return ret['Value']
        else:
            with self.create_session() as conn:
                ret = conn.send_recv_packet(request)
                return ret.get('Value')
    def create_inner_connection(
            self,
            port: int = LOCKDOWN_PORT,  # 0xf27e,
            _ssl: bool = False,
            ssl_dial_only: bool = False) -> PlistSocketProxy:
        """
        make connection to iphone inner port
        """
        device_id = self.info.device_id
        conn = self._usbmux.connect_device_port(device_id, port)
        if _ssl:
            with set_socket_timeout(conn.get_socket, 10.0):
                psock = conn.psock
                psock.switch_to_ssl(self.ssl_pemfile_path)
                if ssl_dial_only:
                    psock.ssl_unwrap()
        return conn
Device = BaseDevice
