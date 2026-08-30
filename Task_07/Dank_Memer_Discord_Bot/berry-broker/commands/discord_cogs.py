import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime, timedelta

from services.economy_service import (
    get_or_create_user,
    get_user_bounty,
    claim_daily,
    transfer_berries
)
from services.shop_service import (
    get_all_items,
    purchase_item,
    get_user_inventory,
    get_user_balance
)
from services.raid_service import attempt_raid
from services.onepiece_api import get_random_logpose
from database.queries import get_leaderboard, get_transaction_history, get_user
from config import DAILY_COOLDOWN_HOURS


class EconomyCog(commands.Cog, name="Economy"):
    """Economy commands: Bounty, Daily rewards, and Trading."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="bounty", aliases=["balance", "bal", "wallet"])
    async def bounty_cmd(self, ctx: commands.Context, member: discord.Member = None):
        """Check your bounty or another pirate's bounty."""
        target = member or ctx.author
        bounty = get_user_bounty(target.name)

        embed = discord.Embed(
            title=f"⚓ {target.display_name}'s Bounty Poster",
            description=f"**Pirate Name:** {target.mention}",
            color=0xF1C40F
        )
        if target.display_avatar:
            embed.set_thumbnail(url=target.display_avatar.url)

        embed.add_field(name="💰 Wallet", value=f"`{bounty['wallet']:,} 🍓`", inline=True)
        embed.add_field(name="🏦 Bank", value=f"`{bounty['bank']:,} 🍓`", inline=True)
        embed.add_field(
            name="🏴‍☠️ Total Bounty",
            value=f"**{bounty['total']:,} 🍓**",
            inline=False
        )
        embed.set_footer(text="Grand Line Economy • Claim daily rewards with !daily")
        await ctx.send(embed=embed)

    @app_commands.command(name="bounty", description="Check your or another pirate's bounty")
    @app_commands.describe(member="The pirate whose bounty you want to inspect")
    async def bounty_slash(self, interaction: discord.Interaction, member: discord.Member = None):
        target = member or interaction.user
        bounty = get_user_bounty(target.name)

        embed = discord.Embed(
            title=f"⚓ {target.display_name}'s Bounty Poster",
            description=f"**Pirate Name:** {target.mention}",
            color=0xF1C40F
        )
        if target.display_avatar:
            embed.set_thumbnail(url=target.display_avatar.url)

        embed.add_field(name="💰 Wallet", value=f"`{bounty['wallet']:,} 🍓`", inline=True)
        embed.add_field(name="🏦 Bank", value=f"`{bounty['bank']:,} 🍓`", inline=True)
        embed.add_field(
            name="🏴‍☠️ Total Bounty",
            value=f"**{bounty['total']:,} 🍓**",
            inline=False
        )
        embed.set_footer(text="Grand Line Economy • Claim daily rewards with /daily")
        await interaction.response.send_message(embed=embed)

    @commands.command(name="daily", aliases=["setsail", "claim"])
    async def daily_cmd(self, ctx: commands.Context):
        """Set sail and claim your daily berry plunder!"""
        username = ctx.author.name
        user = get_or_create_user(username)

        # Check cooldown
        if user["last_daily"]:
            try:
                last_claim = datetime.fromisoformat(user["last_daily"])
                cooldown_end = last_claim + timedelta(hours=DAILY_COOLDOWN_HOURS)
                now = datetime.now()
                if now < cooldown_end:
                    remaining = cooldown_end - now
                    hours = remaining.seconds // 3600
                    minutes = (remaining.seconds % 3600) // 60
                    embed = discord.Embed(
                        title="⚠ Not Yet, Captain!",
                        description=(
                            f"⏰ Your compass is still recalibrating!\n\n"
                            f"Try again in **{hours}h {minutes}m**.\n"
                            f"*(Cooldown: {DAILY_COOLDOWN_HOURS} hours)*"
                        ),
                        color=0xE67E22
                    )
                    await ctx.send(embed=embed)
                    return
            except (ValueError, TypeError):
                pass

        reward = claim_daily(username)
        bounty = get_user_bounty(username)

        embed = discord.Embed(
            title="⛵ Set Sail Successful!",
            description=(
                f"🎉 **{ctx.author.display_name}** plundered **{reward:,} berries** from a merchant ship!\n\n"
                f"💰 **New Wallet:** `{bounty['wallet']:,} 🍓`\n"
                f"*Return tomorrow for more treasure...*"
            ),
            color=0x2ECC71
        )
        await ctx.send(embed=embed)

    @app_commands.command(name="daily", description="Claim your daily berry plunder")
    async def daily_slash(self, interaction: discord.Interaction):
        username = interaction.user.name
        user = get_or_create_user(username)

        if user["last_daily"]:
            try:
                last_claim = datetime.fromisoformat(user["last_daily"])
                cooldown_end = last_claim + timedelta(hours=DAILY_COOLDOWN_HOURS)
                now = datetime.now()
                if now < cooldown_end:
                    remaining = cooldown_end - now
                    hours = remaining.seconds // 3600
                    minutes = (remaining.seconds % 3600) // 60
                    embed = discord.Embed(
                        title="⚠ Not Yet, Captain!",
                        description=(
                            f"⏰ Your compass is still recalibrating!\n\n"
                            f"Try again in **{hours}h {minutes}m**.\n"
                            f"*(Cooldown: {DAILY_COOLDOWN_HOURS} hours)*"
                        ),
                        color=0xE67E22
                    )
                    await interaction.response.send_message(embed=embed)
                    return
            except (ValueError, TypeError):
                pass

        reward = claim_daily(username)
        bounty = get_user_bounty(username)

        embed = discord.Embed(
            title="⛵ Set Sail Successful!",
            description=(
                f"🎉 **{interaction.user.display_name}** plundered **{reward:,} berries** from a merchant ship!\n\n"
                f"💰 **New Wallet:** `{bounty['wallet']:,} 🍓`\n"
                f"*Return tomorrow for more treasure...*"
            ),
            color=0x2ECC71
        )
        await interaction.response.send_message(embed=embed)

    @commands.command(name="trade", aliases=["pay", "give", "transfer"])
    async def trade_cmd(self, ctx: commands.Context, member: discord.Member, amount: int):
        """Transfer berries to another pirate."""
        if amount <= 0:
            embed = discord.Embed(
                title="❌ Invalid Trade",
                description="You must trade a positive amount of berries.",
                color=0xE74C3C
            )
            await ctx.send(embed=embed)
            return

        if ctx.author.id == member.id:
            embed = discord.Embed(
                title="❌ Invalid Trade",
                description="You cannot trade berries with yourself!",
                color=0xE74C3C
            )
            await ctx.send(embed=embed)
            return

        result = transfer_berries(ctx.author.name, member.name, amount)
        if not result["success"]:
            embed = discord.Embed(
                title="❌ Trade Failed",
                description=result["message"],
                color=0xE74C3C
            )
            await ctx.send(embed=embed)
            return

        embed = discord.Embed(
            title="✅ Trade Completed!",
            description=(
                f"🤝 **{ctx.author.display_name}** transferred **{amount:,} 🍓** to **{member.display_name}**!\n\n"
                f"*Transaction recorded in the ship's log.*"
            ),
            color=0x1ABC9C
        )
        await ctx.send(embed=embed)

    @app_commands.command(name="trade", description="Transfer berries to another pirate")
    @app_commands.describe(member="The pirate to receive berries", amount="Amount of berries to send")
    async def trade_slash(self, interaction: discord.Interaction, member: discord.Member, amount: int):
        if amount <= 0:
            embed = discord.Embed(
                title="❌ Invalid Trade",
                description="You must trade a positive amount of berries.",
                color=0xE74C3C
            )
            await interaction.response.send_message(embed=embed)
            return

        if interaction.user.id == member.id:
            embed = discord.Embed(
                title="❌ Invalid Trade",
                description="You cannot trade berries with yourself!",
                color=0xE74C3C
            )
            await interaction.response.send_message(embed=embed)
            return

        result = transfer_berries(interaction.user.name, member.name, amount)
        if not result["success"]:
            embed = discord.Embed(
                title="❌ Trade Failed",
                description=result["message"],
                color=0xE74C3C
            )
            await interaction.response.send_message(embed=embed)
            return

        embed = discord.Embed(
            title="✅ Trade Completed!",
            description=(
                f"🤝 **{interaction.user.display_name}** transferred **{amount:,} 🍓** to **{member.display_name}**!\n\n"
                f"*Transaction recorded in the ship's log.*"
            ),
            color=0x1ABC9C
        )
        await interaction.response.send_message(embed=embed)


class ShopCog(commands.Cog, name="Shop"):
    """Shop commands: Visit shop, Buy items, and View Inventory."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="shop", aliases=["market", "store"])
    async def shop_cmd(self, ctx: commands.Context):
        """Browse items in the Pirate Market."""
        items = get_all_items()
        if not items:
            embed = discord.Embed(
                title="🏪 Shop Closed",
                description="The Pirate Market is currently empty!",
                color=0xE67E22
            )
            await ctx.send(embed=embed)
            return

        embed = discord.Embed(
            title="🏪 PIRATE MARKET - Grand Line Goods",
            description="Acquire artifacts and tools to empower your pirate journey!\nUse `!buy <item name>` to purchase.",
            color=0x9B59B6
        )

        for item in items:
            embed.add_field(
                name=f"📦 {item['name']} — `{item['price']:,} 🍓`",
                value=f"**Effect:** *{item['effect']}*\n*{item['description']}*",
                inline=False
            )

        embed.set_footer(text="Berry Broker Market • Items provide passive raid bonuses & buffs")
        await ctx.send(embed=embed)

    @app_commands.command(name="shop", description="Browse items in the Pirate Market")
    async def shop_slash(self, interaction: discord.Interaction):
        items = get_all_items()
        if not items:
            embed = discord.Embed(
                title="🏪 Shop Closed",
                description="The Pirate Market is currently empty!",
                color=0xE67E22
            )
            await interaction.response.send_message(embed=embed)
            return

        embed = discord.Embed(
            title="🏪 PIRATE MARKET - Grand Line Goods",
            description="Acquire artifacts and tools to empower your pirate journey!\nUse `/buy <item name>` to purchase.",
            color=0x9B59B6
        )

        for item in items:
            embed.add_field(
                name=f"📦 {item['name']} — `{item['price']:,} 🍓`",
                value=f"**Effect:** *{item['effect']}*\n*{item['description']}*",
                inline=False
            )

        embed.set_footer(text="Berry Broker Market • Items provide passive raid bonuses & buffs")
        await interaction.response.send_message(embed=embed)

    @commands.command(name="buy", aliases=["purchase"])
    async def buy_cmd(self, ctx: commands.Context, *, item_name: str):
        """Purchase an item from the Pirate Market."""
        result = purchase_item(ctx.author.name, item_name)
        if not result["success"]:
            embed = discord.Embed(
                title="❌ Purchase Failed",
                description=result["message"],
                color=0xE74C3C
            )
            await ctx.send(embed=embed)
            return

        item = result["item"]
        embed = discord.Embed(
            title="✅ Purchase Successful!",
            description=(
                f"🎉 You purchased **{item['name']}**!\n\n"
                f"💰 **Cost:** `{item['price']:,} 🍓`\n"
                f"💼 **Remaining Wallet:** `{result['new_balance']:,} 🍓`\n"
                f"✨ **Effect:** *{item['effect']}*"
            ),
            color=0x2ECC71
        )
        await ctx.send(embed=embed)

    @app_commands.command(name="buy", description="Purchase an item from the Pirate Market")
    @app_commands.describe(item_name="The name of the item you want to buy")
    async def buy_slash(self, interaction: discord.Interaction, item_name: str):
        result = purchase_item(interaction.user.name, item_name)
        if not result["success"]:
            embed = discord.Embed(
                title="❌ Purchase Failed",
                description=result["message"],
                color=0xE74C3C
            )
            await interaction.response.send_message(embed=embed)
            return

        item = result["item"]
        embed = discord.Embed(
            title="✅ Purchase Successful!",
            description=(
                f"🎉 You purchased **{item['name']}**!\n\n"
                f"💰 **Cost:** `{item['price']:,} 🍓`\n"
                f"💼 **Remaining Wallet:** `{result['new_balance']:,} 🍓`\n"
                f"✨ **Effect:** *{item['effect']}*"
            ),
            color=0x2ECC71
        )
        await interaction.response.send_message(embed=embed)

    @commands.command(name="inventory", aliases=["inv", "bag"])
    async def inventory_cmd(self, ctx: commands.Context, member: discord.Member = None):
        """View your inventory or another pirate's inventory."""
        target = member or ctx.author
        items = get_user_inventory(target.name)
        balance = get_user_balance(target.name)

        if not items:
            embed = discord.Embed(
                title=f"🎒 {target.display_name}'s Inventory",
                description="This pirate's inventory is empty!\nVisit the shop with `!shop` to purchase items.",
                color=0xE67E22
            )
            await ctx.send(embed=embed)
            return

        embed = discord.Embed(
            title=f"🎒 {target.display_name}'s Inventory",
            description=f"💰 **Wallet:** `{balance['wallet']:,} 🍓` | 🏦 **Bank:** `{balance['bank']:,} 🍓`\n",
            color=0x3498DB
        )

        for item in items:
            status = "🟢 Active" if item["active"] else "⚪ Owned"
            embed.add_field(
                name=f"📦 {item['name']} (x{item['quantity']})",
                value=f"**Effect:** {item['effect'] or 'None'}\n**Status:** {status}",
                inline=True
            )

        await ctx.send(embed=embed)

    @app_commands.command(name="inventory", description="View your inventory")
    @app_commands.describe(member="The pirate whose inventory you want to view")
    async def inventory_slash(self, interaction: discord.Interaction, member: discord.Member = None):
        target = member or interaction.user
        items = get_user_inventory(target.name)
        balance = get_user_balance(target.name)

        if not items:
            embed = discord.Embed(
                title=f"🎒 {target.display_name}'s Inventory",
                description="This pirate's inventory is empty!\nVisit the shop with `/shop` to purchase items.",
                color=0xE67E22
            )
            await interaction.response.send_message(embed=embed)
            return

        embed = discord.Embed(
            title=f"🎒 {target.display_name}'s Inventory",
            description=f"💰 **Wallet:** `{balance['wallet']:,} 🍓` | 🏦 **Bank:** `{balance['bank']:,} 🍓`\n",
            color=0x3498DB
        )

        for item in items:
            status = "🟢 Active" if item["active"] else "⚪ Owned"
            embed.add_field(
                name=f"📦 {item['name']} (x{item['quantity']})",
                value=f"**Effect:** {item['effect'] or 'None'}\n**Status:** {status}",
                inline=True
            )

        await interaction.response.send_message(embed=embed)


class RaidCog(commands.Cog, name="Raid"):
    """Raid commands: Battle and plunder other pirates."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="raid", aliases=["rob", "plunder", "attack"])
    async def raid_cmd(self, ctx: commands.Context, member: discord.Member):
        """Raid another pirate and attempt to steal their berries!"""
        if ctx.author.id == member.id:
            embed = discord.Embed(
                title="❌ Invalid Target",
                description="You cannot raid yourself, ya fool!",
                color=0xE74C3C
            )
            await ctx.send(embed=embed)
            return

        result = attempt_raid(ctx.author.name, member.name)
        if not result.get("attempted", False):
            embed = discord.Embed(
                title="⚠ Raid Aborted",
                description=result.get("message", "Raid could not proceed."),
                color=0xE74C3C
            )
            await ctx.send(embed=embed)
            return

        if result["success"]:
            embed = discord.Embed(
                title="⚔️ VICTORY! Raid Succeeded! ⚔️",
                description=(
                    f"🏴‍☠️ **{ctx.author.display_name}** raided **{member.display_name}**'s ship and looted **+{result['amount']:,} 🍓**!\n\n"
                    f"💰 **Your New Wallet:** `{result['raider_new_balance']:,} 🍓`"
                ),
                color=0x2ECC71
            )
        else:
            embed = discord.Embed(
                title="💀 DEFEAT! Raid Failed! 💀",
                description=(
                    f"🛡️ **{member.display_name}** defended against **{ctx.author.display_name}**!\n"
                    f"💸 You lost **-{result['amount']:,} 🍓** in penalty to the defender.\n\n"
                    f"💰 **Your New Wallet:** `{result['raider_new_balance']:,} 🍓`"
                ),
                color=0xE74C3C
            )

        await ctx.send(embed=embed)

    @app_commands.command(name="raid", description="Raid another pirate and steal their berries")
    @app_commands.describe(member="The pirate to raid")
    async def raid_slash(self, interaction: discord.Interaction, member: discord.Member):
        if interaction.user.id == member.id:
            embed = discord.Embed(
                title="❌ Invalid Target",
                description="You cannot raid yourself, ya fool!",
                color=0xE74C3C
            )
            await interaction.response.send_message(embed=embed)
            return

        result = attempt_raid(interaction.user.name, member.name)
        if not result.get("attempted", False):
            embed = discord.Embed(
                title="⚠ Raid Aborted",
                description=result.get("message", "Raid could not proceed."),
                color=0xE74C3C
            )
            await interaction.response.send_message(embed=embed)
            return

        if result["success"]:
            embed = discord.Embed(
                title="⚔️ VICTORY! Raid Succeeded! ⚔️",
                description=(
                    f"🏴‍☠️ **{interaction.user.display_name}** raided **{member.display_name}**'s ship and looted **+{result['amount']:,} 🍓**!\n\n"
                    f"💰 **Your New Wallet:** `{result['raider_new_balance']:,} 🍓`"
                ),
                color=0x2ECC71
            )
        else:
            embed = discord.Embed(
                title="💀 DEFEAT! Raid Failed! 💀",
                description=(
                    f"🛡️ **{member.display_name}** defended against **{interaction.user.display_name}**!\n"
                    f"💸 You lost **-{result['amount']:,} 🍓** in penalty to the defender.\n\n"
                    f"💰 **Your New Wallet:** `{result['raider_new_balance']:,} 🍓`"
                ),
                color=0xE74C3C
            )

        await interaction.response.send_message(embed=embed)


class FunAndStatsCog(commands.Cog, name="Lore & Stats"):
    """One Piece lore, Leaderboard, and Transaction history."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="logpose", aliases=["lore", "op"])
    async def logpose_cmd(self, ctx: commands.Context):
        """Discover random One Piece lore from the Grand Line."""
        result = get_random_logpose()
        if not result or not result.get("success"):
            embed = discord.Embed(
                title="❌ Navigation Error",
                description="The Log Pose is spinning wildly! Try again later.",
                color=0xE74C3C
            )
            await ctx.send(embed=embed)
            return

        data = result["data"]
        embed = discord.Embed(
            title=f"🧭 Log Pose: {data['name']}",
            description=data["description"],
            color=0x1ABC9C
        )
        embed.set_author(name=f"Category: {data.get('category', 'Unknown').title()}")
        embed.set_footer(text="Grand Line Navigational Lore • One Piece")
        await ctx.send(embed=embed)

    @app_commands.command(name="logpose", description="Discover random One Piece lore")
    async def logpose_slash(self, interaction: discord.Interaction):
        result = get_random_logpose()
        if not result or not result.get("success"):
            embed = discord.Embed(
                title="❌ Navigation Error",
                description="The Log Pose is spinning wildly! Try again later.",
                color=0xE74C3C
            )
            await interaction.response.send_message(embed=embed)
            return

        data = result["data"]
        embed = discord.Embed(
            title=f"🧭 Log Pose: {data['name']}",
            description=data["description"],
            color=0x1ABC9C
        )
        embed.set_author(name=f"Category: {data.get('category', 'Unknown').title()}")
        embed.set_footer(text="Grand Line Navigational Lore • One Piece")
        await interaction.response.send_message(embed=embed)

    @commands.command(name="leaderboard", aliases=["lb", "top", "worstgeneration"])
    async def leaderboard_cmd(self, ctx: commands.Context):
        """View the richest pirates (Worst Generation leaderboard)."""
        leaders = get_leaderboard(limit=10)
        if not leaders:
            embed = discord.Embed(
                title="🏴‍☠️ Leaderboard Empty",
                description="No pirates have made their mark on the Grand Line yet.",
                color=0xE67E22
            )
            await ctx.send(embed=embed)
            return

        embed = discord.Embed(
            title="🏴‍☠️ WORST GENERATION - Leaderboard 🏴‍☠️",
            description="The most notorious and wealthy pirates across the seas:\n",
            color=0xF39C12
        )

        medals = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
        for idx, leader in enumerate(leaders):
            medal = medals[idx] if idx < len(medals) else f"#{idx+1}"
            embed.add_field(
                name=f"{medal} {leader['username']}",
                value=f"💰 **Total:** `{leader['total_wealth']:,} 🍓` *(Wallet: {leader['wallet']:,} | Bank: {leader['bank']:,})*",
                inline=False
            )

        embed.set_footer(text="Rise to the top by raiding, trading, and claiming bounties!")
        await ctx.send(embed=embed)

    @app_commands.command(name="leaderboard", description="View the Worst Generation leaderboard")
    async def leaderboard_slash(self, interaction: discord.Interaction):
        leaders = get_leaderboard(limit=10)
        if not leaders:
            embed = discord.Embed(
                title="🏴‍☠️ Leaderboard Empty",
                description="No pirates have made their mark on the Grand Line yet.",
                color=0xE67E22
            )
            await interaction.response.send_message(embed=embed)
            return

        embed = discord.Embed(
            title="🏴‍☠️ WORST GENERATION - Leaderboard 🏴‍☠️",
            description="The most notorious and wealthy pirates across the seas:\n",
            color=0xF39C12
        )

        medals = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
        for idx, leader in enumerate(leaders):
            medal = medals[idx] if idx < len(medals) else f"#{idx+1}"
            embed.add_field(
                name=f"{medal} {leader['username']}",
                value=f"💰 **Total:** `{leader['total_wealth']:,} 🍓` *(Wallet: {leader['wallet']:,} | Bank: {leader['bank']:,})*",
                inline=False
            )

        embed.set_footer(text="Rise to the top by raiding, trading, and claiming bounties!")
        await interaction.response.send_message(embed=embed)

    @commands.command(name="history", aliases=["logs", "transactions", "tx"])
    async def history_cmd(self, ctx: commands.Context, member: discord.Member = None):
        """View your recent transaction log."""
        target = member or ctx.author
        user = get_user(target.name)
        if not user:
            embed = discord.Embed(
                title="❌ Unknown Pirate",
                description="Pirate not found in the registry.",
                color=0xE74C3C
            )
            await ctx.send(embed=embed)
            return

        history = get_transaction_history(user["id"], limit=10)
        if not history:
            embed = discord.Embed(
                title=f"📜 {target.display_name}'s Ship Log",
                description="No transactions recorded yet!",
                color=0xE67E22
            )
            await ctx.send(embed=embed)
            return

        embed = discord.Embed(
            title=f"📜 {target.display_name}'s Transaction History",
            color=0x34495E
        )

        icons = {
            "daily": "⛵",
            "trade": "🤝",
            "raid_win": "⚔️",
            "raid_loss": "💀",
            "purchase": "🛒",
            "reward": "🎁"
        }

        for tx in history:
            icon = icons.get(tx["type"], "📌")
            sign = "+" if tx["amount"] > 0 else ""
            embed.add_field(
                name=f"{icon} {tx['type'].upper()} ({sign}{tx['amount']:,} 🍓)",
                value=f"*{tx['description']}*\n`{tx['timestamp'][:16]}`",
                inline=False
            )

        await ctx.send(embed=embed)

    @app_commands.command(name="history", description="View your transaction history")
    async def history_slash(self, interaction: discord.Interaction):
        user = get_user(interaction.user.name)
        if not user:
            embed = discord.Embed(
                title="❌ Unknown Pirate",
                description="Pirate not found in the registry.",
                color=0xE74C3C
            )
            await interaction.response.send_message(embed=embed)
            return

        history = get_transaction_history(user["id"], limit=10)
        if not history:
            embed = discord.Embed(
                title=f"📜 {interaction.user.display_name}'s Ship Log",
                description="No transactions recorded yet!",
                color=0xE67E22
            )
            await interaction.response.send_message(embed=embed)
            return

        embed = discord.Embed(
            title=f"📜 {interaction.user.display_name}'s Transaction History",
            color=0x34495E
        )

        icons = {
            "daily": "⛵",
            "trade": "🤝",
            "raid_win": "⚔️",
            "raid_loss": "💀",
            "purchase": "🛒",
            "reward": "🎁"
        }

        for tx in history:
            icon = icons.get(tx["type"], "📌")
            sign = "+" if tx["amount"] > 0 else ""
            embed.add_field(
                name=f"{icon} {tx['type'].upper()} ({sign}{tx['amount']:,} 🍓)",
                value=f"*{tx['description']}*\n`{tx['timestamp'][:16]}`",
                inline=False
            )

        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(EconomyCog(bot))
    await bot.add_cog(ShopCog(bot))
    await bot.add_cog(RaidCog(bot))
    await bot.add_cog(FunAndStatsCog(bot))
