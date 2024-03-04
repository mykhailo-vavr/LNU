import hashlib
import random

#################################
#
#           Helpers
#
#################################


def get_random_number(min_val, max_val):
    return random.randint(min_val, max_val)


def mod(a, b):
    c = a % b

    if c < 0:
        return c + b
    return c


def mod_pow(base, exponent, m):
    if m == 1:
        return 0

    a = base % m
    e = exponent
    result = 1

    while e > 0:
        if e % 2 == 1:
            result = (result * a) % m

        e //= 2
        a = (a * a) % m

    return result


def mod_inv(a, m):
    for i in range(1, m):
        if (a * i) % m == 1:
            return i
    return -1


def calculate_hash(data):
    hash_object = hashlib.sha256()
    hash_object.update(data.encode("utf-8"))

    hash_value = int(hash_object.hexdigest(), 16)

    return hash_value


def gcd(a, b):
    return gcd(b, a % b) if b else a


def is_prime(num):
    if num == 2 or num == 3:
        return True
    if num <= 1 or num % 2 == 0 or num % 3 == 0:
        return False

    i = 5
    while i * i <= num:
        if num % i == 0 or num % (i + 2) == 0:
            return False
        i += 6

    return True


def is_coprime(a, b):
    return gcd(a, b) == 1


def get_coprime(num):
    for i in range(2, num):
        if is_coprime(num, i):
            return i
    return 1


def get_random_prime_number(min_val=0, max_val=100):
    num = 1

    while not is_prime(num):
        num = random.randint(min_val, max_val)

    return num


#################################
#
#        Main functions
#
#################################


def get_keys():
    p = get_random_prime_number()
    g = get_random_number(1, p)
    x = random.randint(1, p - 2)  # 1 < x < p

    print(f"p: {x}; g: {g}; x: {x}")

    y = mod_pow(g, x, p)

    return ((p, g, y), (p, g, x))


def sign(msg, p, g, x):
    m = calculate_hash(msg)

    k = get_random_number(1 + 1, p - 1 - 1)  # 1 < k < p - 1

    r = mod_pow(g, k, p)
    s = mod((m - x * r) * mod_inv(k, p - 1), p - 1)

    return (r, s)


def verify(msg, p, g, y, r, s):
    m = calculate_hash(msg)

    left = mod(mod_pow(y, r, p) * mod_pow(r, s, p), p)
    right = mod_pow(g, m, p)

    print(left, right)

    verified = left == right
    return verified


#################################
#
#       Test Elgamal sign
#
#################################


public_key, private_key = get_keys()

p, g, y = public_key
p, g, x = private_key

with open("public.txt", "w") as file:
    file.write("#".join([str(p), str(g), str(y)]))

with open("private.txt", "w") as file:
    file.write("#".join([str(p), str(g), str(x)]))

with open("text.txt", "r") as text_file:
    msg = text_file.read()

r, s = sign(msg, p, g, x)

with open("signed.txt", "w") as signed_file:
    signed_file.write("#".join([msg, str(r), str(s)]))

with open("signed.txt", "r") as read_signed_file:
    signed_msg = read_signed_file.read().split("#")

r = int(signed_msg[1])
s = int(signed_msg[2])

verified = verify(msg, p, g, y, r, s)


print("Signed verified:", verified)
