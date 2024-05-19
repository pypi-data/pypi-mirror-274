import datetime
import pwd
import pydantic
import os
import os.path
import stat


class File(
    pydantic.BaseModel,
):
    name: str
    size_in_bytes: int
    owner: str
    created_date: datetime.datetime
    last_updated_date: datetime.datetime


class Dir(
    pydantic.BaseModel,
):
    name: str
    size_in_bytes: int
    owner: str
    permissions: str
    created_date: datetime.datetime
    last_updated_date: datetime.datetime


class Client:
    @staticmethod
    def get_files() -> list[File]:
        current_dir = os.getcwd()

        for root, _, files in os.walk(current_dir):
            for file in files:
                file_path = os.path.join(root, file)
                file_stats = os.stat(file_path)

                yield File(
                    name=str(file_path),
                    size_in_bytes=file_stats.st_size,
                    owner=pwd.getpwuid(file_stats.st_uid).pw_name if os.name != 'nt' else None,
                    created_date = datetime.datetime.fromtimestamp(file_stats.st_ctime),
                    last_updated_date = datetime.datetime.fromtimestamp(file_stats.st_mtime),
                    last_accessed_date = datetime.datetime.fromtimestamp(file_stats.st_atime),
                )

    @staticmethod
    def get_dirs() -> list[Dir]:
        current_dir = os.getcwd()

        for root, dirnames, _ in os.walk(current_dir):
            for dirname in dirnames:
                dir_path = os.path.join(root, dirname)
                dir_stats = os.stat(dir_path)

                yield Dir(
                    name=str(dir_path),
                    size_in_bytes=sum(
                        os.path.getsize(os.path.join(dir_path, filename))
                        for filename in os.listdir(dir_path)
                        if os.path.isfile(os.path.join(dir_path, filename))
                    ),
                    owner=pwd.getpwuid(dir_stats.st_uid).pw_name if os.name != 'nt' else None,
                    permissions=stat.filemode(dir_stats.st_mode),
                    created_date=datetime.datetime.fromtimestamp(dir_stats.st_ctime),
                    last_updated_date=datetime.datetime.fromtimestamp(dir_stats.st_mtime),
                )
