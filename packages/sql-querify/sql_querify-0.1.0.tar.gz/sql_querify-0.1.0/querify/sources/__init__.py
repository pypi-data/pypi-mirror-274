from . import base_source
from . import dirs
from . import files
from . import process


sources = {
    'dirs': dirs.DirSource(),
    'files': files.FileSource(),
    'processes': process.ProcessSource(),
}


def get_source_by_name(
    source_name: str,
):
    return sources[source_name]
