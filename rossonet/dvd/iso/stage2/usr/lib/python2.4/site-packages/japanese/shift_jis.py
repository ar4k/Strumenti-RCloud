# Tamito KAJIYAMA <24 September 2001>

try:
    from japanese.c.shift_jis import *
except ImportError:
    from japanese.python.shift_jis import *
