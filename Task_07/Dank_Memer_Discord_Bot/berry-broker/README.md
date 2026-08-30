# ⚓ Berry Broker — One Piece Pirate Economy Discord Bot

Berry Broker is a One Piece themed economy and piracy simulator Discord Bot built with `discord.py` and SQLite. Engage in piratical adventures across the Grand Line: claim daily bounties, trade berries, purchase artifacts from the Pirate Market, raid rival pirates, discover One Piece lore, and climb the Worst Generation leaderboard!

---

## 🚀 Features

- 💰 **Pirate Economy**: Check your bounty poster, wallet, and bank reserves.
- ⛵ **Daily Plunder (`!daily`)**: Set sail once every 24 hours to plunder merchant ships for berries.
- 🤝 **Secure Berry Trading (`!trade`)**: Atomic berry transfers between pirates with full ledger records.
- 🏪 **Pirate Market (`!shop`, `!buy`)**: Acquire items with passive buffs:
  - **Berry Compass**: +10% raid success rate
  - **Lucky Dice**: +15% gambling bonus
  - **Sea Stone**: Raid protection (decreases incoming raid success)
  - **Log Pose**: Navigational artifact for special lore & raids
  - **Vivre Card**: +5% trade success
- 🎒 **Inventory (`!inventory`)**: Track your artifacts and active boosts.
- ⚔️ **Pirate Raids (`!raid`)**: Battle rival pirates in real-time to steal berries (with item modifier calculations and safety checks).
- 🧭 **Log Pose Lore (`!logpose`)**: Explore lore entries from the One Piece universe.
- 🏆 **Worst Generation Leaderboard (`!leaderboard`)**: Compete with other pirates to top the bounty rankings.
- 📜 **Transaction History (`!history`)**: Transparent ship log of all trades, plunders, purchases, and raid battles.

---

## 📂 Project Structure

```
berry-broker/
├── bot.py                     # Main application entry point (Discord Bot & CLI runner)
├── config.py                  # Environment configurations and game balance settings
├── requirements.txt           # Python dependencies
├── README.md                  # Documentation and guide
├── .env                       # Environment variables (Discord token, DB path, etc.)
├── .gitignore                 # Git ignore rules
│
├── database/
│   ├── __init__.py
│   ├── connection.py          # SQLite connection manager with foreign key enforcement
│   ├── schema.py              # Table definitions and auto-seed migrations
│   └── queries.py             # Reusable database queries & transactions
│
├── commands/
│   ├── __init__.py            # Command exports for CLI and Discord
│   ├── discord_cogs.py        # Discord prefix & slash command Cogs
│   ├── economy.py             # Terminal economy command handlers
│   ├── shop.py                # Terminal shop command handlers
│   ├── raid.py                # Terminal raid command handlers
│   └── fun.py                 # Terminal lore & leaderboard handlers
│
├── services/
│   ├── __init__.py            # Service layer exports
│   ├── economy_service.py     # Pure business logic for wallets, claims & transfers
│   ├── shop_service.py        # Shop purchase and inventory logic
│   ├── raid_service.py        # Raid calculations, probabilities, and balances
│   └── onepiece_api.py        # One Piece lore retriever
│
├── utils/
│   ├── __init__.py
│   ├── cooldowns.py           # Cooldown calculator and formatter
│   └── helpers.py             # String, emoji, and formatting helpers
│
└── data/
    └── shop_items.py          # Shop item seed definitions
```

---

## 🛠️ Installation & Setup

1. **Clone the repository and navigate to `berry-broker`**:
   ```bash
   cd berry-broker
   ```

2. **Set up a Virtual Environment**:
   ```bash
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # Linux/macOS:
   source .venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure `.env`**:
   Add your Discord Bot Token to `.env`:
   ```env
   DISCORD_TOKEN=your_discord_bot_token_here
   DATABASE_PATH=berry_broker.db
   ENVIRONMENT=development
   ```

---

## 🎮 Running the Bot

### 🤖 Run Discord Bot
```bash
python bot.py
```
This connects to Discord, syncs slash commands, and listens for both `!` prefix and `/` slash commands.

### 💻 Run Terminal CLI Mode
```bash
python bot.py --cli
```
Run the fully interactive Rich terminal UI without needing an active Discord connection.

---

## 📜 Discord Commands Reference

| Prefix Command | Slash Command | Description |
|---|---|---|
| `!bounty [@user]` | `/bounty [member]` | View bounty wanted poster, wallet, and bank balance |
| `!daily` | `/daily` | Claim 24-hour daily berry plunder |
| `!trade <@user> <amt>` | `/trade <member> <amt>` | Send berries to another pirate |
| `!shop` | `/shop` | View the Pirate Market items & buffs |
| `!buy <item_name>` | `/buy <item_name>` | Purchase an item from the market |
| `!inventory [@user]` | `/inventory [member]` | Inspect owned items and buffs |
| `!raid <@user>` | `/raid <member>` | Attempt a raid on a rival pirate's wallet |
| `!logpose` | `/logpose` | Receive random One Piece lore |
| `!leaderboard` | `/leaderboard` | View top 10 Worst Generation richest pirates |
| `!history [@user]` | `/history` | View recent transaction logs |
| `!help` | N/A | Display complete help menu |
