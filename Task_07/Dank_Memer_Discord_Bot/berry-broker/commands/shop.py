from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from services.shop_service import (
    get_all_items,
    purchase_item,
    get_user_inventory,
    get_user_balance
)

console = Console()


def visit_shop():
    """Display all available shop items in a beautiful table."""
    items = get_all_items()
    
    if not items:
        warning_panel = Panel(
            "[bold yellow]The shop is empty! Come back later.[/bold yellow]",
            title="[bold yellow]⚠ Shop Closed[/bold yellow]",
            border_style="yellow",
            expand=False
        )
        console.print()
        console.print(warning_panel)
        console.print()
        return
    
    # Build the shop table
    shop_table = Table(
        title="🏪 PIRATE MARKET 🏪",
        title_style="bold cyan",
        show_header=True,
        header_style="bold magenta",
        border_style="cyan",
        expand=True
    )
    
    shop_table.add_column("ID", justify="center", style="bold yellow", width=4)
    shop_table.add_column("Item Name", style="bold white", width=20)
    shop_table.add_column("Price", justify="right", style="bold green", width=12)
    shop_table.add_column("Description", style="dim", width=35)
    shop_table.add_column("Effect", style="cyan", width=25)
    
    for item in items:
        shop_table.add_row(
            str(item["id"]),
            item["name"],
            f"{item['price']:,} 🍓",
            item["description"] or "No description",
            item["effect"] or "None"
        )
    
    console.print()
    console.print(shop_table)
    console.print()
    
    info_panel = Panel(
        "[dim]Use the buy command to purchase items from this shop.[/dim]\n"
        "[dim]Example: buy Berry Compass[/dim]",
        border_style="dim",
        expand=False
    )
    console.print(info_panel)
    console.print()


def buy_item(username, item_name):
    """Purchase an item from the shop."""
    # Validate item name
    if not item_name or not item_name.strip():
        error_panel = Panel(
            "[bold red]❌ Please specify an item name![/bold red]\n"
            "[dim]Usage: buy <item name>[/dim]",
            title="[bold red]⚠ Invalid Purchase[/bold red]",
            border_style="red",
            expand=False
        )
        console.print()
        console.print(error_panel)
        console.print()
        return
    
    # Attempt purchase
    result = purchase_item(username, item_name.strip())
    
    if not result["success"]:
        error_panel = Panel(
            f"[bold red]❌ {result['message']}[/bold red]",
            title="[bold red]⚠ Purchase Failed[/bold red]",
            border_style="red",
            expand=False
        )
        console.print()
        console.print(error_panel)
        console.print()
        return
    
    # Success display
    item = result["item"]
    new_balance = result["new_balance"]
    
    success_table = Table.grid(padding=(0, 2))
    success_table.add_column(style="bold cyan", justify="right")
    success_table.add_column(style="bold white")
    
    success_table.add_row("🎁 Item:", f"[bold green]{item['name']}[/bold green]")
    success_table.add_row("💰 Cost:", f"[red]{item['price']:,} 🍓[/red]")
    success_table.add_row("💼 Remaining:", f"[yellow]{new_balance:,} 🍓[/yellow]")
    
    if item["effect"]:
        success_table.add_row("✨ Effect:", f"[cyan]{item['effect']}[/cyan]")
    
    success_panel = Panel(
        success_table,
        title="[bold green]✅ Purchase Successful![/bold green]",
        subtitle="[dim]Item added to your inventory[/dim]",
        border_style="green",
        expand=False
    )
    
    console.print()
    console.print(success_panel)
    console.print()


def view_inventory(username):
    """Display the user's inventory."""
    items = get_user_inventory(username)
    
    if not items:
        empty_panel = Panel(
            "[bold yellow]Your inventory is empty![/bold yellow]\n\n"
            "[dim]Visit the shop to purchase items.[/dim]",
            title="[bold yellow]🎒 Empty Inventory[/bold yellow]",
            border_style="yellow",
            expand=False
        )
        console.print()
        console.print(empty_panel)
        console.print()
        return
    
    # Build inventory table
    inv_table = Table(
        title=f"🎒 {username}'s Inventory 🎒",
        title_style="bold cyan",
        show_header=True,
        header_style="bold magenta",
        border_style="cyan",
        expand=True
    )
    
    inv_table.add_column("Item Name", style="bold white", width=20)
    inv_table.add_column("Qty", justify="center", style="bold yellow", width=6)
    inv_table.add_column("Effect", style="cyan", width=30)
    inv_table.add_column("Status", justify="center", width=10)
    
    for item in items:
        status = "[green]ACTIVE[/green]" if item["active"] else "[dim]Inactive[/dim]"
        inv_table.add_row(
            item["name"],
            str(item["quantity"]),
            item["effect"] or "None",
            status
        )
    
    console.print()
    console.print(inv_table)
    console.print()
    
    # Show balance info
    balance = get_user_balance(username)
    balance_panel = Panel(
        f"💰 Wallet: [yellow]{balance['wallet']:,} 🍓[/yellow]  |  "
        f"🏦 Bank: [green]{balance['bank']:,} 🍓[/green]",
        border_style="dim",
        expand=False
    )
    console.print(balance_panel)
    console.print()