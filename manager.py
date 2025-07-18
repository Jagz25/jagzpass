import os
import json
import base64
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from argon2.low_level import hash_secret_raw, Type


def get_vault_file(username: str) -> str:
    return f"vault_{username}.enc"

def derive_key(password: str, salt: bytes) -> bytes:
    return hash_secret_raw(
        secret=password.encode(),
        salt=salt,
        time_cost=3,
        memory_cost=65536,
        parallelism=2,
        hash_len=32,
        type=Type.ID
    )

def encrypt_vault(data: dict, password: str, username: str) -> None:
    salt = os.urandom(16)
    key = derive_key(password, salt)
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)
    ciphertext = aesgcm.encrypt(nonce, json.dumps(data).encode(), None)

    blob = base64.b64encode(salt + nonce + ciphertext)
    with open(get_vault_file(username), 'wb') as f:
        f.write(blob)

def decrypt_vault(password: str, username: str) -> dict:
    try:
        with open(get_vault_file(username), 'rb') as f:
            blob = base64.b64decode(f.read())

        salt = blob[:16]
        nonce = blob[16:28]
        ciphertext = blob[28:]
        key = derive_key(password, salt)
        aesgcm = AESGCM(key)
        plaintext = aesgcm.decrypt(nonce, ciphertext, None)
        return json.loads(plaintext)
    except Exception as e:
        raise ValueError("Incorrect password or corrupt vault") from e

def vault_exists(username: str) -> bool:
    return os.path.exists(get_vault_file(username))

def add_credential(vault: dict, site: str, username: str, password: str) -> dict:
    vault[site.lower()] = {"username": username, "password": password}
    return vault

def search_site(vault: dict, query: str) -> str:
    from difflib import get_close_matches
    matches = get_close_matches(query.lower(), vault.keys(), n=1, cutoff=0.6)
    return matches[0] if matches else None
