# A codec for JIS X 0201 Katakana
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
for c in range(0x21):
    decoding_map[c] = c
for c in range(0x21, 0x60):
    decoding_map[c] = 0xff40 + c
decoding_map[0x7f] = 0x7f

encoding_map = Mapping()
for k, v in decoding_map.items():
    encoding_map[v] = k
