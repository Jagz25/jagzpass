# JagzPass

**JagzPass** is a local, offline-first password manager built in Python. It securely stores your credentials in an encrypted vault file, protected by a master password using modern cryptographic practices.



## 🚀 Features

- AES-GCM authenticated encryption to keep your passwords confidential.
- Argon2id Key Derivation Function (KDF) with strong, tunable parameters.
- CLI-based interface with real-time password strength feedback (color-coded).
- Lockout mechanism with rollback protection (monotonic time + UTC API).
- Strong password generator.
- Detection of reused or common passwords using NCSC's top 100k list.
- No plaintext ever stored on disk, vaults are encrypted end-to-end.


## ⚙️ KDF Configuration (Advanced)

JagzPass uses **Argon2id**, a modern, memory-hard Key Derivation Function (KDF) to derive encryption keys from your master password. Its parameters: time cost, memory cost, and parallelism are already set to values that exceed OWASP’s minimum recommendations while keeping login times reasonable.

**You can modify these parameters** in `Vault.py`, but doing so may make your vault:
- **Incompatible** with older versions of JagzPass. You won't be able to unlock vaults that were made with different Argon2id configurations.
- **More vulnerable** if lowered too far.
- **Slower** on low-end systems if set too high

Only change these settings if you understand the trade-offs between security and performance.

## 🛠️ Project Structure

| File | Description |
|------|-------------|
| `main.py` | Entry point for the CLI application |
| `Vault.py` | Handles encryption, decryption, and key derivation (**KDF parameters can be modified here**) |
| `CredentialManager.py` | Manages credentials in memory |
| `Authenticator.py` | Creates and authenticates users |
| `Lockout.py` | Handles login attempt limits and time spoofing protection |
| `SessionManager.py` | Controls the main CLI flow after login |
| `UserInterface.py` | Rich-based console interface |
| `Generator.py` | Password generation and strength checking |
| `100k-most-used-passwords-NCSC.txt` | Dictionary blacklist for weak password detection |
| `requirements.txt` | Python package dependencies |



## 📦 Installation

### 🐧 For Linux Users

You can download the prebuilt binary directly from the [`dist/`](./dist/) folder:

```bash
cd dist
chmod +x jagzpass
./jagzpass
```

This executable was built with PyInstaller and contains all dependencies.



### 🪟🍎 For Windows and macOS

You can run JagzPass manually using Python:

1. Clone the repo:
   ```bash
   git clone https://github.com/yourusername/jagzpass.git
   cd jagzpass
   ```

2. (Optional) Set up a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the program:
   ```bash
   python main.py
   ```

Feel free to build your own executable using [PyInstaller](https://pyinstaller.org/en/stable/) or any method you prefer.
