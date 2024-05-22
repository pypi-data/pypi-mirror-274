# coding: utf-8
#

import os
import shutil
import tempfile
import time
import typing
import zipfile
from typing import List

import retry
import requests

from ._safe_socket import PlistSocketProxy
from ._utils import get_app_dir, logger
from .exceptions import DeveloperImageError, MuxError, MuxServiceError, DownloadError

_REQUESTS_TIMEOUT = 30.0


@retry.retry(exceptions=requests.ReadTimeout, tries=3, delay=.5)
def _urlretrieve(url, local_filename):
    """ download url to local """
    logger.info("Download %s -> %s", url, local_filename)

    try:
        tmp_local_filename = local_filename + f".download-{int(time.time()*1000)}"
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        with requests.get(url, headers=headers, stream=True, timeout=_REQUESTS_TIMEOUT) as r:
            try:
                r.raise_for_status()
            except requests.HTTPError as e:
                raise DownloadError(f"Download {url} failed: {r.status_code}", e)
            with open(tmp_local_filename, 'wb') as f:
                shutil.copyfileobj(r.raw, f, length=16<<20)
                f.flush()
            os.rename(tmp_local_filename, local_filename)
            logger.info("%r download successfully", local_filename)
    finally:
        if os.path.isfile(tmp_local_filename):
            os.remove(tmp_local_filename)
            

def _get_developer_image_url_list(version: str) -> typing.List[str]:
    """ return url list which may contains mirror url """
    # https://github.com/JinjunHan/iOSDeviceSupport
    # alternative repo: https://github.com/iGhibli/iOS-DeviceSupport
    github_repo = "JinjunHan/iOSDeviceSupport"

    zip_name = f"{version}.zip"
    origin_url = f"https://github.com/{github_repo}/raw/master/iOSDeviceSupport/{zip_name}"
    return (origin_url,)

def cache_developer_image(version: str) -> str:
    """
    download developer image from github to local
    return image_zip_path
    """
    _alias = {
        "12.5": "12.4",
        "15.8": "15.5",
        # "16.5": "17.0",
    }
    if version in _alias:
        version = _alias[version]
        logger.info("Use alternative developer image %s", version)

    # Default download image from https://github.com/JinjunHan/iOSDeviceSupport
    image_urls = _get_developer_image_url_list(version)

    # $HOME/.tidevice/device-support/12.2.zip
    local_device_support = get_app_dir("device-support")
    image_zip_path = os.path.join(local_device_support, version+".zip")
    if not zipfile.is_zipfile(image_zip_path):
        err = None
        for url in image_urls:
            try:
                _urlretrieve(url, image_zip_path)
                if zipfile.is_zipfile(image_zip_path):
                    err = None
                    break
                err = Exception("image file not zip")
            except requests.HTTPError as e:
                err = e
                if e.response.status_code == 404:
                    break
            except requests.RequestException as e:
                err = e
        if err:
            raise err
    return image_zip_path

def get_developer_image_path(version: str) -> str:
    """ return developer image path 
    Raises:
        - DeveloperImageError
        - DownloadError
    """
    if version.startswith("17."):
        raise DeveloperImageError("iOS 17.x is not supported yet")
    image_zip_path = cache_developer_image(version)
    image_path = get_app_dir("device-support/"+version)
    if os.path.isfile(os.path.join(image_path, "DeveloperDiskImage.dmg")):
        return image_path

    # 解压下载的zip文件
    with tempfile.TemporaryDirectory() as tmpdir:
        zf = zipfile.ZipFile(image_zip_path)
        zf.extractall(tmpdir)
        rootfiles = os.listdir(tmpdir)

        rootdirs = []
        for fname in rootfiles:
            if fname.startswith("_") or fname.startswith("."):
                continue
            if os.path.isdir(os.path.join(tmpdir, fname)):
                rootdirs.append(fname)

        dmg_path = tmpdir
        if len(rootfiles) == 0: # empty zip
            raise DeveloperImageError("deviceSupport zip file is empty")
        elif version in rootdirs: # contains directory: {version}
            dmg_path = os.path.join(tmpdir, version)
        elif len(rootdirs) == 1: # only contain one directory
            dmg_path = os.path.join(tmpdir, rootdirs[0])
        
        if not os.path.isfile(os.path.join(dmg_path, "DeveloperDiskImage.dmg")):
            raise DeveloperImageError("deviceSupport zip file is invalid")

        os.makedirs(image_path, exist_ok=True)
        for filename in ("DeveloperDiskImage.dmg", "DeveloperDiskImage.dmg.signature"):
            shutil.copyfile(os.path.join(dmg_path, filename), os.path.join(image_path, filename))
    return image_path


class ImageMounter(PlistSocketProxy):
    SERVICE_NAME = "com.apple.mobile.mobile_image_mounter"

    def prepare(self):
        """
        Note: LookupImage might stuck and no response
        """
        return super().prepare()
    
    def lookup(self, image_type="Developer") -> List[bytes]:
        """
        Check image signature
        """
        ret = self.send_recv_packet({
            "Command": "LookupImage",
            "ImageType": image_type,
        })
        if 'Error' in ret:
            raise MuxError(ret['Error'])
        return ret.get('ImageSignature', [])
        
    def is_developer_mounted(self) -> bool:
        """
        Check if developer image mounted

        Raises:
            MuxError("DeviceLocked")
        """
        return len(self.lookup()) > 0
    
    def _check_error(self, ret: dict):
        if 'Error' in ret:
            raise MuxError(ret['Error'])

    def mount(self,
                image_path: str,
                image_signature_path: str):
        """ Mount developer disk image from local files """
        assert os.path.isfile(image_path), image_path
        assert os.path.isfile(image_signature_path), image_signature_path
        
        logger.debug("image path: %s, %s", image_path, image_signature_path)
        with open(image_signature_path, 'rb') as f:
            signature_content = f.read()
        
        image_size = os.path.getsize(image_path)

        with open(image_path, "rb") as image_reader:
            return self.mount_fileobj(image_reader, image_size, signature_content)
        
    def mount_fileobj(self,
                image_reader: typing.IO,
                image_size: int,
                signature_content: bytes,
                image_type: str = "Developer"):

        ret = self.send_recv_packet({
            "Command": "ReceiveBytes",
            "ImageSignature": signature_content,
            "ImageSize": image_size,
            "ImageType": image_type,
        })
        self._check_error(ret)
        assert ret['Status'] == 'ReceiveBytesAck'

        # Send data through SSL
        logger.info("Pushing DeveloperDiskImage.dmg")
        chunk_size = 1<<14

        while True:
            chunk = image_reader.read(chunk_size)
            if not chunk:
                break
            self.psock.sendall(chunk)

        ret = self.psock.recv_packet()
        self._check_error(ret)
        
        assert ret['Status'] == 'Complete'
        logger.info("Push complete")

        self.psock.send_packet({
            "Command": "MountImage",
            "ImagePath": "/private/var/mobile/Media/PublicStaging/staging.dimag",
            "ImageSignature": signature_content, # FIXME(ssx): ...
            "ImageType": image_type,
        })
        ret = self.psock.recv_packet()
        if 'DetailedError' in ret:
            if 'is already mounted at /Developer' in ret['DetailedError']:
                raise MuxError("DeveloperImage is already mounted")
        self._check_error(ret)
