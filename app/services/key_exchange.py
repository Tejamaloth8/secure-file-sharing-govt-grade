from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization

def encrypt_aes_key(public_key_pem: bytes, aes_key: bytes) -> bytes:
    public_key = serialization.load_pem_public_key(public_key_pem)

    return public_key.encrypt(
        aes_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

def decrypt_aes_key(private_key_pem: bytes, encrypted_key: bytes) -> bytes:
    private_key = serialization.load_pem_private_key(
        private_key_pem,
        password=None
    )

    return private_key.decrypt(
        encrypted_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
