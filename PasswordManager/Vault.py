import os
import json
import base64
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from argon2.low_level import hash_secret_raw, Type

class Vault:
    def __init__(self, username, vault_location=None):
        # Always use ./Vaults directory relative to current working dir
        # This ensures consistent vault location across compiled and uncompiled versions
        vault_location = os.path.abspath("Vaults")

        # Create vault directory if it doesn't exist
        if not os.path.exists(vault_location):
            os.makedirs(vault_location)

        self.username = username
        self.file = os.path.join(vault_location, f"vault_{username}.enc")

    # Check if the vault file already exists for this user
    def exists(self):
        return os.path.exists(self.file)

    # Derives a 256-bit encryption key from the master password using Argon2id
    def _derive_key(self, password: str, salt: bytes):
        return hash_secret_raw(
            secret=password.encode(),
            salt=salt,
            time_cost=3,        # ⬅️ MODIFY this to increase/decrease KDF time cost
            memory_cost=65536,  # ⬅️ MODIFY this (in KiB). 65536 KiB = 64 MiB
            parallelism=2,      # ⬅️ MODIFY this for thread-level parallelism
            hash_len=32,       
            type=Type.ID       
        )

    # Encrypts the vault data using AES-GCM and writes it to file
    def encrypt(self, data: dict, password: str):
        salt = os.urandom(16)              # Fresh salt for each encryption
        key = self._derive_key(password, salt)
        aesgcm = AESGCM(key)

        nonce = os.urandom(12)             # AES-GCM standard nonce length
        plaintext = json.dumps(data).encode()
        ciphertext = aesgcm.encrypt(nonce, plaintext, None)

        # Save blob as [salt][nonce][ciphertext+tag], base64-encoded
        blob = base64.b64encode(salt + nonce + ciphertext)
        with open(self.file, "wb") as f:
            f.write(blob)

    # Decrypts the vault file using the provided password
    def decrypt(self, password: str) -> dict:
        try:
            with open(self.file, "rb") as f:
                blob = base64.b64decode(f.read())

            # Split into components: first 16B = salt, next 12B = nonce, rest = ciphertext+tag
            salt, nonce, ciphertext = blob[:16], blob[16:28], blob[28:]
            key = self._derive_key(password, salt)
            aesgcm = AESGCM(key)

            plaintext = aesgcm.decrypt(nonce, ciphertext, None)
            return json.loads(plaintext)

        except Exception as e:
            # Handles incorrect password or tampered/corrupt vault
            raise ValueError("Incorrect password or corrupt vault") from e
