import argparse
import base64
import json
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tabulate import tabulate

from dzidb import Usbmux
from dzidb._device import Device
import typing
from dzidb._proto import MODELS, ConnectionType
from dzidb.exceptions import MuxError

um: Usbmux = None


# 定义命令函数
def cmd_devices(args):
    _json: typing.Final[bool] = args.json
    ds = um.device_list()
    if args.usb:
        ds = [info for info in ds if info.conn_type == ConnectionType.USB]

    if args.one:
        for info in ds:
            print(info.udid)
        return

    headers = ['UDID', 'SerialNumber', 'NAME', 'MarketName', 'ProductVersion', "ConnType"]
    keys = ["udid", "serial", "name", "market_name", "product_version", "conn_type"]
    tabdata = []
    for dinfo in ds:
        udid, conn_type = dinfo.udid, dinfo.conn_type
        try:
            _d = Device(udid, um)
            name = _d.name
            serial = _d.get_value("SerialNumber")
            tabdata.append([udid, serial, name, MODELS.get(_d.product_type, "-"), _d.product_version, conn_type])

        except MuxError:
            name = ""
    if _json:
        result = []
        for item in tabdata:
            result.append({key: item[idx] for idx, key in enumerate(keys)})
        _print_json(result)
    else:
        print(tabulate(tabdata, headers=headers, tablefmt="plain"))

def cmd_screencap(args):
    a = 1

def _print_json(value):
    def _bytes_hook(obj):
        if isinstance(obj, bytes):
            return base64.b64encode(obj).decode()
        else:
            return str(obj)

    print(json.dumps(value, indent=4, ensure_ascii=False, default=_bytes_hook))

commands = [
    dict(action=cmd_devices,
         command="devices",
         flags=[
             dict(args=['-l'],
                  action='store_true',
                  help='output one entry per line')
         ],
         help="show connected iOS devices"),
    dict(action=cmd_screencap,
         command="screencap",
         flags=[
             dict(args=['-u', '--device'],
                  required=True,
                  help='device identifier'),
             dict(args=['-p', '--output'],
                  required=True,
                  help='output file path')
         ],
         help="take a screenshot from the device"),
]

def main():
    parser = argparse.ArgumentParser(
        description='Custom adb-like tool.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--socket", help="usbmuxd listen address, host:port or local-path")

    subparsers = parser.add_subparsers(dest='subparser')
    actions = {}
    for c in commands:
        cmd_name = c['command']
        cmd_aliases = c.get('aliases', [])
        for alias in [cmd_name] + cmd_aliases:
            actions[alias] = c['action']
        sp = subparsers.add_parser(cmd_name, aliases=cmd_aliases, help=c.get('help'),
                                  formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        for f in c.get('flags', []):
            args = f.get('args')

            if not args:
                args = ['-'*min(2, len(n)) + n for n in f['name']]

            kwargs = f.copy()
            kwargs.pop('name', None)
            kwargs.pop('args', None)
            sp.add_argument(*args, **kwargs)


    # 解析命令行参数
    args = parser.parse_args()

    um = Usbmux(args.socket)
    # 检查命令是否存在于字典中
    if args.command in commands:
        # 调用相应的函数
        actions[args.command](args)
    else:
        print(f"Unknown command: {args.command}")

if __name__ == '__main__':
    main()