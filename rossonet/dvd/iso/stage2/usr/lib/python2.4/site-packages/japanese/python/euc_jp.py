# Tamito KAJIYAMA <12 March 2000>

import codecs

from japanese.mappings import euc_jp, jis_x_0212

class Codec(codecs.Codec):
    # Unicode to character buffer
    def encode(self, data, errors='strict',
               supported_errors=('strict', 'ignore', 'replace')):
        if errors not in supported_errors:
            raise ValueError, "unknown error handling code: " + str(errors)
        m1 = euc_jp.encoding_map
        m2 = jis_x_0212.encoding_map
        buffer = []
        for c in u"" + data:
            if c < u'\u0080':
                buffer.append(c.encode("ascii", errors))
            elif c == u'\u00a5': # YEN SIGN
                buffer.append('\\')
            elif c == u'\u203e': # OVERLINE
                buffer.append('~')
            elif m1.has_key(c):
                buffer.append(m1[c])
            elif c >= u'\uff61' and c <= u'\uff9f':
                buffer.append("\x8e" + self.to_GR(c.encode("japanese.jis-x-0201-katakana", errors)))
            elif m2.has_key(c):
                buffer.append("\x8f" + self.to_GR(m2[c]))
            elif errors == 'replace':
                buffer.append('\xa2\xae') # U+3013 GETA MARK
            elif errors == 'strict':
                raise UnicodeError, "cannot map \\u%04x to EUC-JP" % ord(c)
        return (''.join(buffer), len(data))
    # character buffer to Unicode
    def decode(self, data, errors='strict',
               supported_errors=('strict', 'ignore', 'replace')):
        if errors not in supported_errors:
            raise ValueError, "unknown error handling code: " + str(errors)
        m1 = euc_jp.decoding_map
        m2 = jis_x_0212.decoding_map
        buffer = []
        data = str(data) # character buffer compatible object
        size = len(data)
        p = 0
        while p < size:
            if data[p] < "\x80":
                buffer.append(unicode(data[p], "ascii", errors))
                p = p + 1
            elif data[p] == "\x8e":
                if data[p+1] >= "\x80":
                    buffer.append(unicode(self.to_GL(data[p+1]), "japanese.jis-x-0201-katakana", errors))
                elif errors == 'replace':
                    buffer.append(u'\uFFFD') # REPLACEMENT CHARACTER
                elif errors == 'strict':
                    raise UnicodeError, "unexpected byte 0x%02x found" % ord(data[p+1])
                p = p + 2
            else:
                if data[p] == "\x8f":
                    m = m2
                    c = self.to_GL(data[p+1:p+3])
                    x = p + 1
                    p = p + 3
                else:
                    m = m1
                    c = data[p:p+2]
                    x = p
                    p = p + 2
                if m.has_key(c):
                    buffer.append(m[c])
                elif errors == 'replace':
                    buffer.append(u'\uFFFD') # REPLACEMENT CHARACTER
                elif errors == 'strict':
                    raise UnicodeError, "unexpected byte 0x%02x found" % ord(data[x])
        return (u''.join(buffer), size)
    def to_GL(self, s, func=lambda x, c=chr, o=ord: c(o(x) & 0x7f)):
        return ''.join(map(func, s))
    def to_GR(self, s, func=lambda x, c=chr, o=ord: c(o(x) | 0x80)):
        return ''.join(map(func, s))

class StreamWriter(Codec, codecs.StreamWriter):
    pass

class StreamReader(Codec, codecs.StreamReader):
    def __init__(self, stream, errors='strict'):
        codecs.StreamReader.__init__(self, stream, errors)
        self.data = ''
    def _read(self, func, size):
        if size == 0:
            return u''
        if size is None or size < 0:
            data = self.data + func()
            self.data = ''
        else:
            data = self.data + func(max(size, 2) - len(self.data))
            size = len(data)
            p = 0
            while p < size:
                if data[p] < "\x80":
                    p = p + 1
                elif p + 2 <= size:
                    p = p + 2
                else:
                    break
            data, self.data = data[:p], data[p:]
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
