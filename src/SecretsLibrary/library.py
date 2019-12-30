from typing import Any, List, Tuple

from robot.api import logger
from robot.api.deco import keyword

from .engines import SecretsEngine
from .engines.asymmetric import Asymmetric
from .engines.symmetric import Symmetric
from .version import VERSION

__version__ = VERSION


class SecretsLibrary:
    """SecretsLibrary is a Robot Framework test library for Secrets Management

    For information regarding installation and support, please visit
    [https://github.com/mpstella/robotframework-secretslibrary|project page]

    The library has the following main usages:
    - Encrypt variables/files via Symmetric Algorithm (Fernet) or Asymmetric Algorithm (RSA)
    - Decrypt variables/files via Symmetric Algorithm (Fernet) or Asymmetric Algorithm (RSA)

    == Table of contents ==
    - `Understanding the algorithms`

    = Understanding the algorithms =

    SecretsLibrary supports multiple Algorithms at the same time, namely

    === Asymmetric Algorithms via RSA ===

    This is a type of encryption where a pair of keys, one public and one private, is used to encrypt and decrypt messages.

    === Symmetric Algorithms via Fernet ===

    This is a type of encryption where only one key is used to both encrypt and decrypt information.

    """

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = __version__

    def __init__(self):
        self._engines = {}
        self._current_engine = None
        self._engine = None

    @property
    def current_engine(self) -> SecretsEngine:
        if self._current_engine is None:
            raise RuntimeError("No secrets engine has been configured")
        return self._current_engine

    @keyword
    def list_engines(self) -> List[str]:
        """Returns the name of all the currently registered encryption engines"""
        return list(self._engines.keys())

    @keyword
    def current_engine_name(self) -> str:
        """Return the name of the current active encryption engine"""
        for k, v in self._engines:
            if v == self._current_engine:
                return k
        return None

    @keyword(types={"name": str})
    def switch_engine(self, name: str) -> None:
        """Switches the active engine by registered name"""
        if name not in self._engines:
            raise RuntimeError(f"No registered engines exist with name: {name}")
        self._current_engine = self._engines[name]

    @keyword(types={"name": str, "private_key_path": str, "public_key_path": str})
    def add_asymmetric_engine(self, name: str, private_key_path: str, public_key_path: str) -> None:
        """Adds a new Asymmetric Engine to the engines cache

        You will need to pass in the paths of both the private key and public key to initialise the engine

        Example:
        | Add Asymmetric Engine | RSA | ${CURDIR}${/}private_key.pem | ${CURDIR}${/}public_key.pem |
        """
        logger.info("Configuring Secrets library to use Asymmetric Engine")
        self._engines[name] = Asymmetric(private_key_path, public_key_path)
        self._current_engine = self._engines[name]

    @keyword(types={"name": str, "key_path": str})
    def add_symmetric_engine(self, name: str, key_path: str) -> None:
        """Adds a new Symmetric Engine to the engines cache

        You will need to pass in the path of the symmetric key to initialise the engine

        Example:
        | Add Symmetric Engine | Fernet | ${CURDIR}${/}fernet_key.key |
        """
        logger.info("Configuring Secrets library to use Symmetric Engine")
        self._engines[name] = Symmetric(key_path)
        self._current_engine = self._engines[name]

    @keyword(types={"file_path": str})
    def decrypt_from_file(self, file_path: str) -> Any:
        """Open a file and decrypt the contents, returning the decrypted text"""
        with open(file_path, "rb") as file:
            return self.current_engine.decrypt(file.read())

    @keyword(types={"plain_text": str, "file_path": str})
    def encrypt_to_file(self, plain_text: str, file_path: str) -> None:
        """Encrypt input and write out to file"""
        with open(file_path, "wb") as file:
            file.write(self.current_engine.encrypt(plain_text))

    @keyword(types={"file_path": str})
    def encrypt_file(self, file_path: str) -> bytes:
        """Encrypt a file and return encrypted contents"""
        with open(file_path, "r") as file:
            return self.current_engine.encrypt(file.read())

    @keyword(types=None)
    def decrypt(self, cypher_text: Any) -> Any:
        """Decrypt encrypted data and return decrypted contents"""
        return self.current_engine.decrypt(cypher_text)

    @keyword(types=None)
    def encrypt(self, plain_text) -> bytes:
        """Encrypt input and return encrypted contents"""
        return self.current_engine.encrypt(plain_text)
