# A codec for JIS X 0201 Roman
# Tamito KAJIYAMA <4 December 2000>

import codecs
import UserDict

class Codec(codecs.Codec):
    def encode(self,input,errors='strict'):
        return codecs.charmap_encode(input,errors,encoding_map)
    def decode(self,input,errors='strict'):
        return codecs.charmap_decode(input,errors,decoding_map)

class StreamWriter(Codec,codecs.StreamWriter):
    pass
        
class StreamReader(Codec,codecs.StreamReader):
    pass

### encodings module API

def getregentry():
    return (Codec().encode,Codec().decode,StreamReader,StreamWriter)

class Mapping(UserDict.UserDict):
    def __getitem__(self, key):
        try:
            return UserDict.UserDict.__getitem__(self, key)
        except KeyError:
            return None

decoding_map = Mapping()
for c in range(0x80):
    decoding_map[c] = c
decoding_map[0x5c] = 0xa5   # YEN SIGN
decoding_map[0x7e] = 0x203e # OVERLINE

encoding_map = Mapping()
for k, v in decoding_map.items():
    encoding_map[v] = k
