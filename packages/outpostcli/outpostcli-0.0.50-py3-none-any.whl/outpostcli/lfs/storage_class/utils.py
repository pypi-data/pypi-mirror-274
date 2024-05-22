import re
from typing import (
    List,
)

import requests
from outpostkit.repository.lfs.logger import create_lfs_logger
from tenacity import retry, stop_after_attempt, wait_exponential

from outpostcli.lfs.exc import handle_request_errors
from outpostcli.lfs.types import UploadedPartObject

_log = create_lfs_logger(__name__)


def try_extracting_part_number(s: str):
    match = re.match(r"part_(\d+)", s)
    if match:
        return int(match.group(1))
    return None


def part_dict_list_to_xml(multi_parts: List[UploadedPartObject]):
    s = "<CompleteMultipartUpload>\n"
    for part in multi_parts:
        s += "  <Part>\n"
        s += "    <PartNumber>%d</PartNumber>\n" % part.get("part_number")
        s += "    <ETag>%s</ETag>\n" % part.get("etag")
        s += "  </Part>\n"
    s += "</CompleteMultipartUpload>"
    return s


@handle_request_errors
@retry(
    reraise=True,
    stop=stop_after_attempt(4),  # Maximum number of retries
    wait=wait_exponential(multiplier=1, min=1, max=60),  # Exponential backoff
)
def complete_multipart_upload(url: str, parts: List[UploadedPartObject]):
    r = requests.post(url, data=part_dict_list_to_xml(parts))
    r.raise_for_status()
    return r


@handle_request_errors
@retry(
    reraise=True,
    stop=stop_after_attempt(4),  # Maximum number of retries
    wait=wait_exponential(multiplier=1, min=1, max=60),  # Exponential backoff
)
def initiate_multipart_upload(url: str) -> str:
    r = requests.post(url, headers={"Content-Type": "application/octet-stream"})
    r.raise_for_status()
    # parse uploadid from response example response
    #   <?xml version='1.0' encoding='UTF-8'?><InitiateMultipartUploadResult xmlns='http://s3.amazonaws.com/doc/2006-03-01/'><Bucket>pr-cache-bucket-0</Bucket><Key>randomfile.tar.gz</Key><UploadId>ABPnzm5hfCDjy44Aa2WDHPxGL9kDyJ3GwtFvToGhVYgNul2PiIOcGI8siu_HjXHeYRkbPxo</UploadId></InitiateMultipartUploadResult>
    upload_id = r.text.split("<UploadId>")[1].split("</UploadId>")[0]
    return upload_id


@handle_request_errors
@retry(
    reraise=True,
    stop=stop_after_attempt(4),  # Maximum number of retries
    wait=wait_exponential(multiplier=1, min=1, max=60),  # Exponential backoff
)
def abort_multipart_upload(url: str):
    r = requests.delete(url)
    r.raise_for_status()
    _log.info(f"aborted multipart upload: {url}")
    return r
