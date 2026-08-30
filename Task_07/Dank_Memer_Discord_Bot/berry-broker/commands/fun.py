from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from services.onepiece_api import get_random_logpose
from database.queries import get_user, get_transaction_history, get_leaderboard

console = Console()


def log_pose():
    """Fetch and display a random piece of One Piece lore from the Log Pose."""
    console.print("\n[dim]🧭 Calibrating the Log Pose...[/dim]")
    
    result = get_random_logpose()
    
    if not result or not result.get("success"):
        error_panel = Panel(
            "[bold red]❌ The Log Pose is spinning wildly![/bold red]\n\n"
            f"[dim]{result.get('message', 'Could not connect to the Grand Line.')}[/dim]\n\n"
            "[dim]Try again in a moment, navigator.[/dim]",
            title="[bold red]⚠ Navigation Error[/bold red]",
            border_style="red",
            expand=False
        )
        console.print()
        console.print(error_panel)
        console.print()
        return
    
    data = result["data"]
    category = data.get("category", "Unknown").title()
    name = data.get("name", "Unknown")
    description = data.get("description", "No information available.")
    
    # Build a lore panel
    lore_text = Text(description, style="italic")
    
    info_panel = Panel(
        lore_text,
        title=f"[bold cyan]🧭 LOG POSE: {name} 🧭[/bold cyan]",
        subtitle=f"[dim]Category: {category}[/dim]",
        border_style="cyan",
        expand=False,
        width=70
    )
    
    console.print()
    console.print(info_panel)
    console.print()


def view_leaderboard():
    """Display the richest pirates (Worst Generation leaderboard)."""
    leaders = get_leaderboard(limit=10)
    
    if not leaders:
        empty_panel = Panel(
            "[bold yellow]🏴‍☠️ No pirates found in the registry yet![/bold yellow]",
            title="[bold yellow]Worst Generation Leaderboard[/bold yellow]",
            border_style="yellow",
            expand=False
        )
        console.print()
        console.print(empty_panel)
        console.print()
        return
    
    leader_table = Table(
        title="🏴‍☠️ WORST GENERATION - LEADERBOARD 🏴‍☠️",
        title_style="bold yellow",
        show_header=True,
        header_style="bold cyan",
        border_style="yellow",
        expand=True
    )
    
    leader_table.add_column("Rank", justify="center", width=6)
    leader_table.add_column("Pirate", style="bold white", width=20)
    leader_table.add_column("Wallet", justify="right", style="green", width=14)
    leader_table.add_column("Bank", justify="right", style="cyan", width=14)
    leader_table.add_column("Total Bounty", justify="right", style="bold yellow", width=16)
    
    medals = ["🥇", "🥈", "🥉", "4th", "5th", "6th", "7th", "8th", "9th", "10th"]
    for idx, leader in enumerate(leaders):
        rank = medals[idx] if idx < len(medals) else f"#{idx+1}"
        leader_table.add_row(
            rank,
            leader["username"],
            f"{leader['wallet']:,} 🍓",
            f"{leader['bank']:,} 🍓",
            f"{leader['total_wealth']:,} 🍓"
        )
    
    console.print()
    console.print(leader_table)
    console.print()


def view_history(username):
    """Display the user's transaction history."""
    user = get_user(username)
    
    if not user:
        error_panel = Panel(
            f"[bold red]❌ Pirate '{username}' not found in the registry.[/bold red]",
            title="[bold red]⚠ Unknown Pirate[/bold red]",
            border_style="red",
            expand=False
        )
        console.print()
        console.print(error_panel)
        console.print()
        return
    
    history = get_transaction_history(user["id"], limit=20)
    
    if not history:
        empty_panel = Panel(
            "[bold yellow]📜 No transactions recorded yet![/bold yellow]\n\n"
            "[dim]Your ship's log is empty. Start trading, raiding, or claiming daily rewards.[/dim]",
            title=f"[bold yellow]📜 {username}'s Ship Log[/bold yellow]",
            border_style="yellow",
            expand=False
        )
        console.print()
        console.print(empty_panel)
        console.print()
        return
    
    history_table = Table(
        title=f"📜 {username}'s Transaction Log 📜",
        title_style="bold cyan",
        show_header=True,
        header_style="bold magenta",
        border_style="cyan",
        expand=True
    )
    
    history_table.add_column("Time", style="dim", width=18)
    history_table.add_column("Type", justify="center", width=12)
    history_table.add_column("Amount", justify="right", width=12)
    history_table.add_column("With/From", style="white", width=18)
    history_table.add_column("Description", style="dim")
    
    type_icons = {
        "daily": "⛵",
        "trade": "🤝",
        "raid_win": "⚔️",
        "raid_loss": "💀",
        "purchase": "🛒",
        "reward": "🎁"
    }
    
    type_colors = {
        "daily": "green",
        "trade": "cyan",
        "raid_win": "bold green",
        "raid_loss": "bold red",
        "purchase": "yellow",
        "reward": "magenta"
    }
    
    for tx in history:
        tx_type = tx["type"]
        icon = type_icons.get(tx_type, "📌")
        color = type_colors.get(tx_type, "white")
        
        amount = tx["amount"]
        if amount > 0:
            amount_str = f"[green]+{amount:,} 🍓[/green]"
        else:
            amount_str = f"[red]{amount:,} 🍓[/red]"
        
        target = tx["target_username"] if tx["target_username"] else "—"
        desc = tx["description"] or "—"
        timestamp = tx["timestamp"][:16] if tx["timestamp"] else "—"
        
        history_table.add_row(
            timestamp,
            f"[{color}]{icon} {tx_type.upper()}[/{color}]",
            amount_str,
            target,
            desc
        )
    
    console.print()
    console.print(history_table)
    
    summary_panel = Panel(
        f"[dim]Showing last {len(history)} transactions[/dim]",
        border_style="dim",
        expand=False
    )
    console.print(summary_panel)
    console.print()