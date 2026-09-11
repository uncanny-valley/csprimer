import struct
from typing import Final

import pytest
from hypothesis import given
from hypothesis import strategies as st

from varint import SignedVarintCodec, UnsignedVarintCodec

TESTDATA_PATH: Final[str] = "./varint/testdata"


def read_file_as_int(filename: str) -> int:
    f = open(f"{TESTDATA_PATH}/{filename}", "rb")
    return int(struct.unpack(">Q", f.read())[0])


class TestUnsignedIntegers:
    @pytest.fixture
    def codec(self) -> UnsignedVarintCodec:
        return UnsignedVarintCodec()

    def test_basic_unsigned_encode(self, codec: UnsignedVarintCodec) -> None:
        assert codec.encode(num=150) == b"\x96\x01"

    def test_basic_unsigned_decode(self, codec: UnsignedVarintCodec) -> None:
        assert codec.decode(data=b"\x96\x01") == 150

    def test_given_num_is_negative_when_encode_then_raise_value_error(
        self, codec: UnsignedVarintCodec
    ) -> None:
        with pytest.raises(ValueError):
            codec.encode(num=-1)

    @pytest.mark.parametrize(
        "filename",
        (
            "1.uint64",
            "150.uint64",
            "maxint.uint64",
        ),
    )
    def test_uint64_file_round_trips(
        self, codec: UnsignedVarintCodec, filename: str
    ) -> None:
        num = read_file_as_int(filename=filename)
        assert codec.decode(data=codec.encode(num=num)) == num

    @given(num=st.integers(min_value=0, max_value=1 << 30))
    def test_unsigned_integer_round_trips(self, num: int) -> None:
        codec = UnsignedVarintCodec()
        assert codec.decode(data=codec.encode(num=num)) == num


class TestSignedIntegers:
    @pytest.fixture
    def codec(self) -> SignedVarintCodec:
        return SignedVarintCodec()

    def test_basic_signed_encode(self, codec: SignedVarintCodec) -> None:
        assert codec.encode(num=-150) == b"\xab\x02"

    def test_basic_signed_decode(self, codec: SignedVarintCodec) -> None:
        assert codec.decode(data=b"\xab\x02") == -150

    @given(num=st.integers(min_value=-(1 << 30), max_value=1 << 30))
    def test_signed_integer_round_trips(self, num: int) -> None:
        codec = SignedVarintCodec()
        assert codec.decode(data=codec.encode(num=num)) == num
