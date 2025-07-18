# main.py
import time
import getpass
import pyperclip
from rich.console import Console
from rich.progress import Progress, BarColumn, TimeRemainingColumn
import manager

MAX_ATTEMPTS = 10
LOCKOUT_DURATION = 5 * 60  # 5 minutes
LOCK_FILE = ".lock"

console = Console()

def show_lockdown_timer(seconds: int):
    console.print(f"[red]Too many incorrect attempts. Locked for {seconds // 60} minutes.[/red]")
    with Progress("[progress.description]{task.description}",
                  BarColumn(),
                  TimeRemainingColumn(),
                  transient=True) as progress:
        task = progress.add_task("Locking down...", total=seconds)
        for _ in range(seconds):
            time.sleep(1)
            progress.update(task, advance=1)

def load_vault_with_attempts(username: str):
    attempts = 0
    vault_file = manager.get_vault_file(username)

    if manager.vault_exists(username):
        if LOCK_FILE in manager.os.listdir():
            with open(LOCK_FILE, "r") as f:
                lock_time = float(f.read())
            if time.time() < lock_time:
                remaining = int(lock_time - time.time())
                show_lockdown_timer(remaining)
                return None, None
            else:
                manager.os.remove(LOCK_FILE)

        while attempts < MAX_ATTEMPTS:
            password = getpass.getpass("Enter master password: ")
            try:
                vault = manager.decrypt_vault(password, username)
                console.print(f"[green]Vault unlocked for user: {username}![/green]")
                return vault, password
            except ValueError:
                attempts += 1
                console.print(f"[red]Incorrect password. Attempts left: {MAX_ATTEMPTS - attempts}[/red]")

        with open(LOCK_FILE, "w") as f:
            f.write(str(time.time() + LOCKOUT_DURATION))
        show_lockdown_timer(LOCKOUT_DURATION)
        return None, None

    return None, None

def create_user_flow(username: str):
    password = getpass.getpass("Set master password for new vault: ")
    manager.encrypt_vault({}, password, username)
    console.print("[green]New vault created![/green]")
    return {}, password

def list_existing_users():
    return [f.split("_")[1].split(".")[0] for f in manager.os.listdir() if f.startswith("vault_") and f.endswith(".enc")]

def menu(vault: dict, password: str, username: str):
    while True:
        console.print("\n[bold blue]1.[/bold blue] Add Credential")
        console.print("[bold blue]2.[/bold blue] Retrieve Credential")
        console.print("[bold blue]3.[/bold blue] Logout")
        console.print("[bold blue]4.[/bold blue] Exit")
        choice = console.input("[bold cyan]Select an option:[/bold cyan] ")

        if choice == "1":
            site = console.input("Site name: ")
            uname = console.input("Username: ")
            pwd = getpass.getpass("Password: ")
            vault = manager.add_credential(vault, site, uname, pwd)
            manager.encrypt_vault(vault, password, username)
            console.print("[green]Credential added and saved.[/green]")

        elif choice == "2":
            query = console.input("Search site: ")
            match = manager.search_site(vault, query)
            if match:
                confirm = console.input(f"Did you mean [yellow]{match}[/yellow]? (y/n): ")
                if confirm.lower() == "y":
                    cred = vault[match]
                    if isinstance(cred, dict):
                        username_val = cred.get("username")
                        if username_val:
                            console.print(f"Username: {username_val}")
                        else:
                            console.print("[red]Username not found for this credential.[/red]")
                        console.print("[bold]What do you want to do?[/bold]")
                        console.print("[blue]1.[/blue] Show password")
                        console.print("[blue]2.[/blue] Copy password to clipboard")
                        action = console.input("Choose: ")
                        if action == "1":
                            console.print(f"Username: {username_val}")
                            console.print(f"Password: {cred['password']}")
                        elif action == "2":
                            pyperclip.copy(cred['password'])
                            console.print("[green]Password copied to clipboard.[/green]")
                        else:
                            console.print("[red]Invalid option.[/red]")
                    else:
                        console.print("[red]Invalid credential format.[/red]")
                else:
                    console.print("[red]No matching site confirmed.[/red]")
            else:
                console.print("[red]No close match found.[/red]")

        elif choice == "3":
            console.print("[blue]Logging out...[/blue]")
            return

        elif choice == "4":
            console.print("[blue]Exiting...[/blue]")
            exit()

        else:
            console.print("[red]Invalid option.[/red]")

if __name__ == "__main__":
    while True:
        console.print("[bold]Welcome to JagzPass Password Manager[/bold]")
        console.print("[blue]1.[/blue] Login")
        console.print("[blue]2.[/blue] Create New User")
        console.print("[blue]3.[/blue] Exit")
        choice = console.input("[bold cyan]Select an option:[/bold cyan] ")

        if choice == "1":
            username = console.input("Enter your username: ")
            if not manager.vault_exists(username):
                console.print("[red]No vault found for this user.[/red]")
                continue
            vault_data, master_password = load_vault_with_attempts(username)
        elif choice == "2":
            username = console.input("Choose a username: ")
            if manager.vault_exists(username):
                console.print("[red]User already exists.[/red]")
                continue
            vault_data, master_password = create_user_flow(username)
        elif choice == "3":
            console.print("[blue]Exiting...[/blue]")
            break
        else:
            console.print("[red]Invalid choice.[/red]")
            continue

        if vault_data is not None:
            menu(vault_data, master_password, username)
