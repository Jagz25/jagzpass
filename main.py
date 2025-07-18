from PasswordManager import Vault, UserInterface, Authenticator, SessionManager
import os

VAULT_DIR = "./Vaults"

if __name__ == "__main__":
    ui = UserInterface()
    auth = Authenticator(ui.console)
    session = SessionManager(ui, VAULT_DIR)

    while True:
        choice = ui.prompt_main_menu()

        if choice == "1":
            username = ui.console.input("Enter your username: ")
            vault = Vault(username, VAULT_DIR)
            if not vault.exists():
                ui.console.print("[red]No vault found for this user.[/red]")
                continue
            data, pwd = auth.authenticate(vault)

        elif choice == "2":
            username = ui.console.input("Choose a username: ")
            vault = Vault(username, VAULT_DIR)
            if vault.exists():
                ui.console.print("[red]User already exists.[/red]")
                continue
            data, pwd = auth.create_user(vault)

        elif choice == "3":
            ui.console.print("[blue]Exiting...[/blue]")
            break

        else:
            ui.console.print("[red]Invalid choice.[/red]")
            continue

        if data:
            session.run(data, pwd, username)
