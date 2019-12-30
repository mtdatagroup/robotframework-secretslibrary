import os
from typing import Tuple

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

PRIVATE_KEY_FILE_NAME = "testdata/asymmetric/private_key.pem"
PUBLIC_KEY_FILE_NAME = "testdata/asymmetric/public_key.pem"
SYMMETRIC_KEY_FILE_NAME = "testdata/symmetric/symmetric_key.key"


def _write(key: bytes, file_name: str) -> None:
    with open(file_name, 'wb') as f:
        f.write(key)


def generate_asymmetric_keys() -> None:

    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )

    public_key = private_key.public_key()

    _pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    _write(_pem, PRIVATE_KEY_FILE_NAME)

    _pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    _write(_pem, PUBLIC_KEY_FILE_NAME)


def generate_symmetric_key() -> None:
    _write(Fernet.generate_key(), SYMMETRIC_KEY_FILE_NAME)


if __name__ == '__main__':
    generate_symmetric_key()
    generate_asymmetric_keys()
