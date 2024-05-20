# ref: https://github.com/huggingface/huggingface_hub/blob/main/src/huggingface_hub/commands/lfs.py
import json
import os
import subprocess
import sys
from multiprocessing import cpu_count
from typing import Dict, List, Optional

import click
import requests
from outpostkit.repository.lfs.logger import create_lfs_logger

from outpostcli.constants import CLI_BINARY_NAME
from outpostcli.lfs.parallel import multimap
from outpostcli.lfs.part import PartInfo, transfer_part
from outpostcli.lfs.utils import part_dict_list_to_xml
from outpostcli.utils import click_group


@click_group()
def lfs():
    pass


_log = create_lfs_logger(__name__)

MULTIPART_UPLOAD_COMMAND_NAME = "multipart-upload"
LFS_MULTIPART_UPLOAD_COMMAND = f"lfs {MULTIPART_UPLOAD_COMMAND_NAME}"


# TODO: find a way to register commands like this
# class LfsCommands(BaseHuggingfaceCLICommand):
#     @staticmethod
#     def register_subcommand(parser: _SubParsersAction):
#         parser.add_command(enable_largefiles)
#         parser.add_command(multipart_upload)

@lfs.command(name="enable-largefiles")
@click.argument("path", type=str)
def enable_largefiles(path):
    """Configure your repository to enable upload of files > 5GB"""
    local_path = os.path.abspath(path)

    if not os.path.isdir(local_path):
        click.echo("This does not look like a valid git repo.")
        sys.exit(1)

    subprocess.run(
        f"git config lfs.customtransfer.multipart-basic.path {CLI_BINARY_NAME}".split(),
        check=True,
        cwd=local_path,
    )

    subprocess.run(
        [
            "git",
            "config",
            "lfs.customtransfer.multipart-basic.args",
            f"{LFS_MULTIPART_UPLOAD_COMMAND}",
        ],
        check=True,
        cwd=local_path,
    )

    subprocess.run(
        [
            "git",
            "config",
            "lfs.customtransfer.multipart-basic.concurrent",
            "false",
        ],
        check=True,
        cwd=local_path,
    )

    click.echo("Local repository set up for largefiles")


def write_msg(msg: Dict):
    """Write out the message in Line delimited JSON."""
    msg_str = json.dumps(msg) + "\n"
    sys.stdout.write(msg_str)
    sys.stdout.flush()

def read_msg() -> Optional[Dict]:
    """Read Line delimited JSON from stdin."""
    msg = json.loads(sys.stdin.readline().strip())
    _log.info(msg)
    if "terminate" in (msg.get("type"), msg.get("event")):
        # terminate message received
        return None

    if msg.get("event") not in ("download", "upload"):
        # logger.critical("Received unexpected message")
        sys.exit(1)

    return msg

@lfs.command(name=MULTIPART_UPLOAD_COMMAND_NAME)
def multipart_upload():
    try:
        """Command called by git lfs directly and is not meant to be called by the user"""
        # ... (rest of the existing code)
        init_msg = json.loads(sys.stdin.readline().strip())

        if not (init_msg.get("event") == "init" and init_msg.get("operation") == "upload"):
            write_msg({"error": {"code": 32, "message": "Wrong lfs init operation"}})
            sys.exit(1)

        _log.info(init_msg)
        # The transfer process should use the information it needs from the
        # initiation structure, and also perform any one-off setup tasks it
        # needs to do. It should then respond on stdout with a simple empty
        # confirmation structure, as follows:
        write_msg({})
        bytes_so_far = 0

        def on_progress(oid: str, uploaded_bytes: int):
            write_msg(
                {
                    "event": "progress",
                    "oid": oid,
                    "bytesSoFar": bytes_so_far + uploaded_bytes,
                    "bytesSinceLast": uploaded_bytes,
                }
            )

        # After the initiation exchange, git-lfs will send any number of
        # transfer requests to the stdin of the transfer process, in a serial sequence.
        while True:
            msg = read_msg()
            if msg is None:
                # When all transfers have been processed, git-lfs will send
                # a terminate event to the stdin of the transfer process.
                # On receiving this message the transfer process should
                # clean up and terminate. No response is expected.
                sys.exit(0)
            oid = msg["oid"]
            filepath = msg["path"]

            _log.info(msg)
            completion_url = msg["action"]["href"]
            header: Dict[str, str] = msg["action"]["header"]
            chunk_size = int(header.pop("chunk_size"))
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
            with multimap(cores) as pmap:
                for resp in pmap(
                    transfer_part,
                    (
                        PartInfo(filepath, i + 1, chunk_size, part)
                        for (i, part) in enumerate(presigned_urls)
                    ),
                ):
                    # write_msg(
                    #     {
                    #         "event": "progress",
                    #         "oid": oid,
                    #         "bytesSoFar": (i + 1) * chunk_size,
                    #         "bytesSinceLast": chunk_size,
                    #     }
                    # )
                    _log.info(resp)
                    parts.append(resp)
                    pass
            # for i, presigned_url in enumerate(presigned_urls):

            # Not precise but that's ok.
            _log.info(parts)
            r = requests.post(
                completion_url,
                data=part_dict_list_to_xml(parts),
            )
            r.raise_for_status()
            write_msg({"event": "complete", "oid": oid})
    except requests.HTTPError as e:
        _log.error(e, exc_info=True)
        write_msg(
            {"error": {"code": e.response.status_code, "message": e.response.text}}
        )
    except Exception as e:
        _log.error(e, exc_info=True)
        raise

if __name__ == "__main__":
    lfs()
