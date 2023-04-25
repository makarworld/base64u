#
# Base64u - URL-Safe Base64 variant no padding.
# Based on https://gist.github.com/jonleighton/958841
#
# Also main part code was from https://github.com/greymass/eosio-signing-request/blob/ffe7458abb48c4fcd998d7c6b142cdd4c7d46cda/src/base64u.ts
#
from typing import List

# local import class for imitate Uint8Array type in JavaScript
try:
    from uint8array import Uint8Array
except ImportError:
    from .uint8array import Uint8Array

base_charset = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
lookup = Uint8Array(range(256))
for i in range(62):
    lookup[ord(base_charset[i])] = i
# support both urlsafe and standard base64
lookup[ord('+')] = lookup[ord('-')] = 62
lookup[ord('/')] = lookup[ord('_')] = 63



def encode(data: Uint8Array, url_safe: bool = True) -> str:
    byte_remainder = len(data) % 3
    main_length = len(data) - byte_remainder
    charset = base_charset + ('-_' if url_safe else '+/')
    parts = []

    for i in range(0, main_length, 3):
        # Combine the three bytes into a single integer
        chunk = (data[i] << 16) | (data[i + 1] << 8) | data[i + 2]

        # Use bitmasks to extract 6-bit segments from the triplet
        a = (chunk & 16515072) >> 18 # 16515072 = (2^6 - 1) << 18
        b = (chunk & 258048) >> 12   # 258048   = (2^6 - 1) << 12
        c = (chunk & 4032) >> 6      # 4032     = (2^6 - 1) << 6
        d = chunk & 63               # 63       = 2^6 - 1

        # Convert the raw binary segments to the appropriate ASCII encoding
        parts.append(charset[a] + charset[b] + charset[c] + charset[d])

    # Deal with the remaining bytes
    if byte_remainder == 1:
        chunk = data[main_length]

        a = (chunk & 252) >> 2 # 252 = (2^6 - 1) << 2

        # Set the 4 least significant bits to zero
        b = (chunk & 3) << 4   # 3   = 2^2 - 1

        parts.append(charset[a] + charset[b])
    elif byte_remainder == 2:
        chunk = (data[main_length] << 8) | data[main_length + 1]

        a = (chunk & 64512) >> 10 # 64512 = (2^6 - 1) << 10
        b = (chunk & 1008) >> 4   # 1008  = (2^6 - 1) << 4

        # Set the 2 least significant bits to zero
        c = (chunk & 15) << 2     # 15    = 2^4 - 1

        parts.append(charset[a] + charset[b] + charset[c])

    return ''.join(parts)

def decode(input_str: str) -> List[int]:
    input_bytes = Uint8Array(input_str.encode('ascii'))
    byte_length = len(input_bytes) * 3 // 4
    data = Uint8Array(byte_length)

    p = 0
    for i in range(0, len(input_bytes), 4):
        a = lookup[input_bytes[i]]
        b = lookup[input_bytes[i + 1]]
        c = lookup[input_bytes[i + 2]]
        d = lookup[input_bytes[i + 3]]

        data[p] = (a << 2) | (b >> 4)
        data[p + 1] = ((b & 15) << 4) | (c >> 2) if c else 0
        data[p + 2] = ((c & 3) << 6) | ( d & 63) if d else 0 
        p += 3

    return data

if __name__ == "__main__":
    # small test

    # Uint8Array(13) [
    #   1, 2, 3, 0, 1, 0, 
    #   3, 4, 3, 1, 2, 3, 
    #   2
    # ]
    # result: AQIDAAEAAwQDAQIDAg

    data = [1, 2, 3, 0, 1, 0, 3, 4, 3, 1, 2, 3, 2]
    encoded_data = encode(data)
    print(encoded_data)
    decoded_data = decode(encoded_data)
    print(decoded_data)
    
    assert data == decoded_data
    assert encoded_data == 'AQIDAAEAAwQDAQIDAg'
