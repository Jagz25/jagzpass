import os
import json
import base64
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from argon2.low_level import hash_secret_raw, Type


VAULT_DIR = os.path.join(os.path.expanduser("~"), ".jagzpass", "vaults")

def ensure_secure_vault_dir():
    # Create the vault directory if it doesn't exist, with owner only access
    if not os.path.exists(VAULT_DIR):
        os.makedirs(VAULT_DIR, mode=0o700, exist_ok=True)
    os.chmod(VAULT_DIR, 0o700) 

class Vault:
    def __init__(self, username, vault_location=VAULT_DIR):
        ensure_secure_vault_dir()
        self.username = username
        self.file = os.path.join(vault_location, f"vault_{username}.enc")

    def exists(self):
        return os.path.exists(self.file)

    def _derive_key(self, password: str, salt: bytes):
        return hash_secret_raw(
            secret=password.encode(),
            salt=salt,
            time_cost=3,
            memory_cost=65536,
            parallelism=2,
            hash_len=32,
            type=Type.ID
        )

    def encrypt(self, data: dict, password: str):
        salt = os.urandom(16)
        key = self._derive_key(password, salt)
        aesgcm = AESGCM(key)
        nonce = os.urandom(12)
        ciphertext = aesgcm.encrypt(nonce, json.dumps(data).encode(), None)
        blob = base64.b64encode(salt + nonce + ciphertext)
        with open(self.file, "wb") as f:
            f.write(blob)
        os.chmod(self.file, 0o600)  # Owner can read/write, others cannot

    def decrypt(self, password: str) -> dict:
        try:
            with open(self.file, "rb") as f:
                blob = base64.b64decode(f.read())
            salt, nonce, ciphertext = blob[:16], blob[16:28], blob[28:]
            key = self._derive_key(password, salt)
            aesgcm = AESGCM(key)
            plaintext = aesgcm.decrypt(nonce, ciphertext, None)
            return json.loads(plaintext)
        except Exception as e:
            raise ValueError("Incorrect password or corrupt vault") from e
