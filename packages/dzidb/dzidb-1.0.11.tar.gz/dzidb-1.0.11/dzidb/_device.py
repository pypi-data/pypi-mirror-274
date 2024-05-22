import threading
from typing import Optional, Union

from _types import DeviceInfo
from _proto import PROGRAM_NAME
from dzidb import Usbmux


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
Device = BaseDevice
