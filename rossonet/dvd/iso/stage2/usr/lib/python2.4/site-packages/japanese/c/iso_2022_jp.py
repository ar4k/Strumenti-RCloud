# A codec for ISO-2022-JP [RFC1468] (so-called 7-bit JIS)
# Tamito KAJIYAMA <24 November 2000>

import codecs, japanese.c._japanese_codecs

US_ASCII      = 1
JISX0201_1976 = 2
JISX0208_1978 = 3
JISX0208_1983 = 4

CHARSETS = {
    "\033(B": US_ASCII,
    "\033(J": JISX0201_1976,
    "\033$@": JISX0208_1978,
    "\033$B": JISX0208_1983,
}

DESIGNATIONS = {}
for k, v in CHARSETS.items():
    DESIGNATIONS[v] = k

class Codec(codecs.Codec):
    encode = japanese.c._japanese_codecs.iso_2022_jp_encode
    decode = japanese.c._japanese_codecs.iso_2022_jp_decode

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
        if pos >= 0 and pos + 3 >= len(data):
            # data ends on the way of an escape sequence
            data, self.data = data[:pos], data[pos:]
            pos = data.rfind("\033")
        if pos >= 0:
            try:
                self.charset = CHARSETS[data[pos:pos+3]]
            except KeyError:
                raise UnicodeError, "unknown designation"
            if self.charset in [JISX0208_1978, JISX0208_1983] and \
               (len(data) - pos - 3) % 2 == 1:
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
