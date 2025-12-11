# 🎣 Discord Fishing Bot

A feature-rich Discord fishing bot built with Node.js, TypeScript, and discord.js v14. Catch fish, upgrade your rod, build your collection, and compete on the leaderboards!

## ✨ Features

- 🎣 **Fishing System**: Cast your rod with cooldowns and catch fish of varying rarities
- 🐟 **6 Rarity Tiers**: Common, Uncommon, Rare, Epic, Legendary, and Mythic fish
- 🎨 **Custom Emojis**: Fully configurable emoji mappings for fish and rods
- 💰 **Economy System**: Earn and spend "Scales" currency
- 📦 **Inventory Management**: Store and manage your fish collection
- ⬆️ **Rod Upgrades**: Progress through 5 rod tiers with improved catch rates
- 🛒 **Shop System**: Purchase passive upgrades to boost your fishing
- 🏆 **Leaderboards**: Compete for richest, most catches, and highest rod tier
- ⚡ **Golden Bite Events**: Random bonus events that double fish value
- 🔒 **Persistent Data**: Each user's progress saved in individual JSON files
- 👑 **Admin Commands**: Customize emojis, cooldowns, and catch rates without code changes

## 📋 Requirements

- Node.js 18 or higher (LTS recommended)
- A Discord Bot Token ([Get one here](https://discord.com/developers/applications))
- npm or yarn package manager

## 🚀 Quick Start

### 1. Clone and Install

\`\`\`bash
# Clone the repository
git clone <repository-url>
cd discord-fishing-bot

# Install dependencies
npm install
\`\`\`

### 2. Configure Environment

Create a `.env` file in the root directory:

\`\`\`env
DISCORD_TOKEN=your_bot_token_here
CLIENT_ID=your_application_client_id
GUILD_ID=your_test_guild_id_optional
\`\`\`

**How to get these values:**

- **DISCORD_TOKEN**: Go to [Discord Developer Portal](https://discord.com/developers/applications) → Your App → Bot → Token
- **CLIENT_ID**: Your App → General Information → Application ID
- **GUILD_ID** (optional): Right-click your server in Discord → Copy Server ID (enables Developer Mode in Discord settings first)

### 3. Register Slash Commands

\`\`\`bash
# Register commands (required before first run)
npm run register
\`\`\`

**Note:** If you set `GUILD_ID`, commands appear instantly in that server. Without it, commands are registered globally and may take up to 1 hour to appear.

### 4. Start the Bot

\`\`\`bash
# Development mode (auto-restart on changes)
npm run dev

# Production mode
npm run build
npm start
\`\`\`

## 🎮 Commands

### User Commands

| Command | Description |
|---------|-------------|
| `/fish` | Cast your rod and try to catch a fish (45s cooldown) |
| `/balance` | Check your current currency balance |
| `/inventory` | View all fish in your inventory with values |
| `/sell <type>` | Sell fish (all, or by rarity) |
| `/rod` | View your current rod and upgrade information |
| `/upgrade` | Upgrade to the next rod tier |
| `/shop` | View available passive upgrades |
| `/buy <upgrade>` | Purchase a passive upgrade |
| `/leaderboard <type>` | View server leaderboards (richest/catches/rod) |

### Admin Commands

Requires "Manage Server" permission:

| Command | Description |
|---------|-------------|
| `/setemojis` | Update emoji mappings for fish and rods |
| `/setcooldown <seconds>` | Change fishing cooldown duration |
| `/setrates <rod> <rarity> <weight>` | Adjust catch rates for specific rarities |

## 🎣 Rod Tiers

Progress through 5 rod tiers, each improving your catch rates:

1. **Wood** 🎣 - Starter rod (free)
2. **Fiberglass** 🎣 - 500 Scales
3. **Steel** ⚔️ - 2,000 Scales
4. **Titanium** ⚡ - 8,000 Scales
5. **Mythic** ✨ - 30,000 Scales

Higher tier rods significantly increase your chances of catching rare and legendary fish!

## 🐟 Fish Rarities

| Rarity | Base Value | Examples |
|--------|-----------|----------|
| **Common** | 10 Scales | Salmon, Carp, Anchovy |
| **Uncommon** | 30 Scales | Trout, Bass |
| **Rare** | 80 Scales | Tuna, Puffer |
| **Epic** | 200 Scales | Swordfish |
| **Legendary** | 500 Scales | Shark |
| **Mythic** | 1,500 Scales | Leviathan |

## ⚙️ Configuration

### Custom Emojis

Edit `config/emoji.json` to customize fish and rod emojis. You can use:
- Unicode emojis: `"🐟"`
- Custom server emojis: `"<:emoji_name:123456789>"`
- Animated emojis: `"<a:emoji_name:123456789>"`

### Catch Rates

Adjust rarity weights in `config/rates.json`. Higher weights = more common catches. Weights are per rod tier.

### General Settings

Modify `config/settings.json` for:
- Cooldown duration
- Currency name
- Fish base values
- Golden Bite chance
- Upgrade costs and effects

## 📁 Project Structure

\`\`\`
discord-fishing-bot/
├── src/
│   ├── commands/          # All slash command implementations
│   │   ├── fish.ts
│   │   ├── balance.ts
│   │   ├── sell.ts
│   │   ├── inventory.ts
│   │   ├── upgrade.ts
│   │   ├── rod.ts
│   │   ├── shop.ts
│   │   ├── buy.ts
│   │   ├── leaderboard.ts
│   │   └── [admin commands]
│   ├── lib/               # Core functionality
│   │   ├── config.ts      # Environment configuration
│   │   ├── persistence.ts # User data loading/saving
│   │   ├── fishing.ts     # Fishing mechanics & RNG
│   │   ├── economy.ts     # Currency calculations
│   │   ├── emojis.ts      # Emoji management
│   │   ├── leaderboards.ts # Ranking system
│   │   └── validation.ts  # Permission checks
│   ├── index.ts           # Bot initialization
│   ├── register-commands.ts # Command registration
│   └── types.ts           # TypeScript definitions
├── config/                # Configuration files
│   ├── emoji.json
│   ├── rates.json
│   └── settings.json
├── data/                  # User data (auto-created)
│   └── [user-id].json
├── .env                   # Environment variables
├── package.json
├── tsconfig.json
└── README.md
\`\`\`

## 🔧 Development

\`\`\`bash
# Run in development mode with auto-reload
npm run dev

# Build TypeScript to JavaScript
npm run build

# Run linter
npm run lint
\`\`\`

## 🐛 Troubleshooting

### Commands not appearing

- Make sure you ran `npm run register`
- Global commands take up to 1 hour; use `GUILD_ID` for instant testing
- Check bot has `applications.commands` scope

### Permission errors

- Bot needs these permissions: Send Messages, Embed Links, Use Slash Commands
- Admin commands require "Manage Server" permission

### Data corruption

- The bot automatically backs up corrupted files with `.backup-[timestamp]` suffix
- Corrupted user data is reset automatically with a console warning

## 📊 Data Persistence

User data is stored in `data/<user-id>.json` files with atomic writes to prevent corruption. Each file contains:

- Currency balance
- Rod tier and level
- Passive upgrade levels
- Total catches and last fish timestamp
- Complete inventory (fish counts by rarity)

## 🚀 Deployment

### Production Checklist

1. Set `NODE_ENV=production` in `.env`
2. Remove `GUILD_ID` for global command registration
3. Run `npm run build` before starting
4. Use a process manager like PM2:

\`\`\`bash
npm install -g pm2
pm2 start dist/index.js --name fishing-bot
pm2 save
\`\`\`

### Hosting Options

- [Railway](https://railway.app/)
- [Heroku](https://www.heroku.com/)
- [DigitalOcean App Platform](https://www.digitalocean.com/products/app-platform)
- Any VPS with Node.js support

## 📝 License

MIT License - feel free to modify and use for your own Discord servers!

## 🤝 Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

## 💡 Future Ideas

- [ ] Trading system between players
- [ ] Fishing tournaments with prizes
- [ ] Bait system for targeted fishing
- [ ] Aquarium to display your best catches
- [ ] Seasonal events with limited-time fish
- [ ] Fishing locations with unique fish pools

---

**Happy Fishing! 🎣**
