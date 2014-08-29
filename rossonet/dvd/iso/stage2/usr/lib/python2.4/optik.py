"""Backward-compatibility version of optparse

Export optparse under the name of optik, and issue a deprecation warning
"""

import warnings
warnings.warn("the optik interface is deprecated; please use optparse instead",
    DeprecationWarning)

import optparse
for s in dir(optparse):
    globals()[s] = getattr(optparse, s)

# Only export what optparse exports
__all__ = [ getattr(optparse, s) for s in dir(optparse) ]
del s
del optparse
