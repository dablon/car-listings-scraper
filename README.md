# 🚗 Car Listings Scraper

**Scrape vehicle listings from Colombian marketplaces.**

> ⚠️ **Facebook Marketplace blocks automated access.** This tool uses TuCarro.com.co instead — the same listings, no blocking.

## Quick Start

### Web Search (any agent)

```bash
# Search for Jeep Wranglers in Medellin
web_search query="site:articulo.tucarro.com.co \"Jeep Wrangler\" Medellin precio"

# Get listing details
web_fetch url="https://articulo.tucarro.com.co/MCO-XXXXXXXX" maxChars=5000
```

### Python Script (local terminal)

```bash
# Install dependencies
pip install -r requirements.txt

# Search for vehicles
python3 scripts/scrape_tucarro.py "Jeep Wrangler" --location Medellin --max-price 50000000

# Filter by HP
python3 scripts/scrape_tucarro.py "BMW 335i" --hp-min 200 --max-price 60000000

# Save results to JSON
python3 scripts/scrape_tucarro.py "Audi A6" --output results.json
```

### Shell Wrapper

```bash
# Make executable
chmod +x scripts/search.sh

# Search
./scripts/search.sh "Jeep Wrangler" Medellin 50000000
./scripts/search.sh "BMW 335i" --hp-min 250
```

## Project Structure

```
car-listings-scraper/
├── SKILL.md              # Agent skill instructions
├── README.md             # This file
├── requirements.txt       # Python dependencies
├── scripts/
│   ├── scrape_tucarro.py # Main Python scraper
│   └── search.sh         # Shell wrapper
└── references/
    └── hp_guide.md       # HP reference for common Colombian vehicles
```

## Why TuCarro?

| Source | Status |
|--------|--------|
| Facebook Marketplace | ❌ Blocked |
| TuCarro.com.co | ✅ Works |
| MercadoLibre Cars | ✅ Works |

## Requirements

- Python 3.6+
- `requests` library
- `beautifulsoup4` and `lxml` (optional, for advanced parsing)

## License

MIT - Nicolas Alcaraz (@dablon)
