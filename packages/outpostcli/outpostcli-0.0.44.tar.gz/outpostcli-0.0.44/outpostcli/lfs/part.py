from dataclasses import dataclass

import requests
from outpostkit.repository.lfs.logger import create_lfs_logger
from tenacity import retry, stop_after_attempt, wait_exponential

from outpostcli.lfs.exc import ProxyLFSException, handle_request_errors
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


@handle_request_errors
@retry(
    stop=stop_after_attempt(4),  # Maximum number of retries
    wait=wait_exponential(multiplier=1, min=1, max=60),  # Exponential backoff
)
def retriable_upload_part(url: str, data: FileSlice):
    r = requests.put(url, data=data)
    r.raise_for_status()
    return r


@map_wrap
def transfer_part(part: PartInfo):
    with FileSlice(
        part.filepath,
        seek_from=(part.no - 1) * part.chunk_size,
        read_limit=part.chunk_size,
    ) as data:
        try:
            r = retriable_upload_part(part.url, data)
            return UploadedPartObject(
                {
                    "etag": str(r.headers.get("etag")),
                    "part_number": part.no,
                }
            )
        except Exception as e:
            _log.error(e)
            return ProxyLFSException(code=500, message=f"Unhandled Error: {e}")
