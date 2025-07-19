# Lockout.py
# All functions related to locking the password manager up.
# Tracks lockout duration using both system-independent monotonic time
# and an external time API to prevent time rollback attacks.

import os
import time
import json
import requests
from rich.progress import Progress, BarColumn, TimeRemainingColumn
from rich.console import Console

class LockoutHandler:
    # Handles lockout after too many failed login attempts.
    # Lockout time increases with each failure and resets on successful login.
    
    def __init__(self, lock_file=".lock", max_attempts=10, duration=5 * 60):
        self.lock_file = lock_file
        self.max_attempts = max_attempts
        self.duration = duration
        self.console = Console()

    def _get_online_time(self):
        # Gets current UTC time from online API (worldtimeapi.org)
        try:
            response = requests.get("https://worldtimeapi.org/api/timezone/etc/UTC", timeout=3)
            if response.status_code == 200:
                return response.json()["unixtime"]
        except requests.RequestException:
            pass
        return None  # fallback if offline

    def is_locked(self):
        # Checks if user is still locked out
        if not os.path.exists(self.lock_file):
            return None

        try:
            with open(self.lock_file, "r") as f:
                lock_data = json.load(f)
                time_online_then = lock_data["wall_time"]
                time_monotonic_then = lock_data["mono_time"]
                self.duration = lock_data.get("duration", self.duration)
        except Exception:
            return None

        time_online_now = self._get_online_time()
        time_monotonic_now = time.monotonic()

        if time_online_now is not None:
            time_passed = time_online_now - time_online_then
        else:
            time_passed = time_monotonic_now - time_monotonic_then

        time_left = self.duration - time_passed
        return int(time_left) if time_left > 0 else None

    def lock(self):
        # Locks the user and sets how long based on how many times it's happened
        previous_strikes = 0
        if os.path.exists(self.lock_file):
            try:
                with open(self.lock_file, "r") as f:
                    prev_data = json.load(f)
                    previous_strikes = prev_data.get("lock_count", 0)
            except Exception:
                pass

        this_strike = previous_strikes + 1

        # Progressive lockout: 1st = 1 min, 2nd = 2 mins, 3rd = 5 mins, then capped at 10 mins
        delay_map = {1: 60, 2: 120, 3: 300}
        this_timeout = delay_map.get(this_strike, 600)

        time_online_now = self._get_online_time() or time.time()
        time_monotonic_now = time.monotonic()

        lock_data = {
            "wall_time": time_online_now,
            "mono_time": time_monotonic_now,
            "lock_count": this_strike,
            "duration": this_timeout
        }

        with open(self.lock_file, "w") as f:
            json.dump(lock_data, f)

        self.duration = this_timeout

    def reset(self):
        # Clears lock file and resets lockout count
        if os.path.exists(self.lock_file):
            try:
                os.remove(self.lock_file)
            except Exception:
                pass

    def show_timer(self, seconds):
        # Shows a countdown timer using rich progress bar
        self.console.print(f"[red]Too many incorrect attempts. Locked for {seconds // 60} minutes.[/red]")

        with Progress(
            "[progress.description]{task.description}",
            BarColumn(),
            TimeRemainingColumn(),
            transient=True
        ) as progress:
            lock_bar = progress.add_task("Locking down...", total=seconds)
            for _ in range(seconds):
                time.sleep(1)
                progress.update(lock_bar, advance=1)
