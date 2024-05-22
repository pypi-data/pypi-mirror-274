import logging
from dataclasses import dataclass

import requests
from outpostkit.repository.lfs.logger import create_lfs_logger
from tenacity import before_sleep_log, retry, stop_after_attempt, wait_exponential

from outpostcli.lfs.exc import LFSException, ProxyLFSException, handle_request_errors
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


@handle_request_errors("UploadPart")
@retry(
    reraise=True,
    stop=stop_after_attempt(4),  # Maximum number of retries
    wait=wait_exponential(multiplier=1, min=4, max=60),  # Exponential backoff
    before_sleep=before_sleep_log(_log, logging.INFO, exc_info=True),
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
            _log.info(f"uploading part of {part.filepath}, part no: {part.no}")
            r = retriable_upload_part(part.url, data)
            if isinstance(r, LFSException):
                return LFSException(code=r.code, message=r.message, doc_url=r.doc_url)
            else:
                etag = str(r.headers.get("etag"))
                _log.info(
                    f"completed upload part of {part.filepath}, part no: {part.no}, etag: {etag}"
                )
                return UploadedPartObject(
                    {
                        "etag": etag,
                        "part_number": part.no,
                    }
                )
        except Exception as e:
            _log.error(e, exc_info=True)
            return ProxyLFSException(code=500, message=f"Unhandled Error: {e}")
