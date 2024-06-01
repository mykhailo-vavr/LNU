import random
from math import gcd


def is_prime(num, num_trials=5):
    if num < 2:
        return False
    for _ in range(num_trials):
        a = random.randint(2, num - 1)
        if pow(a, num - 1, num) != 1:
            return False
    return True


def generate_large_prime(bits):
    while True:
        candidate = random.getrandbits(bits)
        if is_prime(candidate):
            return candidate


def generate_coprime(n):
    while True:
        x = random.randint(2, n - 1)
        if gcd(x, n) == 1:
            return x


def bbs_generator(n, x):
    while True:
        x = (x**2) % n
        yield x % 2


def encrypt(message, n, x):
    bit_generator = bbs_generator(n, x)
    encrypted_message = [ord(char) ^ next(bit_generator) for char in message]
    return encrypted_message


def decrypt(encrypted_message, n, x):
    bit_generator = bbs_generator(n, x)
    decrypted_message = "".join(
        [chr(char ^ next(bit_generator)) for char in encrypted_message]
    )
    return decrypted_message


def main():
    with open("text.txt", "r") as file:
        original_message = file.read()

    # Генерація двох великих простих чисел p та q
    p = generate_large_prime(512)
    q = generate_large_prime(512)
    n = p * q
    x = generate_coprime(n)

    print("p:", p)
    print("q:", q)

    print("n:", n)
    print("x:", x)

    encrypted_message = encrypt(original_message, n, x)

    with open("encrypted.txt", "w") as file:
        file.write(" ".join(map(str, encrypted_message)))

    decrypted_message = decrypt(encrypted_message, n, x)

    with open("decrypted.txt", "w") as file:
        file.write(decrypted_message)

    print("Written to 'encrypted.txt'")
    print("Written to 'decrypted.txt'")


if __name__ == "__main__":
    main()
