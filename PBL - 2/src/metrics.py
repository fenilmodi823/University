import base64
from math import log2


def avalanche_effect(original: str, modified: str) -> float:
    """Compute percentage of bit-flips between two bitstrings."""
    assert len(original) == len(modified)
    flips = sum(o != m for o, m in zip(original, modified))
    return flips / len(original) * 100


def ciphertext_avalanche(key_bits: str, plaintext: str, encrypt_func) -> float:
    """Measure avalanche effect on ciphertext by flipping the first bit of the key."""
    # Original ciphertext
    data1 = base64.b64decode(encrypt_func(plaintext, key_bits)['ciphertext'])
    # Flip the first key bit
    flipped_key = ('1' if key_bits[0] == '0' else '0') + key_bits[1:]
    data2 = base64.b64decode(encrypt_func(plaintext, flipped_key)['ciphertext'])
    # Convert to bitstrings
    b1 = ''.join(f'{byte:08b}' for byte in data1)
    b2 = ''.join(f'{byte:08b}' for byte in data2)
    length = min(len(b1), len(b2))
    flips = sum(x != y for x, y in zip(b1, b2))
    return flips / length * 100


def compute_throughput(bytes_processed: int, seconds: float) -> float:
    """Return throughput in bytes/sec."""
    return bytes_processed / seconds


def chi_square_test(bitstring: str) -> float:
    """Perform a chi-square test for randomness on a bitstring."""
    n = len(bitstring)
    count0 = bitstring.count('0')
    count1 = bitstring.count('1')
    expected = n / 2
    return ((count0 - expected) ** 2 / expected) + ((count1 - expected) ** 2 / expected)