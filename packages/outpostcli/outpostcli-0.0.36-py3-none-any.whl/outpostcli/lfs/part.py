from dataclasses import dataclass
import requests
from outpostkit.repository.lfs.logger import create_lfs_logger

from outpostcli.lfs.file_slice import FileSlice
from outpostcli.lfs.parallel import map_wrap
from outpostcli.lfs.types import UploadedPartObject

_log = create_lfs_logger(__name__)


@dataclass
class PartInfo:
    filepath: str
    no: int
    chunk_size: int
    url: str


@map_wrap
def transfer_part(part: PartInfo):
    with FileSlice(
        part.filepath,
        seek_from=(part.no - 1) * part.chunk_size,
        read_limit=part.chunk_size,
    ) as data:
        try:
            r = requests.put(part.url, data=data)
            r.raise_for_status()

            return UploadedPartObject(
                {
                    "etag": str(r.headers.get("etag")),
                    "part_number": part.no,
                }
            )
        except Exception as e:
            _log.error(e)
            raise
