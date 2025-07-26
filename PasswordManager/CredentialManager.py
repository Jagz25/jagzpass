from difflib import get_close_matches

class CredentialManager:
    def __init__(self, vault_data: dict):
        # vault_data is a dictionary of credentials loaded from the vault
        # Format: { "site": { "username": ..., "password": ... } }
        self.vault_data = vault_data

    # Adds a new credential to the vault (overwrites if site already exists)
    def add(self, site: str, username: str, password: str):
        self.vault_data[site.lower()] = {"username": username, "password": password}
        
    # Performs a fuzzy search to find the closest matching site name
    def search(self, query: str):
        matches = get_close_matches(query.lower(), self.vault_data.keys(), n=1, cutoff=0.6)
        return matches[0] if matches else None

    # Retrieves stored credentials for a given site
    def get(self, site: str):
        return self.vault_data.get(site.lower())
    
    # Checks if a given password is already used in any saved credential
    def password_already_used(self, new_password: str) -> bool:
        return any(entry["password"] == new_password for entry in self.vault_data.values())
