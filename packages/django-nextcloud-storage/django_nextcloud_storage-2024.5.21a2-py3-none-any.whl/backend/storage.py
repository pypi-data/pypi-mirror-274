import os
from io import BytesIO
from typing import IO, Self

import nc_py_api
from django.conf import settings
from django.core.files.base import File
from django.core.files.storage import Storage
from nc_py_api._exceptions import NextcloudException


class NCFile(File):
    def __init__(self, name: str, mode: str, storage: "NextCloudStorage") -> None:
        self.storage: NextCloudStorage = storage
        self._mode: str = mode
        self.name: str = name
        self.file: IO | None = None
        self._is_dirty: bool = False
        self._closed: bool = False
        self._is_read: bool = False

    def open(self, mode: str | None = None, *args, **kwargs) -> Self:
        if mode is None:
            mode = "rb"
        # Implement file opening logic using nc_py_api
        self._is_read = True
        if self.file is not None and not self.closed:
            self.seek(0)  # Mirror Django's behavior
        elif mode and mode != self._mode:
            raise ValueError("Cannot reopen file with a new mode.")

        # Accessing the file will functionally re-open it
        self._get_file()  # noqa: B018
        return self

    def _get_file(self) -> None:
        if self.file is None:
            self.file = BytesIO(self.storage.nc_client.files.download(self.name))
            if "r" in self._mode:
                self._is_dirty = False
                self.file.seek(0)
            self._closed = False

    def write(self, content):
        if "w" not in self._mode:
            raise AttributeError("File was not opened in write mode.")
        self._is_dirty = True
        return super().write(content)

    def close(self):
        if self._is_dirty:
            self.storage.nc_client.files.upload_stream(self.storage.get_file_path(self.name), self.file)
        self._closed = True
        self._is_dirty = False

    def read(self, *args, **kwargs):
        if not self._is_read:
            self._get_file()
        return self.file.read(*args, **kwargs)


class NextCloudStorage(Storage):
    def __init__(self) -> None:
        self.nc_client: nc_py_api.Nextcloud = nc_py_api.Nextcloud(
            nextcloud_url=settings.NEXTCLOUD_STORAGE_URL,
            nc_auth_user=settings.NEXTCLOUD_STORAGE_USERNAME,
            nc_auth_pass=settings.NEXTCLOUD_STORAGE_PASSWORD,
        )
        self.location: str = settings.NEXTCLOUD_STORAGE_DIRECTORY
        self.file_overwrite: bool = settings.NEXTCLOUD_FILE_OWERWRITE

    def get_file_path(self, name: str) -> str:
        return "/".join([self.location, name])

    def delete(self, name: str) -> None:
        self.nc_client.files.delete(path=self.get_file_path(name), not_fail=True)

    def exists(self, name: str) -> bool:
        try:
            return bool(self.nc_client.files.by_path(path=self.get_file_path(name)))
        except NextcloudException as ex:
            if ex.status_code == 404:
                return False
            raise

    def listdir(self, name: str) -> tuple[list[str], list[str]]:
        directory_content = self.nc_client.files.listdir(path=self.get_file_path(name))
        files = []
        directories = []
        for item in directory_content:
            if item.is_dir:
                directories.append(item.full_path)
            else:
                files.append(item.full_path)
        return directories, files

    def size(self, name: str) -> int:
        _file = self.nc_client.files.by_path(path=self.get_file_path(name))
        return _file.info.size

    def url(self, name: str | None) -> str:
        if name is None:
            raise ValueError("null name is not permitted.")
        file_path = self.get_file_path(name)
        if shared_list := self.nc_client.files.sharing.get_list(path=file_path):
            shared = shared_list[0]
        else:
            shared = self.nc_client.files.sharing.create(
                path=file_path,
                permissions=nc_py_api.FilePermissions.PERMISSION_READ,
                share_type=nc_py_api.ShareType.TYPE_LINK,
            )
        # by default nextcloud api returns share url of the file which opens the nextcloud interface
        # we change the url to get the download link
        return shared._raw_data.get("url") + "/download" + shared._raw_data.get("file_target")

    def _save(self, name: str, content) -> str:
        full_path = self.get_file_path(name)
        self.nc_client.files.makedirs(path=os.path.dirname(full_path), exist_ok=True)
        content.seek(0)
        self.nc_client.files.upload_stream(path=full_path, fp=content)
        return name

    def _open(self, name: str, mode="rb") -> File:
        file_path = self.get_file_path(name)
        return NCFile(file_path, mode=mode, storage=self)

    @staticmethod
    def get_available_overwrite_name(name: str, max_length: int) -> str:
        if max_length is None or len(name) <= max_length:
            return name

        # Adapted from Django
        dir_name, file_name = os.path.split(name)
        file_root, file_ext = os.path.splitext(file_name)
        truncation = len(name) - max_length

        file_root = file_root[:-truncation]
        if not file_root:
            raise RuntimeError(
                f'Storage tried to truncate away entire filename "{name}". '
                "Please make sure that the corresponding file field "
                'allows sufficient "max_length".'
            )
        return os.path.join(dir_name, f"{file_root}{file_ext}")

    def get_available_name(self, name: str, max_length=None) -> str:
        """Overwrite existing file with the same name."""
        if self.file_overwrite:
            return self.get_available_overwrite_name(name, max_length)
        return super().get_available_name(name, max_length)
