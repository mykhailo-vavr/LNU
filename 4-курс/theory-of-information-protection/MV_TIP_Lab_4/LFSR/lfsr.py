def shift_register_key_generation(seed, seed_length, register_length, taps):
    register = seed
    key = ""
    seed_length -= 1

    for _ in range(register_length):
        # print("{:04b}".format(register))
        key += str(register & 1)

        shifts = [register >> tap for tap in taps]
        shifted = register
        for shift in shifts:
            shifted = shifted ^ shift
        new_bit = shifted & 1

        register = (register >> 1) | (new_bit << seed_length)

    return key


seed = 0b1001100110011001100110011001100110011001
seed_length = 40
register_length = 20
feedback_taps = [3, 10]

generated_key = shift_register_key_generation(
    seed, seed_length, register_length, feedback_taps
)

print("Generated Key:", generated_key)
