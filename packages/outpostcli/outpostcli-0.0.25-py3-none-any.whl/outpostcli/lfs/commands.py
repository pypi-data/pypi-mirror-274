# ref: https://github.com/huggingface/huggingface_hub/blob/main/src/huggingface_hub/commands/lfs.py
from functools import partial
import json
import logging
import os
import subprocess
import sys
from typing import Dict, Optional

import click
from outpostkit.repository.lfs.logger import create_lfs_logger
from outpostkit.repository.lfs.transfer import MultipartTransferAdapter

from outpostcli.constants import CLI_BINARY_NAME
from outpostcli.lfs.utils import HTTPException
from outpostcli.utils import click_group


@click_group()
def lfs():
    pass


_log = create_lfs_logger(__name__)
_log.setLevel(10)

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
            _log.info("h")
            msg = read_msg()
            _log.info("new message: ", msg)
            if msg is None:
                # When all transfers have been processed, git-lfs will send
                # a terminate event to the stdin of the transfer process.
                # On receiving this message the transfer process should
                # clean up and terminate. No response is expected.
                sys.exit(0)
            oid = msg["oid"]
            filepath = msg["path"]

            _log.info(msg)
            with open(filepath, "rb") as file_obj:
                MultipartTransferAdapter().upload(
                    file_obj, msg["action"], partial(on_progress, oid)
                )
            write_msg({"event": "complete", "oid": oid})
    except HTTPException as e:
        _log.error(e, exc_info=True)
        write_msg({"error": {"code": e.status_code, "message": e.message}})
    except Exception as e:
        _log.error(e, exc_info=True)
        raise
    # except:
    #     write_msg({"error": {"code": 500, "message": "Something went wrong"}})


if __name__ == "__main__":
    lfs()
