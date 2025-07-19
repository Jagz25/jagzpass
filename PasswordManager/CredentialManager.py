from difflib import get_close_matches

class CredentialManager:
    def __init__(self, vault_data: dict):
        self.vault_data = vault_data

    def add(self, site: str, username: str, password: str):
        self.vault_data[site.lower()] = {"username": username, "password": password}

    def search(self, query: str):
        matches = get_close_matches(query.lower(), self.vault_data.keys(), n=1, cutoff=0.6)
        return matches[0] if matches else None

    def get(self, site: str):
        return self.vault_data.get(site.lower())
        
    def password_already_used(self, new_password: str) -> bool:
        return any(entry["password"] == new_password for entry in self.vault_data.values())
