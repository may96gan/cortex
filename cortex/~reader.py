import protobuf3
import gzip
import shutil
import struct
from cor import User, Snapshot
class Reader:
    def __init__(self, path):
        self.path = path
        self._eof = False
        self._fp = gzip.open(self.path, 'rb')
        length = struct.unpack('I',self._fp.read(4))[0]
        print(length)
        message = self._fp.read(length)
        if not message:
            self._eof = True
        self.user = User()
        self.user.parse_from_bytes(message)
    def read(self):
        while not self._eof:
            yield self._next_snapshot()
    def _next_snapshot(self):
        length = struct.unpack('I',self._fp.read(4))[0]
        print(length)
        message = self._fp.read(length)
        if not message:
            self._eof = True
        snapshot = Snapshot()
        snapshot.parse_from_bytes(message)
        return snapshot
