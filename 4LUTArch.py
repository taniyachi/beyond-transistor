import numpy as np
# test file has : Generated 1000000 bits: 499532 ones, 500468 zeros,
# percentage of 1s =49.953199999999995% , percentage of 0=50.046800000000005 %

# LUT bias simulation function with noise

# 4-LUT XOR generator approach
def lut_bias(bias_input):
    A1 = 0.239
    A2 = 102
    x0 = 1.49  # Inflection point (center)
    dx = 0.01334  # Slope
    noise_std = 0.05


    # this is the configuration of device

    input_range = np.linspace(x0 - 0.05, x0 + 0.05, 256)
    current_input = input_range[bias_input]
    y = A2 + (A1 - A2) / (1 + np.exp((current_input - x0) / dx))
    y += np.random.normal(0, noise_std)

    y_norm = (y - A1) / (A2 - A1)
    y_norm = np.clip(y_norm, 0, 1) # float
    return int(y_norm * (2 ** 32 - 1))  # Output a 32-bit unsigned int


# Generate and analyze

def lut_output(bias_input):
    threshold =  lut_bias(128)
    return 1 if lut_bias(bias_input) > threshold else 0


bias_level = 128


def generate_bits(num_bits):
    bits = []
    for _ in range(num_bits):
        l1 = lut_output(bias_level)
        l2 = lut_output(bias_level)
        l3 = lut_output(bias_level)
       # l4 = lut_output(bias_level)
        bit = (l1 ^ l2)
        bits.append(bit)
    return bits

num_cycles = 1000000
# Count 1s and 0s
bits = generate_bits(num_cycles)
num_ones = sum(bits)
num_zeros = len(bits) - num_ones
pof1 = 100 * (num_ones / num_cycles)
pof0 = 100 * (num_zeros / num_cycles)
print(f"Generated {len(bits)} bits: {num_ones} ones, {num_zeros} zeros, percentage of 1s ={pof1}% , percentage of 0={pof0} %")

bits_array = np.array(bits, dtype=np.uint8)

with open("2LUT_test.bin", "wb") as f:
   f.write(bits_array.tobytes())
#with open("3LUT1m.txt", "w") as f:
 #  for bit in bits:
  #    f.write(str(bit))
