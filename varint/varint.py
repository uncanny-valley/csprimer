from typing import Final

# the number of lower bits in byte that are dedicated to the payload
PAYLOAD_LENGTH_IN_BITS: Final[int] = 7
# 01111111 mask to isolate the 7-bit payload in a byte
PAYLOAD_BIT_MASK: Final[int] = 0x7F
# 10000000 mask to isolate the continuation bit (i.e. MSB) in a byte
CONTINUATION_BIT_MASK: Final[int] = 0x80


def encode(num: int) -> bytes:
    curr = num
    out = bytearray()
    while curr:
        payload = curr & PAYLOAD_BIT_MASK
        # discard the payload bits from the number now that we've extracted it
        curr = curr >> PAYLOAD_LENGTH_IN_BITS

        # if we have more bytes to process after the current payload, set its
        # continuation bit
        if curr > 0:
            payload |= CONTINUATION_BIT_MASK
        out.append(payload)

    return bytes(out)


def decode(data: bytes) -> int:
    out = 0
    # counter to track how many bits we'll need to shift to place the current byte
    # into position in `out`
    shift = 0
    for byte in data:
        payload = byte & PAYLOAD_BIT_MASK
        mask = payload << shift
        out |= mask
        shift += PAYLOAD_LENGTH_IN_BITS
    return out
