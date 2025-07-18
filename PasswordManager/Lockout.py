import time
from rich.progress import Progress, BarColumn, TimeRemainingColumn

class LockoutHandler:
    def __init__(self, lock_file: str = ".lock", max_attempts: int = 10, duration: int = 5 * 60):
        self.lock_file = lock_file
        self.max_attempts = max_attempts
        self.duration = duration

    def is_locked(self):
        try:
            with open(self.lock_file, "r") as f:
                lock_time = float(f.read())
                if time.time() < lock_time:
                    return int(lock_time - time.time())
        except FileNotFoundError:
            pass
        return None

    def lock(self):
        with open(self.lock_file, "w") as f:
            f.write(str(time.time() + self.duration))

    def show_timer(self, seconds):
        from rich.console import Console
        console = Console()
        console.print(f"[red]Too many incorrect attempts. Locked for {seconds // 60} minutes.[/red]")
        with Progress("[progress.description]{task.description}", BarColumn(), TimeRemainingColumn(), transient=True) as progress:
            task = progress.add_task("Locking down...", total=seconds)
            for _ in range(seconds):
                time.sleep(1)
                progress.update(task, advance=1)