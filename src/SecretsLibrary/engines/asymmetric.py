import os

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from . import SecretsEngine


class Asymmetric(SecretsEngine):

    def __init__(self, private_key_path: str = None, public_key_path: str = None, password: str = None):

        self._private_key, self._public_key = None, None

        if private_key_path and public_key_path:
            self.read_keys(private_key_path, public_key_path, password)

    @property
    def public_key(self):
        if self._public_key is None:
            raise RuntimeError("No public key has been setup yet")
        return self._public_key

    @property
    def private_key(self):
        if self._private_key is None:
            raise RuntimeError("No private key has been setup yet")
        return self._private_key

    def encrypt(self, plain_text: str) -> bytes:

        return self.public_key.encrypt(
            str.encode(plain_text),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

    def decrypt(self, cipher_text: bytes) -> str:

        return self.private_key.decrypt(
            cipher_text,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

    def read_keys(self, private_key_path: str, public_key_path: str, password: str = None) -> None:

        if os.path.exists(private_key_path):

            with open(private_key_path, "rb") as key_file:
                self._private_key = serialization.load_pem_private_key(
                    key_file.read(),
                    password=password,
                    backend=default_backend()
                )

        if os.path.exists(public_key_path):

            with open(public_key_path, "rb") as key_file:
                self._public_key = serialization.load_pem_public_key(
                    key_file.read(),
                    backend=default_backend()
                )
