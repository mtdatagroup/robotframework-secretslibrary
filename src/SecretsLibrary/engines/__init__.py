class SecretsEngine:

    def encrypt(self, plain_text: str) -> bytes:
        raise NotImplementedError

    def decrypt(self, cipher_text: bytes) -> str:
        raise NotImplementedError

    def __str__(self) -> str:
        return self.__class__.__name__
