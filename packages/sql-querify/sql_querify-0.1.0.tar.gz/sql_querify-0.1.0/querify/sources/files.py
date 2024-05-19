from . import base_source
from . import clients


class FileSource(
    base_source.BaseSource,
):
    name = 'files'

    def __init__(
        self,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)

        self.storage_client = clients.storage.Client()

    @property
    def model(
        self,
    ):
        return clients.storage.File

    def get_data(
        self,
    ):
        return list(self.storage_client.get_files())


