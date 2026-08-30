from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from datetime import datetime, timedelta

from services.economy_service import (
    get_or_create_user,
    claim_daily,
    transfer_berries,
    get_user_bounty
)
from config import DAILY_COOLDOWN_HOURS

console = Console()


def check_bounty(username):
    """Display the user's current wallet, bank, and total bounty."""
    user = get_or_create_user(username)
    
    total = user["wallet"] + user["bank"]
    
    # Build a beautiful bounty card
    bounty_table = Table.grid(padding=(0, 2))
    bounty_table.add_column(style="bold cyan", justify="right")
    bounty_table.add_column(style="bold white")
    
    bounty_table.add_row("💰 Wallet:", f"{user['wallet']:,} 🍓")
    bounty_table.add_row("🏦 Bank:", f"{user['bank']:,} 🍓")
    bounty_table.add_row("─" * 20, "─" * 15)
    bounty_table.add_row("🏴‍☠️ Total Bounty:", f"[bold yellow]{total:,} 🍓[/bold yellow]")
    
    panel = Panel(
        bounty_table,
        title=f"[bold cyan]⚓ {username}'s Bounty ⚓[/bold cyan]",
        subtitle=f"[dim]Pirate since {user['created_at']}[/dim]",
        border_style="cyan",
        expand=False
    )
    
    console.print()
    console.print(panel)
    console.print()


def set_sail(username):
    """Claim the daily reward (once every 24 hours)."""
    user = get_or_create_user(username)
    
    # Check cooldown
    if user["last_daily"]:
        last_claim = datetime.fromisoformat(user["last_daily"])
        cooldown_end = last_claim + timedelta(hours=DAILY_COOLDOWN_HOURS)
        now = datetime.now()
        
        if now < cooldown_end:
            remaining = cooldown_end - now
            hours = remaining.seconds // 3600
            minutes = (remaining.seconds % 3600) // 60
            
            warning_panel = Panel(
                f"[bold red]⏰ Your compass is still recalibrating![/bold red]\n\n"
                f"Try again in [yellow]{hours}h {minutes}m[/yellow]\n"
                f"[dim](Cooldown: {DAILY_COOLDOWN_HOURS} hours)[/dim]",
                title="[bold yellow]⚠ Not Yet, Captain![/bold yellow]",
                border_style="yellow",
                expand=False
            )
            console.print()
            console.print(warning_panel)
            console.print()
            return
    
    # Claim reward
    reward = claim_daily(username)
    
    success_panel = Panel(
        f"[bold green]🎉 You plundered {reward:,} berries from a merchant ship![/bold green]\n\n"
        f"💰 New Wallet: [yellow]{get_user_bounty(username)['wallet']:,} 🍓[/yellow]\n"
        f"[dim]Return tomorrow for more treasure...[/dim]",
        title="[bold green]⛵ Set Sail Successful! ⛵[/bold green]",
        border_style="green",
        expand=False
    )
    
    console.print()
    console.print(success_panel)
    console.print()


def trade_berries(sender, receiver, amount):
    """Transfer berries from one pirate to another."""
    # Validate amount
    if amount <= 0:
        error_panel = Panel(
            "[bold red]❌ You can't trade nothing, ya landlubber![/bold red]\n"
            "[dim]Enter a positive amount of berries.[/dim]",
            title="[bold red]⚠ Invalid Trade[/bold red]",
            border_style="red",
            expand=False
        )
        console.print()
        console.print(error_panel)
        console.print()
        return
    
    # Validate users aren't the same
    if sender.lower() == receiver.lower():
        error_panel = Panel(
            "[bold red]❌ You can't trade with yourself![/bold red]\n"
            "[dim]Find another pirate to deal with.[/dim]",
            title="[bold red]⚠ Invalid Trade[/bold red]",
            border_style="red",
            expand=False
        )
        console.print()
        console.print(error_panel)
        console.print()
        return
    
    # Attempt transfer
    result = transfer_berries(sender, receiver, amount)
    
    if not result["success"]:
        error_panel = Panel(
            f"[bold red]❌ {result['message']}[/bold red]",
            title="[bold red]⚠ Trade Failed[/bold red]",
            border_style="red",
            expand=False
        )
        console.print()
        console.print(error_panel)
        console.print()
        return
    
    # Success display
    trade_table = Table.grid(padding=(0, 2))
    trade_table.add_column(style="bold cyan")
    trade_table.add_column(style="bold white")
    
    trade_table.add_row("👤 From:", f"[red]{sender}[/red]")
    trade_table.add_row("👤 To:", f"[green]{receiver}[/green]")
    trade_table.add_row("💰 Amount:", f"[yellow]{amount:,} 🍓[/yellow]")
    
    success_panel = Panel(
        trade_table,
        title="[bold green]✅ Trade Completed![/bold green]",
        subtitle=f"[dim]Transaction recorded in the ship's log[/dim]",
        border_style="green",
        expand=False
    )
    
    console.print()
    console.print(success_panel)
    console.print()