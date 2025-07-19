from PasswordManager import Vault, UserInterface, Authenticator, SessionManager
import os

VAULT_DIR = "./Vaults"

if __name__ == "__main__":
    ui = UserInterface()
    auth = Authenticator(ui.console)
    session = SessionManager(ui, VAULT_DIR)

    while True:
        choice = ui.prompt_main_menu()

        if choice == "1":  # Login
            username = ui.input("Enter your username: ")
            vault = Vault(username, VAULT_DIR)

            if not vault.exists():
                ui.print("[red]Vault not found.[/red]")
                continue

            data, pwd = auth.authenticate(vault)
            if data is not None:
                session.run(data, pwd, username)
        
        elif choice == "2":  # Create New User
            username = ui.input("Choose a username: ")
            vault = Vault(username, VAULT_DIR)

            if vault.exists():
                ui.print("[red]User already exists.[/red]")
                continue

            data, pwd = auth.create_user(vault)
            session.run(data, pwd, username)

        elif choice == "3":  # Exit
            break

        else:
            ui.print("[red]Invalid option[/red]")
