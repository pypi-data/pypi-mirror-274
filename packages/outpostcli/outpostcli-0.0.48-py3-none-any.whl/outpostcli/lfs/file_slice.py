import os
from contextlib import AbstractContextManager


class FileSlice(AbstractContextManager):
    """
    File-like object that only reads a slice of a file

    Inspired by stackoverflow.com/a/29838711/593036
    """

    def __init__(self, filepath: str, seek_from: int, read_limit: int):
        self.filepath = filepath
        self.seek_from = seek_from
        self.read_limit = read_limit
        self.n_seen = 0

    def __enter__(self):
        self.f = open(self.filepath, "rb")
        self.f.seek(self.seek_from)
        return self

    def __len__(self):
        total_length = os.fstat(self.f.fileno()).st_size
        return min(self.read_limit, total_length - self.seek_from)

    def read(self, n=-1):
        if self.n_seen >= self.read_limit:
            return b""
        remaining_amount = self.read_limit - self.n_seen
        data = self.f.read(remaining_amount if n < 0 else min(n, remaining_amount))
        self.n_seen += len(data)
        return data

    def __iter__(self):
        yield self.read(n=4 * 1024 * 1024)

    def __exit__(self, *args):
        self.f.close()
