# SessionManager.py
import getpass
import pyperclip
from PasswordManager.CredentialManager import CredentialManager
from PasswordManager.Vault import Vault

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
                pwd = getpass.getpass("Password: ")
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
                            self.console.print("[bold]What do you want to do?[/bold]")
                            self.console.print("[blue]1.[/blue] Show password")
                            self.console.print("[blue]2.[/blue] Copy password to clipboard")
                            action = self.console.input("Choose: ")
                            if action == "1":
                                self.console.print(f"Password: {cred['password']}")
                            elif action == "2":
                                pyperclip.copy(cred['password'])
                                self.console.print("[green]Password copied to clipboard.[/green]")
                            else:
                                self.console.print("[red]Invalid option.[/red]")
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
