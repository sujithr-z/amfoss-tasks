import time
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.live import Live
from rich.table import Table
from rich import box

console = Console()

def clear_screen():
    console.clear()

def rich_animated_intro():
    """Rich module animated intro with colors and effects"""
    clear_screen()
    
    # Title with typing effect
    title_text = "🌟 WELCOME TO THE SHOP 🌟"
    displayed_title = ""
    
    for char in title_text:
        displayed_title += char
        text = Text(displayed_title, style="bold cyan", justify="center")
        panel = Panel(
            Align.center(text),
            border_style="bright_blue",
            box=box.DOUBLE,
            padding=(1, 10)
        )
        console.clear()
        console.print("\n" * 8)
        console.print(panel)
        time.sleep(0.05)
    
    time.sleep(0.5)
    
    # Subtitle with gradient effect
    subtitle = Text("Your Premium Shopping Destination", style="bold yellow", justify="center")
    console.print("\n")
    console.print(Align.center(subtitle))
    time.sleep(1)
    
    # Feature showcase with animation
    console.print("\n")
    features = [
        ("✨", "Premium Products", "cyan"),
        ("💰", "Best Prices", "green"),
        ("🚀", "Fast Service", "magenta"),
        ("🎯", "Quality Guaranteed", "yellow")
    ]
    
    table = Table(show_header=False, box=box.SIMPLE, expand=True)
    table.add_column(justify="center", style="bold")
    
    for emoji, feature, color in features:
        table.add_row(f"[{color}]{emoji} {feature}[/{color}]")
        console.clear()
        console.print("\n" * 8)
        console.print(panel)
        console.print("\n")
        console.print(Align.center(subtitle))
        console.print("\n")
        console.print(table)
        time.sleep(0.4)
    
    time.sleep(0.5)
    
    # Loading animation with progress bar
    console.print("\n")
    with Progress(
        SpinnerColumn(style="cyan"),
        TextColumn("[bold blue]Loading shop system..."),
        console=console,
        transient=True
    ) as progress:
        task = progress.add_task("", total=100)
        for i in range(100):
            progress.update(task, advance=1)
            time.sleep(0.02)
    
    # Ready message
    console.print("\n")
    ready_text = Text("✓ System Ready!", style="bold green blink", justify="center")
    console.print(Align.center(ready_text))
    
    time.sleep(0.5)
    
    # Press enter prompt
    console.print("\n")
    prompt = Panel(
        "[bold white]Press [cyan]ENTER[/cyan] to start shopping[/bold white]",
        border_style="green",
        box=box.ROUNDED
    )
    console.print(Align.center(prompt))
    
    input()
    clear_screen()

def rich_simple_intro():
    """Simpler rich intro"""
    clear_screen()
    
    # Main panel
    title = Text()
    title.append("🛒 ", style="bold yellow")
    title.append("WELCOME TO THE SHOP", style="bold white on blue")
    title.append(" 🛒", style="bold yellow")
    
    main_panel = Panel(
        Align.center(title),
        border_style="bright_blue",
        box=box.DOUBLE_EDGE,
        padding=(2, 5)
    )
    
    console.print("\n" * 10)
    console.print(main_panel)
    
    time.sleep(0.8)
    
    # Animated dots
    console.print("\n")
    with console.status("[bold cyan]Initializing shop system...", spinner="dots"):
        time.sleep(2)
    
    console.print("\n[bold green]✓[/bold green] Ready to serve you!")
    time.sleep(0.5)
    
    console.print("\n[dim]Press ENTER to continue...[/dim]")
    input()
    clear_screen()

def rich_fancy_intro():
    """Fancy intro with multiple effects"""
    clear_screen()
    
    # Animated border reveal
    console.print("\n" * 10)
    
    borders = [
        "[blue]╔[/blue]",
        "[blue]╔═[/blue]",
        "[blue]╔══[/blue]",
        "[blue]╔═══════════════════════════════════[/blue]",
        "[blue]╔═══════════════════════════════════╗[/blue]"
    ]
    
    for border in borders:
        console.clear()
        console.print("\n" * 10)
        console.print(border, justify="center")
        time.sleep(0.1)
    
    # Build the complete box
    box_lines = [
        "[blue]╔═══════════════════════════════════╗[/blue]",
        "[blue]║[/blue]                                   [blue]║[/blue]",
        "[blue]║[/blue]   [bold cyan]🌟 WELCOME TO THE SHOP 🌟[/bold cyan]   [blue]║[/blue]",
        "[blue]║[/blue]                                   [blue]║[/blue]",
        "[blue]╚═══════════════════════════════════╝[/blue]"
    ]
    
    for i in range(len(box_lines)):
        console.clear()
        console.print("\n" * 10)
        for line in box_lines[:i+1]:
            console.print(line, justify="center")
        time.sleep(0.2)
    
    time.sleep(0.5)
    
    # Tagline appears
    console.print("\n[bold yellow]Your Gateway to Premium Shopping[/bold yellow]", justify="center")
    time.sleep(0.8)
    
    # Features appear one by one
    console.print("\n")
    features_text = [
        "[cyan]✨ Quality Products[/cyan]",
        "[green]💰 Competitive Prices[/green]",
        "[magenta]🚀 Lightning Fast[/magenta]"
    ]
    
    for feature in features_text:
        console.print(f"            {feature}")
        time.sleep(0.3)
    
    # Loading bar
    console.print("\n")
    with Progress(
        TextColumn("[bold blue]{task.description}"),
        SpinnerColumn("bouncingBar", style="cyan"),
        console=console,
        transient=True
    ) as progress:
        progress.add_task("Preparing your experience", total=None)
        time.sleep(1.5)
    
    console.print("\n[bold green]⚡ All systems ready![/bold green]", justify="center")
    console.print("\n[dim italic]Press ENTER to begin...[/dim italic]", justify="center")
    
    input()
    clear_screen()

# Example usage
if __name__ == "__main__":
    console.print("\n[bold cyan]Choose intro style:[/bold cyan]")
    console.print("[yellow]1.[/yellow] Rich Animated Intro (Full features)")
    console.print("[yellow]2.[/yellow] Rich Simple Intro (Quick & clean)")
    console.print("[yellow]3.[/yellow] Rich Fancy Intro (Fancy animations)")
    
    choice = input("\n[bold]Enter choice (1-3):[/bold] ")
    
    if choice == "1":
        rich_animated_intro()
    elif choice == "2":
        rich_simple_intro()
    elif choice == "3":
        rich_fancy_intro()
    else:
        console.print("[red]Invalid choice![/red]")
    
    console.print("\n[bold green]🛒 Shop System Loaded Successfully! 🛒[/bold green]\n")