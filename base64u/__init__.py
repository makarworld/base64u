try:
    from uint8array import Uint8Array
    from base64u import encode, decode
except ImportError:
    from .uint8array import Uint8Array
    from .base64u import encode, decode

__all__ = [
    'encode', 'decode',
    'Uint8Array'
]
