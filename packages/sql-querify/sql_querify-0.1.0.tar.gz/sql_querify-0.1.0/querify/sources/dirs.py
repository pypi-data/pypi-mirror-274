from . import base_source
from . import clients


class DirSource(
    base_source.BaseSource,
):
    name = 'dirs'

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
        return clients.storage.Dir

    def get_data(
        self,
    ):
        return list(self.storage_client.get_dirs())
