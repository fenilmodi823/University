# – AES wrapper that pulls key bits from qrw_generator.py

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from base64 import b64encode, b64decode
from qrw_generator import generate_qrw_bits


def quantum_key_to_bytes(bitstring: str) -> bytes:
    """
    Convert a binary string (e.g., 128 bits) into bytes for AES key.
    """
    return int(bitstring, 2).to_bytes(len(bitstring) // 8, byteorder='big')


def encrypt_with_aes(plaintext: str, key_bits: str) -> dict:
    """
    Encrypts plaintext using AES-CBC with a quantum-generated key.
    Returns a dict containing:
      - 'ciphertext': base64-encoded IV + ciphertext
      - 'iv': hex-encoded IV for display
    """
    key = quantum_key_to_bytes(key_bits)
    cipher = AES.new(key, AES.MODE_CBC)
    iv = cipher.iv
    padded = pad(plaintext.encode('utf-8'), AES.block_size)
    ciphertext = cipher.encrypt(padded)
    return {
        'ciphertext': b64encode(iv + ciphertext).decode('utf-8'),
        'iv': iv.hex()
    }


def decrypt_with_aes(ciphertext_b64: str, key_bits: str) -> str:
    """
    Decrypts base64-encoded IV + ciphertext using AES-CBC with the given quantum key.
    Returns the decrypted plaintext string.
    """
    key = quantum_key_to_bytes(key_bits)
    data = b64decode(ciphertext_b64)
    iv = data[:AES.block_size]
    ciphertext = data[AES.block_size:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return plaintext.decode('utf-8')


if __name__ == '__main__':
    # Demo
    key_bits = generate_qrw_bits(128)
    print(f"Quantum Key (128 bits): {key_bits}")
    message = "Cyber Security is evolving!"
    enc = encrypt_with_aes(message, key_bits)
    print(f"Plaintext: {message}")
    print(f"Encrypted (base64): {enc['ciphertext']}")
    dec = decrypt_with_aes(enc['ciphertext'], key_bits)
    print(f"Decrypted: {dec}")
