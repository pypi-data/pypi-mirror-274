from typing import Any
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP


class AsymmetricEncryption:
    def __init__(self):
        """
        Initialize the AsymmetricEncryption class by generating a new RSA key pair and creating a cipher object for encryption and decryption.
        """
        self.key = RSA.generate(2048)
        self.cipher = PKCS1_OAEP.new(self.key)

    def get_public_key(self):
        """
        Get the public key in PEM format.

        Returns:
        bytes: Public key in PEM format
        """
        return self.key.publickey().export_key()

    def get_private_key(self):
        """
        Get the private key in PEM format.

        Returns:
        bytes: Private key in PEM format
        """
        return self.key.export_key()

    def encrypt_message(self, message: Any) -> bytes:
        """
        Encrypt a message using the public key.

        Args:
        bytes: Message to be encrypted

        Returns:
        bytes: Encrypted message
        """
        encrypted_message = self.cipher.encrypt(message)
        return encrypted_message

    def decrypt_message(self, encrypted_message: bytes) -> bytes:
        """
        Decrypt an encrypted message using the private key.

        Args:
        bytes: Encrypted message

        Returns:
        bytes: Decrypted message
        """
        decrypted_message = self.cipher.decrypt(encrypted_message)
        return decrypted_message
