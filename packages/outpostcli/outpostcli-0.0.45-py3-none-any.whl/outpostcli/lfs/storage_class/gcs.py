import os
from math import ceil
from multiprocessing import cpu_count
from typing import Any, Dict, Literal, TypedDict

import requests
from outpostkit.repository.lfs.logger import create_lfs_logger

from outpostcli.lfs.comms import write_msg
from outpostcli.lfs.exc import LFSException, ProxyLFSException
from outpostcli.lfs.parallel import multimap
from outpostcli.lfs.part import PartInfo, transfer_part
from outpostcli.lfs.storage_class.utils import (
    abort_multipart_upload,
    complete_multipart_upload,
    initiate_multipart_upload,
)

_log = create_lfs_logger(__name__)


class GCSUploadActionDetails(TypedDict):
    storage_provide: Literal["gcs"]
    chunk_size: str
    abort_url: str
    part_url: str


class GCSUploadAction(TypedDict):
    href: str
    header: Dict[str, str]
    method: Literal["POST"]


class GCSUploadMessage(TypedDict):
    oid: str
    path: str
    action: GCSUploadAction


def gen_part_url(signed_url: str, part_num: int):
    return f"{signed_url}&partNumber={part_num}"


def gen_upload_specific_url(signed_url: str, upload_id: str):
    return f"{signed_url}&uploadId={upload_id}"


def gen_initiate_multipart_url(signed_url: str):
    return f"{signed_url}&uploads"


def gcs_multipart_upload(msg: Dict[str, Any]):
    oid = msg["oid"]
    filepath = msg["path"]

    _log.info(msg)
    initiate_url = msg["action"]["href"]

    upload_id = initiate_multipart_upload(initiate_url)

    header = msg["action"]["header"]
    chunk_size = int(header.pop("chunk_size"))
    abort_url = gen_upload_specific_url(str(header.pop("abort_url")), upload_id)
    part_url = gen_upload_specific_url(str(header.pop("part_url")), upload_id)
    complete_url = gen_upload_specific_url(str(header.pop("complete_url")), upload_id)

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
    file_size = os.path.getsize(filepath)
    num_parts = ceil(file_size / chunk_size)
    try:
        with multimap(cores) as pmap:
            for resp in pmap(
                transfer_part,
                (
                    PartInfo(
                        filepath,
                        i + 1,
                        chunk_size,
                        gen_part_url(part_url, i + 1),
                    )
                    for i in range(num_parts)
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
        complete_multipart_upload(complete_url, parts)
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
