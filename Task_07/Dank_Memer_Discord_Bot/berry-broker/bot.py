import sys
import os
import argparse
import asyncio
import discord
from discord.ext import commands
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt, IntPrompt

from database.schema import initialize_database
from config import DISCORD_TOKEN
import commands as cmd

console = Console()


# ==========================================
# Terminal CLI Mode
# ==========================================
def run_cli():
    """Run Berry Broker in interactive terminal CLI mode."""
    console.print("\n[bold cyan]⚓ Welcome to Berry Broker Interactive CLI ⚓[/bold cyan]")
    username = Prompt.ask("[bold yellow]Enter your pirate captain name[/bold yellow]", default="Luffy")
    
    while True:
        console.clear()
        
        title = Text("⚓ BERRY BROKER ⚓", style="bold cyan")
        subtitle = Text(f"Grand Line Economy Simulator • Captain {username}", style="dim italic")
        
        menu_text = Text.assemble(
            ("\n[1] ", "bold yellow"), ("Check Bounty\n", "white"),
            ("[2] ", "bold yellow"), ("Set Sail (Daily Reward)\n", "white"),
            ("[3] ", "bold yellow"), ("Trade Berries\n", "white"),
            ("[4] ", "bold yellow"), ("Visit Shop\n", "white"),
            ("[5] ", "bold yellow"), ("Buy Item\n", "white"),
            ("[6] ", "bold yellow"), ("View Inventory\n", "white"),
            ("[7] ", "bold yellow"), ("Worst Generation (Leaderboard)\n", "white"),
            ("[8] ", "bold yellow"), ("Raid Another Pirate\n", "white"),
            ("[9] ", "bold yellow"), ("Log Pose (One Piece Lore)\n", "white"),
            ("[10] ", "bold yellow"), ("Transaction History\n", "white"),
            ("[0] ", "bold yellow"), ("Exit\n", "white"),
        )
        
        panel = Panel(
            menu_text,
            title=title,
            subtitle=subtitle,
            border_style="cyan",
            expand=False
        )
        
        console.print(panel)
        choice = Prompt.ask("Enter your choice", choices=[str(i) for i in range(11)])
        
        if choice == "0":
            console.print("\n[yellow]Fair winds, pirate! ⚓[/yellow]\n")
            break
        elif choice == "1":
            cmd.check_bounty(username)
        elif choice == "2":
            cmd.set_sail(username)
        elif choice == "3":
            receiver = Prompt.ask("Enter recipient pirate name")
            amount = IntPrompt.ask("Enter berry amount to trade")
            cmd.trade_berries(username, receiver, amount)
        elif choice == "4":
            cmd.visit_shop()
        elif choice == "5":
            item_name = Prompt.ask("Enter item name to purchase")
            cmd.buy_item(username, item_name)
        elif choice == "6":
            cmd.view_inventory(username)
        elif choice == "7":
            cmd.view_leaderboard()
        elif choice == "8":
            target = Prompt.ask("Enter pirate name to raid")
            cmd.raid_pirate(username, target)
        elif choice == "9":
            cmd.log_pose()
        elif choice == "10":
            cmd.view_history(username)
            
        console.input("\n[dim]Press Enter to continue...[/dim]")


# ==========================================
# Discord Bot Mode
# ==========================================
class BerryBrokerBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(
            command_prefix=commands.when_mentioned_or("!"),
            intents=intents,
            help_command=None
        )

    async def setup_hook(self):
        console.print("[cyan]Loading Discord command modules...[/cyan]")
        await self.load_extension("commands.discord_cogs")
        try:
            synced = await self.tree.sync()
            console.print(f"[green]✓ Successfully synced {len(synced)} slash commands.[/green]")
        except Exception as e:
            console.print(f"[yellow]⚠ Failed to sync slash commands: {e}[/yellow]")

    async def on_ready(self):
        console.print(f"[bold green]✓ Logged in as {self.user.name} ({self.user.id})[/bold green]")
        console.print(f"[bold cyan]⚓ Berry Broker Discord Bot is online and ready![/bold cyan]")
        console.print(f"[dim]Default prefix: '!' | Slash commands enabled[/dim]\n")
        
        # Set Discord presence
        activity = discord.Activity(
            type=discord.ActivityType.watching,
            name="the Grand Line | !help"
        )
        await self.change_presence(activity=activity, status=discord.Status.online)

    async def on_command_error(self, ctx: commands.Context, error: Exception):
        if isinstance(error, commands.CommandNotFound):
            return
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"❌ Missing argument: `{error.param.name}`. Use `!help` for usage.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send(f"❌ Invalid argument provided. Please check command format.")
        else:
            console.print(f"[bold red]Command Error:[/bold red] {error}")
            await ctx.send(f"❌ An error occurred while executing the command.")


def run_discord():
    """Start the Discord bot."""
    if not DISCORD_TOKEN or DISCORD_TOKEN == "your_discord_bot_token_here":
        console.print("[bold red]❌ DISCORD_TOKEN is missing or not set in .env![/bold red]")
        console.print("[yellow]Please update .env with your bot token or run in CLI mode with: python bot.py --cli[/yellow]\n")
        sys.exit(1)
        
    bot = BerryBrokerBot()
    
    @bot.command(name="help")
    async def help_command(ctx: commands.Context):
        embed = discord.Embed(
            title="⚓ BERRY BROKER - Pirate Help & Commands ⚓",
            description="Welcome to the Grand Line Economy! Here are all available pirate commands:\n",
            color=0xF1C40F
        )
        
        embed.add_field(
            name="💰 Economy Commands",
            value=(
                "`!bounty [@user]` or `/bounty` — View wallet, bank, and total bounty\n"
                "`!daily` or `/daily` — Set sail and claim daily berry plunder\n"
                "`!trade <@user> <amount>` or `/trade` — Transfer berries to another pirate"
            ),
            inline=False
        )
        embed.add_field(
            name="🏪 Market & Inventory",
            value=(
                "`!shop` or `/shop` — Browse the Pirate Market\n"
                "`!buy <item_name>` or `/buy` — Purchase an artifact from the shop\n"
                "`!inventory [@user]` or `/inventory` — View owned items & effects"
            ),
            inline=False
        )
        embed.add_field(
            name="⚔️ Raids & Warfare",
            value=(
                "`!raid <@user>` or `/raid` — Attack a rival pirate and steal their berries!"
            ),
            inline=False
        )
        embed.add_field(
            name="🧭 Lore & Statistics",
            value=(
                "`!logpose` or `/logpose` — Random One Piece world lore\n"
                "`!leaderboard` or `/leaderboard` — View the Worst Generation top pirates\n"
                "`!history` or `/history` — View your transaction log"
            ),
            inline=False
        )
        embed.set_footer(text="Grand Line Economy • Berry Broker Bot")
        await ctx.send(embed=embed)
        
    console.print("\n[bold cyan]Connecting to Discord Gateway...[/bold cyan]")
    try:
        bot.run(DISCORD_TOKEN)
    except discord.errors.LoginFailure:
        console.print("[bold red]❌ Invalid Discord Token! Please verify your token in .env.[/bold red]")
        sys.exit(1)
    except Exception as e:
        console.print(f"[bold red]❌ Fatal Discord Error: {e}[/bold red]")
        sys.exit(1)


# ==========================================
# Main Entry Point
# ==========================================
def main():
    parser = argparse.ArgumentParser(description="Berry Broker - Grand Line Economy Bot")
    parser.add_argument("--cli", action="store_true", help="Run interactive terminal CLI menu")
    args = parser.parse_args()
    
    console.print("[bold cyan]Initializing Berry Broker...[/bold cyan]")
    initialize_database()
    console.print("[green]✓ Database schema & shop items ready[/green]\n")
    
    if args.cli:
        run_cli()
    else:
        run_discord()


if __name__ == "__main__":
    main()