# Authenticator.py
import getpass

import pyperclip
from PasswordGenerator.Generator import check_password_strength, generate_strong_password
from PasswordManager.Lockout import LockoutHandler

class Authenticator:
    def __init__(self, console):
        self.console = console
        self.lock_handler = LockoutHandler(max_attempts=5, duration=60)

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
        self.console.print(
            "[bold]Create a strong master password.[/bold]\n"
            "[cyan]Tips to get [green]strong[/green] strength:[/cyan]\n"
            "- At least 8 characters\n"
            "- Mix of uppercase and lowercase letters\n"
            "- Include numbers\n"
            "- Include symbols"
        )

        while True:
            password = getpass.getpass("Set master password for new vault: ")
            strength, color = check_password_strength(password)
            self.console.print(f"Password strength: [{color}]{strength}[/{color}]")

            if strength != "strong":
                self.console.print("[red]Master password must be strong. Try again.[/red]")
                continue

            confirm = getpass.getpass("Confirm master password: ")
            if password != confirm:
                self.console.print("[red]Passwords do not match. Try again.[/red]")
                continue

            break

        vault.encrypt({}, password)
        self.console.print("[green]New vault created![/green]")
        return {}, password