# Copyright (c) 2026 SysMind Contributors
# Licensed under the MIT License.
# See LICENSE file in the project root for full license information.

import os
import sys
import shutil
import subprocess
from rich.console import Console
from dotenv import load_dotenv

load_dotenv()

console = Console()

def check():
    console.print("[bold cyan]🚀 SysMind Pre-Flight Check[/bold cyan]")
    
    # 1. Check API Key
    if os.environ.get("GEMINI_API_KEY"):
        console.print("[green]✔[/green] GEMINI_API_KEY found.")
    else:
        console.print("[red]✘[/red] GEMINI_API_KEY missing in env!")

    # 2. Check Docker
    if shutil.which("docker"):
        console.print("[green]✔[/green] Docker CLI found.")
    else:
        console.print("[red]✘[/red] Docker CLI missing!")

    # 3. Check Target Container
    try:
        res = subprocess.run("docker inspect -f '{{.State.Running}}' sysmind-target", shell=True, capture_output=True, text=True)
        if "true" in res.stdout.lower():
            console.print("[green]✔[/green] Target Container (sysmind-target) is RUNNING.")
        else:
            console.print("[red]✘[/red] Target Container is DOWN! Run 'docker-compose up -d'.")
    except Exception as e:
        console.print(f"[red]✘[/red] Docker check failed: {e}")

    # 4. Check Generated Files
    if os.path.exists("dashboard_cpu_spike.png"):
        console.print("[green]✔[/green] Dashboard image ready.")
    else:
        console.print("[yellow]![/yellow] dashboard_cpu_spike.png missing. Run 'python generate_dashboard.py'.")

if __name__ == "__main__":
    check()
