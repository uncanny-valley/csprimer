
def encode(num: int) -> bytes:
    curr = num
    out = bytearray()
    while curr:
        payload = curr & 0x7F
        curr = curr >> 7
        if curr > 0:
            payload |= 0x80
        out.append(payload)

    return out


def decode(data: bytes) -> int: 
    out = 0
    shift = 0
    for byte in data: 
        payload = byte & 0x7F
        mask = payload << shift 
        out |= mask
        shift += 7
    return out
