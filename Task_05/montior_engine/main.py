import sys
import subprocess
import time

REQUIRED_PACKAGES = ["rich"]

def check_and_install_dependencies():
    missing_packages = []
    
    for package in REQUIRED_PACKAGES:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
            
    if missing_packages:
        print(f"[*] Missing dependencies detected: {', '.join(missing_packages)}")
        print("[*] Installing automatically using the current Python environment...")
        
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", *missing_packages])
            print("[+] Dependencies installed successfully!\n")
        except subprocess.CalledProcessError as e:
            print(f"[-] Failed to install dependencies: {e}")
            print("[-] Please install them manually: pip install rich")
            sys.exit(1)

check_and_install_dependencies()

from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from guardian.system.platform import detect_os
from guardian.collectors.linux import LinuxCollector
from guardian.collectors.windows import WindowsCollector
from guardian.core.monitor import Monitor
from guardian.ui.display import Display

console = Console()

def get_collector(os_type):
    if os_type == "Linux":
        return LinuxCollector()
    elif os_type == "Windows":
        return WindowsCollector()
    return None

def main():
    os_type = detect_os()
    
    title = Text("GRAND LINE GUARDIAN", style="bold cyan")
    subtitle = Text(f"Target OS: {os_type} | Refresh Rate: 0.5s", style="dim italic")
    
    console.print(Panel.fit(
        Text.assemble(title, "\n", subtitle),
        border_style="blue",
        title="System Monitor"
    ))
    
    console.print("\n[bold yellow]Initializing monitoring engine...[/bold yellow]")
    
    collector = get_collector(os_type)
    if not collector:
        console.print(f"[bold red]Error:[/bold red] Unsupported platform '{os_type}'. Guardian supports Windows and Linux.")
        sys.exit(1)
        
    monitor = Monitor(collector=collector, rate=0.5)
    display = Display(monitor=monitor, os_type=os_type, rate=0.5)
    
    time.sleep(1)
    console.print("[green][+] Bootstrap successful. Starting live monitor...[/green]")
    time.sleep(0.5)
    
    display.start()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[yellow]Grand Line Guardian shutting down gracefully...[/yellow]")
        sys.exit(0)