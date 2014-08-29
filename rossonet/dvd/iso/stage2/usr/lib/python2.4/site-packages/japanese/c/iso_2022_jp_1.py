# A codec for ISO-2022-JP-1 [RFC2237]
# Tamito KAJIYAMA <18 December 2000>

import codecs, japanese.c._japanese_codecs
import re

US_ASCII      = 1
JISX0201_1976 = 2
JISX0208_1978 = 3
JISX0208_1983 = 4
JISX0212_1990 = 5

CHARSETS = {
    "\033(B": US_ASCII,
    "\033(J": JISX0201_1976,
    "\033$@": JISX0208_1978,
    "\033$B": JISX0208_1983,
    "\033$(D": JISX0212_1990,
}

DESIGNATIONS = {}
for k, v in CHARSETS.items():
    DESIGNATIONS[v] = k

re_designations = re.compile("\033(\\([BJ]|\\$[@B]|\\$\\(D)")

class Codec(codecs.Codec):
    encode = japanese.c._japanese_codecs.iso_2022_jp_1_encode
    decode = japanese.c._japanese_codecs.iso_2022_jp_1_decode

class StreamWriter(Codec, codecs.StreamWriter):
    pass

class StreamReader(Codec, codecs.StreamReader):
    def __init__(self, stream, errors='strict'):
        codecs.StreamReader.__init__(self, stream, errors)
        self.data = ''
        self.charset = US_ASCII
    def _read(self, func, size):
        if size == 0:
            return u''
        if size is None or size < 0:
            data = self.data + func()
        else:
            data = self.data + func(max(size, 8) - len(self.data))
        self.data = ''
        if self.charset != US_ASCII:
            data = DESIGNATIONS[self.charset] + data
        pos = data.rfind("\033")
        if pos >= 0 and not re_designations.match(data, pos):
            # data ends on the way of an escape sequence
            data, self.data = data[:pos], data[pos:]
            pos = data.rfind("\033")
        if pos >= 0:
            match = re_designations.match(data, pos)
            if not match:
                raise UnicodeError, "unknown designation"
            self.charset = CHARSETS[match.group()]
            if self.charset in [JISX0208_1978, JISX0208_1983, JISX0212_1990] and \
               (len(data) - match.end()) % 2 == 1:
                data, self.data = data[:-1], data[-1]
            if self.charset != US_ASCII:
                data = data + DESIGNATIONS[US_ASCII]
        return self.decode(data, self.errors)[0]
    def read(self, size=-1):
        return self._read(self.stream.read, size)
    def readline(self, size=-1):
        return self._read(self.stream.readline, size)
    def readlines(self, size=-1):
        data = self._read(self.stream.read, size)
        buffer = []
        end = 0
        while 1:
            pos = data.find(u'\n', end)
            if pos < 0:
                if end < len(data):
                    buffer.append(data[end:])
                break
            buffer.append(data[end:pos+1])
            end = pos+1
        return buffer
    def reset(self):
        self.data = ''

### encodings module API

def getregentry():
    return (Codec().encode,Codec().decode,StreamReader,StreamWriter)
