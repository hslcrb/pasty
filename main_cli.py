
"""
Pasty (페이스티) - CLI Version
"""

import sys
import time
import argparse
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.progress import track
from rich.live import Live
from rich.layout import Layout
from rich import print as rprint

from src.engine import GhostTyper
from src.config import APP_NAME, VERSION, STRINGS

console = Console()

def print_header(lang="ko"):
    s = STRINGS[lang]
    grid = Panel.fit(
        f"[bold cyan]{APP_NAME} {VERSION}[/bold cyan]\n[dim]{s['subtitle']}[/dim]",
        border_style="blue",
        title=s["copyright"],
        subtitle="CLI Version"
    )
    console.print(grid)

def main():
    parser = argparse.ArgumentParser(description="Pasty CLI - Ghost Typing Tool")
    parser.add_argument("source", nargs="?", help="Source text file")
    parser.add_argument("target", nargs="?", help="Target file to append to (optional)")
    parser.add_argument("--lang", choices=["ko", "en"], default="ko", help="Interface language")
    
    args = parser.parse_args()
    lang = args.lang
    s = STRINGS[lang]
    
    print_header(lang)
    
    # 1. Source File
    source_path = args.source
    if not source_path:
        source_path = Prompt.ask(f"[bold green]{s['source_label']}[/bold green]")
    
    if not Path(source_path).exists():
        console.print(f"[bold red]{s['error']}: {s['failed_read']} ({source_path})[/bold red]")
        sys.exit(1)
        
    try:
        with open(source_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        console.print(f"[bold red]{s['error']}: {e}[/bold red]")
        sys.exit(1)

    # 2. Target File
    target_path = args.target
    if not target_path:
        target_path = Prompt.ask(f"[bold green]{s['target_label']}[/bold green] (Enter to skip)")
    
    if target_path and not Path(target_path).exists():
        Path(target_path).touch()

    # 3. Armed & Ready
    engine = GhostTyper(content, target_path)
    engine.start()
    
    console.print(f"\n[bold yellow]>>> {s['ready']} <<<[/bold yellow]")
    console.print(f"[dim]Press [bold white]HOLD TO START[/bold white] (Any key logic simulated by holding space or just standard typing)[/dim]")
    console.print(f"[bold red]CLI Mode: Press 'Enter' to toggle recording. Press 'Ctrl+C' to exit.[/bold red]\n")
    
    is_recording = False
    
    try:
        while True:
            cmd = Prompt.ask("[bold blue]Command[/bold blue] (start/stop/exit)", choices=["start", "stop", "exit"], default="start")
            
            if cmd == "exit":
                break
            elif cmd == "start":
                if not is_recording:
                    is_recording = True
                    engine.set_recording(True)
                    console.print(f"[bold red]{s['rec']} {s['pasting']}[/bold red]")
            elif cmd == "stop":
                if is_recording:
                    is_recording = False
                    engine.set_recording(False)
                    console.print(f("[bold green]PAUSED[/bold green]"))
            
    except KeyboardInterrupt:
        pass
    finally:
        engine.stop()
        console.print("\n[bold cyan]Goodbye![/bold cyan]")

if __name__ == "__main__":
    main()
