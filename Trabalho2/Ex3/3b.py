#!/usr/bin/env python3
# recv_fib_crc.py

import serial, time, sys, random
from collections import namedtuple

# ----- Parameters -----
PORT       = 'COM4'     # or '/dev/ttyACM0' on Linux/Mac
BAUD       = 9600
N          = 20         # must match Arduino N
TIMEOUT    = 1.0        # seconds
BURST_BITS = 8          # length of burst error
TRIALS     = 1000       # per experiment

Record = namedtuple('Record', ['value', 'crc_tx'])


def crc8(data: bytes, poly=0x07, init=0x00) -> int:
    """Compute CRC-8-ATM over data."""
    crc = init
    for b in data:
        crc ^= b
        for _ in range(8):
            if crc & 0x80:
                crc = ((crc << 1) & 0xFF) ^ poly
            else:
                crc = (crc << 1) & 0xFF
    return crc


def int_to_bytes(n: int) -> bytes:
    """4-byte big-endian."""
    return n.to_bytes(4, 'big')


def inject_single_bit_error(payload: bytes) -> bytes:
    """Flip one random bit in payload."""
    b = bytearray(payload)
    total = len(b) * 8
    bit = random.randrange(total)
    idx, off = divmod(bit, 8)
    b[idx] ^= (1 << off)
    return bytes(b)


def inject_burst_error(payload: bytes, burst_len=BURST_BITS) -> bytes:
    """Flip a burst of burst_len consecutive bits."""
    b = bytearray(payload)
    total = len(b) * 8
    start = random.randrange(total - burst_len + 1)
    for i in range(burst_len):
        idx, off = divmod(start + i, 8)
        b[idx] ^= (1 << off)
    return bytes(b)


def test_crc_detection(received, inject_fn, trials=TRIALS):
    detected = 0
    total = len(received) * trials
    for _ in range(trials):
        for rec in received:
            orig_bytes = int_to_bytes(rec.value)
            corrupt = inject_fn(orig_bytes)
            crc_calc = crc8(corrupt)
            if crc_calc != rec.crc_tx:
                detected += 1
    rate = detected / total * 100
    print(f"{inject_fn.__name__:22s}: detected {detected}/{total} errors ({rate:.2f}%)")


def main():
    # 1) Read from serial
    try:
        ser = serial.Serial(PORT, BAUD, timeout=TIMEOUT)
    except Exception as e:
        print("Failed to open serial port:", e)
        sys.exit(1)
    time.sleep(2)  # allow Arduino reset

    received = []
    print(f"Receiving {N} Fibonacci terms from Arduino on {PORT}…")
    for i in range(N):
        line = ser.readline().decode('ascii', errors='ignore').strip()
        if not line:
            print(f"Timeout reading term {i+1}")
            continue
        parts = line.split(',')
        if len(parts) != 2:
            print("Malformed line:", line)
            continue
        value = int(parts[0])
        crc_tx = int(parts[1])
        print(f"[{i+1:2d}] {value:10d}    CRC={crc_tx:3d}")
        received.append(Record(value, crc_tx))
    ser.close()

    # 2) Test CRC detection
    print("\n-- CRC Detection Experiments --")
    test_crc_detection(received, inject_single_bit_error)
    test_crc_detection(received, inject_burst_error)

if __name__ == "__main__":
    main()
