from multiprocessing import cpu_count
from typing import Any, Dict, List, TypedDict

import requests
from outpostkit.repository.lfs.logger import create_lfs_logger

from outpostcli.lfs.comms import write_msg
from outpostcli.lfs.exc import LFSException, ProxyLFSException
from outpostcli.lfs.parallel import multimap
from outpostcli.lfs.part import PartInfo, transfer_part
from outpostcli.lfs.storage_class.utils import (
    abort_multipart_upload,
    complete_multipart_upload,
)

_log = create_lfs_logger(__name__)


class AWSUploadAction(TypedDict):
    href: str
    header: Dict[str, str]


class AWSUploadMessage(TypedDict):
    oid: str
    path: str
    action: AWSUploadAction


def aws_multipart_upload(msg: Dict[str, Any]):
    oid = msg["oid"]
    filepath = msg["path"]

    _log.info(msg)
    completion_url = msg["action"]["href"]
    header: Dict[str, str] = msg["action"]["header"]
    chunk_size = int(header.pop("chunk_size"))
    abort_url = str(header.pop("abort_url"))
    presigned_urls: List[str] = list(header.values())

    # if i can extract part number from url, no need for this.
    # parts: List[Tuple[int, str]] = []
    # for k, v in header.items():
    #     pNo = try_extracting_part_number(k)
    #     if pNo:
    #         parts.append((pNo, v))s
    parts = []
    cores = cpu_count()
    _log.info({"cores": cores})
    bytes_so_far = 0
    try:
        with multimap(cores) as pmap:
            for resp in pmap(
                transfer_part,
                (
                    PartInfo(filepath, i + 1, chunk_size, part)
                    for (i, part) in enumerate(presigned_urls)
                ),
            ):
                if isinstance(resp, ProxyLFSException):
                    raise LFSException(
                        code=resp.code,
                        message=resp.message,
                        doc_url=resp.doc_url,
                    )
                else:
                    bytes_so_far += chunk_size
                    # Not precise but that's ok.
                    write_msg(
                        {
                            "event": "progress",
                            "oid": oid,
                            "bytesSoFar": bytes_so_far,
                            "bytesSinceLast": chunk_size,
                        }
                    )
                    parts.append(resp)
                    pass
        complete_multipart_upload(completion_url, parts)
        write_msg({"event": "complete", "oid": oid})
    except LFSException as e:
        abort_multipart_upload(abort_url)
        write_msg({"error": {"code": e.code, "message": e.message}})
    except requests.HTTPError as e:
        abort_multipart_upload(abort_url)
        _log.error(e, exc_info=True)
        write_msg(
            {
                "error": {
                    "code": e.response.status_code,
                    "message": e.response.text,
                }
            }
        )
    except Exception as e:
        abort_multipart_upload(abort_url)
        _log.error(e, exc_info=True)
        raise
