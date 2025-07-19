# SessionManager.py
import getpass
import pyperclip
import re
from rich.console import Console

from PasswordManager.CredentialManager import CredentialManager
from PasswordManager.Vault import Vault
from PasswordGenerator import check_password_strength, generate_strong_password

class SessionManager:
    def __init__(self, console, vault_location):
        self.console = console
        self.vault_location = vault_location

    def run(self, vault_data, password, username):
        cm = CredentialManager(vault_data)
        vault = Vault(username, self.vault_location)

        while True:
            self.console.print("\n[bold blue]1.[/bold blue] Add Credential")
            self.console.print("[bold blue]2.[/bold blue] Retrieve Credential")
            self.console.print("[bold blue]3.[/bold blue] Logout")
            self.console.print("[bold blue]4.[/bold blue] Exit")
            choice = self.console.input("[bold cyan]Select an option:[/bold cyan] ")

            if choice == "1":
                site = self.console.input("Site name: ")
                uname = self.console.input("Username: ")

                use_gen = self.console.input("Generate strong password? (y/n): ").lower()
                if use_gen == "y":
                    pwd = generate_strong_password()
                    pyperclip.copy(pwd)
                    self.console.print("[green]Password generated and copied to clipboard.[/green]")
                else:
                    while True:
                        pwd = getpass.getpass("Enter your password: ")

                        if cm.password_already_used(pwd):
                            self.console.print("[red]This password was already used. Try a new one.[/red]")
                            continue

                        strength, color = check_password_strength(pwd)
                        self.console.print(f"Password strength: [{color}]{strength}[/{color}]")

                        confirm = self.console.input("Use this password? (y/n): ").lower()
                        if confirm == "y":
                            pyperclip.copy(pwd)
                            self.console.print("[green]Password copied to clipboard.[/green]")
                            break

                cm.add(site, uname, pwd)
                vault.encrypt(cm.vault_data, password)
                self.console.print("[green]Credential added and saved.[/green]")

            elif choice == "2":
                query = self.console.input("Search site: ")
                match = cm.search(query)
                if match:
                    confirm = self.console.input(f"Did you mean [yellow]{match}[/yellow]? (y/n): ")
                    if confirm.lower() == "y":
                        cred = cm.get(match)
                        if cred:
                            self.console.print(f"Username: {cred.get('username', '[red]Not Found[/red]')}")
                            pyperclip.copy(cred['password'])
                            self.console.print("[green]Password copied to clipboard.[/green]")
                    else:
                        self.console.print("[red]No matching site confirmed.[/red]")
                else:
                    self.console.print("[red]No close match found.[/red]")

            elif choice == "3":
                self.console.print("[blue]Logging out...[/blue]")
                break

            elif choice == "4":
                self.console.print("[blue]Exiting...[/blue]")
                exit()
            else:
                self.console.print("[red]Invalid option.[/red]")
