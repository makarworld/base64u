# base64u
Base64u - URL-Safe Base64 variant no padding.
Based on https://gist.github.com/jonleighton/958841

Also main part code was from https://github.com/greymass/eosio-signing-request/blob/ffe7458abb48c4fcd998d7c6b142cdd4c7d46cda/src/base64u.ts

# Installation

```bash
pip install base64u
```

# Usage

```python
import base64u

data = base64u.Uint8Array(10) # like bytearray
encoded = base64u.encode(data)
decoded = base64u.decode(encoded)

print(encoded)
print(decoded)

# data is Uint8Array for assert equality bytearray and List[int]
assert data == [0]*10 
assert encoded == "AAAAAAAAAAAAAA"
assert decoded == data
```
