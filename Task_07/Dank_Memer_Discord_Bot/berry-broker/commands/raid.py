import time
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.live import Live

from services.raid_service import attempt_raid

console = Console()


def raid_pirate(raider, target):
    """Attempt to raid another pirate and steal their berries."""
    
    # Validate: can't raid yourself
    if raider.lower() == target.lower():
        error_panel = Panel(
            "[bold red]❌ You can't raid yourself, ya fool![/bold red]\n"
            "[dim]Find another pirate to plunder.[/dim]",
            title="[bold red]⚠ Invalid Target[/bold red]",
            border_style="red",
            expand=False
        )
        console.print()
        console.print(error_panel)
        console.print()
        return
    
    # Dramatic battle animation
    console.print()
    battle_stages = [
        "[dim]⚔️  Drawing swords...[/dim]",
        "[yellow]⚔️  Sailing toward target...[/yellow]",
        "[bold yellow]⚔️  Engaging in battle![/bold yellow]",
        "[bold red]⚔️  ⚔️  ⚔️  CLASH!  ⚔️  ⚔️[/bold red]",
    ]
    
    with Live(console=console, refresh_per_second=4, transient=True) as live:
        for stage in battle_stages:
            live.update(Panel(stage, border_style="yellow", expand=False))
            time.sleep(0.4)
    
    # Attempt the raid
    result = attempt_raid(raider, target)
    
    # Handle error cases
    if not result.get("attempted", False):
        error_panel = Panel(
            f"[bold red]❌ {result.get('message', 'Raid failed.')}[/bold red]",
            title="[bold red]⚠ Raid Aborted[/bold red]",
            border_style="red",
            expand=False
        )
        console.print()
        console.print(error_panel)
        console.print()
        return
    
    # Build the battle report
    report_table = Table.grid(padding=(0, 2))
    report_table.add_column(style="bold cyan", justify="right")
    report_table.add_column(style="bold white")
    
    report_table.add_row("👤 Raider:", f"[bold]{raider}[/bold]")
    report_table.add_row("🎯 Target:", f"[bold]{target}[/bold]")
    report_table.add_row("─" * 20, "─" * 15)
    
    if result["success"]:
        # SUCCESS - raider stole berries
        report_table.add_row(
            "💰 Plundered:",
            f"[bold green]+{result['amount']:,} 🍓[/bold green]"
        )
        report_table.add_row(
            "💼 Your Wallet:",
            f"[yellow]{result['raider_new_balance']:,} 🍓[/yellow]"
        )
        
        success_panel = Panel(
            report_table,
            title="[bold green]⚔️ VICTORY! ⚔️[/bold green]",
            subtitle=f"[dim]You raided {target}'s ship and escaped with the loot![/dim]",
            border_style="green",
            expand=False
        )
        
        console.print()
        console.print(success_panel)
        console.print()
        
    else:
        # FAILURE - raider lost berries
        report_table.add_row(
            "💸 Penalty:",
            f"[bold red]-{result['amount']:,} 🍓[/bold red]"
        )
        report_table.add_row(
            "💼 Your Wallet:",
            f"[yellow]{result['raider_new_balance']:,} 🍓[/yellow]"
        )
        
        failure_panel = Panel(
            report_table,
            title="[bold red]💀 DEFEAT! 💀[/bold red]",
            subtitle=f"[dim]{target} fought back! You lost berries in the battle.[/dim]",
            border_style="red",
            expand=False
        )
        
        console.print()
        console.print(failure_panel)
        console.print()