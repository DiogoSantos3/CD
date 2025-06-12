/*
  FibSender.ino

  Send the first N Fibonacci numbers with an 8-bit CRC-8-ATM (poly 0x07)
  over Serial (USB) in simplex mode.
*/

const uint16_t N = 20;          // how many Fibonacci terms to send
const unsigned long BAUD = 9600;
const unsigned long INTERVAL_MS = 500;  // delay between numbers

// compute CRC-8-ATM over a byte buffer
uint8_t compute_crc8(uint8_t *data, size_t len) {
  const uint8_t POLY = 0x07;
  uint8_t crc = 0x00;
  for (size_t i = 0; i < len; i++) {
    crc ^= data[i];
    for (uint8_t b = 0; b < 8; b++) {
      if (crc & 0x80) crc = (crc << 1) ^ POLY;
      else           crc <<= 1;
    }
  }
  return crc;
}

void setup() {
  Serial.begin(BAUD);
  while (!Serial) ;  // wait for USB Serial
}

void loop() {
  // generate and send N Fibonacci numbers
  uint32_t f0 = 0, f1 = 1;
  for (uint16_t i = 0; i < N; i++) {
    uint32_t fi = (i < 2 ? i : f0 + f1);

    // prepare payload: 4-byte big-endian representation
    uint8_t buf[4];
    buf[0] = (fi >> 24) & 0xFF;
    buf[1] = (fi >> 16) & 0xFF;
    buf[2] = (fi >>  8) & 0xFF;
    buf[3] = (fi >>  0) & 0xFF;

    uint8_t crc = compute_crc8(buf, 4);

    // send "value,crc\n" as ASCII
    Serial.print(fi);
    Serial.print(',');
    Serial.println(crc, DEC);

    // slide window
    if (i >= 1) {
      f0 = f1;
      f1 = fi;
    }
    delay(INTERVAL_MS);
  }

  // done sending; stop
  while (true) { }
}
