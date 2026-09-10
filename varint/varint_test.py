from typing import Final

import pytest
from hypothesis import given
from hypothesis import strategies as st

from varint import decode, encode

TESTDATA_PATH: Final[str] = "./varint/testdata"


def read_testdata_as_bytes(filename: str) -> bytes:
    f = open(f"{TESTDATA_PATH}/{filename}", "rb")
    return f.read()


@pytest.mark.parametrize(
    "filename",
    (
        "1.uint64",
        "150.uint64",
        "maxint.uint64",
    ),
)
def test_uint64_file_cases(filename: str) -> None:
    data = read_testdata_as_bytes(filename=filename)
    num = int.from_bytes(data)
    assert decode(data=encode(num=num)) == num


@given(num=st.integers(min_value=0, max_value=1 << 30))
def test_uint64_positive_integers(num: int) -> None:
    assert decode(data=encode(num=num)) == num
