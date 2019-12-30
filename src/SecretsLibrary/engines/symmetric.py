import os

import cryptography
from cryptography.fernet import Fernet
from . import SecretsEngine


class Symmetric(SecretsEngine):

    def __init__(self, symmetric_key_path: str = None) -> None:

        self._asymmetric_key = None

        if symmetric_key_path:
            self.read_key(symmetric_key_path)

    @property
    def symmetric_key(self):
        if self._asymmetric_key is None:
            raise RuntimeError("No symmetric key has been setup")
        return self._asymmetric_key

    def read_key(self, key_file_path: str) -> None:

        if os.path.exists(key_file_path):

            with open(key_file_path) as file:
                self._asymmetric_key = file.read()

    def encrypt(self, plain_text: str) -> bytes:
        return Fernet(self.symmetric_key).encrypt(str.encode(plain_text))

    def decrypt(self, cipher_text: bytes) -> str:

        try:

            if isinstance(cipher_text, str):
                return Fernet(self.symmetric_key).decrypt(str.encode(cipher_text))
            return Fernet(self.symmetric_key).decrypt(cipher_text)

        except (cryptography.exceptions.InvalidSignature, cryptography.fernet.InvalidToken):
            raise
