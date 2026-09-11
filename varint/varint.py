from abc import ABC, abstractmethod
from typing import Final

# the number of lower bits in byte that are dedicated to the payload
_PAYLOAD_LENGTH_IN_BITS: Final[int] = 7

# 01111111 mask to isolate the 7-bit payload in a byte
_PAYLOAD_BIT_MASK: Final[int] = 0x7F

# 10000000 mask to isolate the continuation bit (i.e. MSB) in a byte
_CONTINUATION_BIT_MASK: Final[int] = 0x80


class _Codec(ABC):
    @abstractmethod
    def encode(self, num: int) -> bytes: ...

    @abstractmethod
    def decode(self, data: bytes) -> int: ...


class UnsignedVarintCodec(_Codec):
    """Variable-length integer encoding for unsigned integers"""

    def encode(self, num: int) -> bytes:
        if num < 0:
            raise ValueError("`num` must be non-negative")

        curr = num
        out = bytearray()
        while curr:
            payload = curr & _PAYLOAD_BIT_MASK
            # discard the payload bits from the number now that we've extracted it
            curr >>= _PAYLOAD_LENGTH_IN_BITS

            # if we have more bytes to process after the current payload, set its
            # continuation bit
            if curr > 0:
                payload |= _CONTINUATION_BIT_MASK
            out.append(payload)

        return bytes(out)

    def decode(self, data: bytes) -> int:
        out = 0
        # counter to track how many bits we'll need to shift to place the current byte
        # into position in `out`
        shift = 0
        for byte in data:
            payload = byte & _PAYLOAD_BIT_MASK
            mask = payload << shift
            out |= mask
            shift += _PAYLOAD_LENGTH_IN_BITS
        return out


class SignedVarintCodec(_Codec):
    """Zig-zag encoding for signed integers"""

    def __init__(self) -> None:
        self._unsigned_codec = UnsignedVarintCodec()

    def encode(self, num: int) -> bytes:
        if num < 0:
            num = -2 * num - 1
        else:
            num *= 2

        return self._unsigned_codec.encode(num=num)

    def decode(self, data: bytes) -> int:
        num = self._unsigned_codec.decode(data=data)
        # if the number is odd, then we know it represents a negative number
        if num & 1 == 1:
            return -num // 2

        return num // 2
