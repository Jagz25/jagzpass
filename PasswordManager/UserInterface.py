# UserInterface.py
from rich.console import Console

class UserInterface:
    def __init__(self):
        self.console = Console()

    def prompt_main_menu(self):
        self.console.print("[bold]Welcome to JagzPass Password Manager[/bold]")
        self.console.print("[blue]1.[/blue] Login")
        self.console.print("[blue]2.[/blue] Create New User")
        self.console.print("[blue]3.[/blue] Exit")
        return self.console.input("[bold cyan]Select an option:[/bold cyan] ")

    def input(self, prompt: str):
        return self.console.input(prompt)

    def print(self, message: str):
        self.console.print(message)
