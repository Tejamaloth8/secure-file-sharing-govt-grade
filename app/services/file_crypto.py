from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os

def generate_aes_key():
    return AESGCM.generate_key(bit_length=256)

def encrypt_file(data: bytes, key: bytes):
    aes = AESGCM(key)
    nonce = os.urandom(12)
    return nonce + aes.encrypt(nonce, data, None)

def decrypt_file(data: bytes, key: bytes):
    aes = AESGCM(key)
    return aes.decrypt(data[:12], data[12:], None)
