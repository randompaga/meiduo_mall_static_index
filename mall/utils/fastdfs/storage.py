
from django.core.files.storage import Storage
from fdfs_client.client import Fdfs_client
from mall import settings
from django.utils.deconstruct import deconstructible

@deconstructible
class FastDFSStorage(Storage):
    def __init__(self,conf_path=None,ip=None):
        if not conf_path:
            conf_path = settings.FDFS_CLIENT_CONF
        self.conf_path = conf_path
        if not ip:
            conf_ip = settings.FDFS_URL
        self.conf_ip = conf_ip

    def _open(self,name, mode='rb'):
        pass
    def _save(self ,mame ,content ,max_length=None):
        client = Fdfs_client(self.conf_path)
        file_data = content.read()
        result = client.upload_by_buffer(file_data)
        if result.get('Status') =='Upload successed.':
            file_id = result.get('Remote file_id')
        else:
            return Exception('上传失败')
        return file_id
    def exists(self, name):
        return False
    def url(self ,name):
        # use for where?
        return self.conf_ip + name

