import requests
from outpostkit.repository.lfs.logger import create_lfs_logger

from outpostcli.lfs.file_slice import FileSlice
from outpostcli.lfs.types import UploadedPartObject

_log = create_lfs_logger(__name__)


def transfer_part(filepath: str, part_number: int, chunk_size: int, presigned_url: str):
    with FileSlice(
        filepath, seek_from=(part_number - 1) * chunk_size, read_limit=chunk_size
    ) as data:
        try:
            r = requests.put(presigned_url, data=data)
            r.raise_for_status()

            return UploadedPartObject(
                {
                    "etag": str(r.headers.get("etag")),
                    "part_number": part_number,
                }
            )
        except Exception as e:
            _log.error(e)
            raise
