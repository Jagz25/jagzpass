# Authenticator.py
import getpass
from PasswordManager.Lockout import LockoutHandler

class Authenticator:
    def __init__(self, console):
        self.console = console
        self.lock_handler = LockoutHandler()

    def authenticate(self, vault):
        attempts = 0
        locked_seconds = self.lock_handler.is_locked()
        if locked_seconds:
            self.lock_handler.show_timer(locked_seconds)
            return None, None

        while attempts < self.lock_handler.max_attempts:
            password = getpass.getpass("Enter master password: ")
            try:
                data = vault.decrypt(password)
                self.console.print(f"[green]Vault unlocked for user: {vault.username}![/green]")
                return data, password
            except ValueError:
                attempts += 1
                self.console.print(f"[red]Incorrect password. Attempts left: {self.lock_handler.max_attempts - attempts}[/red]")

        self.lock_handler.lock()
        self.lock_handler.show_timer(self.lock_handler.duration)
        return None, None

    def create_user(self, vault):
        password = getpass.getpass("Set master password for new vault: ")
        vault.encrypt({}, password)
        self.console.print("[green]New vault created![/green]")
        return {}, password
