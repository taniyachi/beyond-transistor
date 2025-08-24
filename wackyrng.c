#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <math.h>

FILE *randf;

uint32_t urand(void) {
  uint32_t out;
  (void) !!fread(&out, sizeof(out), 1, randf);
  return out;
}
#define URAND_MAX (1LLU<<32)

double rand_normal(double mean, double stddev) {
  double u1 = (urand() + 1.0) / (URAND_MAX + 2.0);
  double u2 = (urand() + 1.0) / (URAND_MAX + 2.0);
  double z0 = sqrt(-2.0 * log(u1)) * cos(2.0 * M_PI * u2);
  return z0 * stddev + mean;
}

// i bet that i could make this way more random nearly Instantly.
uint32_t lut_bias() {
  double y = 0.5023486404418196 + rand_normal(0.0023486404418195574, 0.0004913473727655978);
  if (y < 0.0L) y = 0.0L;
  if (y > 1.0L) y = 1.0L;
  return (uint32_t)(y * 4294967295.0);
}

unsigned rand_bit(void) {
  static uint32_t state = 0xabcc6efe;
  unsigned b31 = (state >> 31) & 1;
  unsigned b21 = (state >> 21) & 1;
  unsigned b1 = (state >> 1) & 1;
  unsigned b0 = (state >> 0) & 1;
  uint32_t lut = lut_bias();
  unsigned lut_bit0 = lut & 1;
  unsigned lut_bit1 = (lut >> 16) & 1;
  uint32_t feedback = (b31 ^ b21 ^ b1 ^ b0 ^ lut_bit0 ^ lut_bit1 ^ 1) & 1;
  state = state << 1 | feedback;
  return feedback;
}

int main(int argc, char *argv[]) {
  randf = fopen("/dev/urandom", "rb");
  for (long long i = atoll(argv[1]); i; --i) {
    unsigned x = 0;
    for (unsigned b = 0; b < 8; ++b) {
      x <<= 1;
      x |= rand_bit();
    }
    putchar(x);
  }
  return 0;
}
