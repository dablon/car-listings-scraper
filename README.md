# Car Listings Scraper

Scrape vehicle listings from Colombian marketplaces. **Facebook Marketplace blocks automated access**, so this skill uses TuCarro.com.co instead — it's MercadoLibre's classifieds platform with the same listings, no blocking.

## Quick Start

```bash
# Find Jeep Wranglers in Medellin
web_search query="site:articulo.tucarro.com.co \"Jeep Wrangler\" Medellin precio"

# Fetch a specific listing
web_fetch url="https://articulo.tucarro.com.co/MCO-XXXXXXXX" maxChars=5000
```

## Sources

| Source | URL Pattern | Works? |
|--------|-------------|--------|
| TuCarro.com.co | `articulo.tucarro.com.co/MCO-*` | ✅ Yes |
| MercadoLibre Cars | `carros.mercadolibre.com.co` | ✅ Yes |
| Facebook Marketplace | `facebook.com/marketplace/item/*` | ❌ Blocked |

## Common HP reference (Colombian market)

| Model | Engine | HP |
|-------|--------|-----|
| Jeep Wrangler 3.6 | V6 3.6L | 285 HP |
| Jeep Wrangler 3.8 | V6 3.8L | 202 HP |
| Jeep Wrangler 2.0 Turbo | L4 2.0L Turbo | 270-285 HP |
| BMW 335i (F30) | 3.0L N55 Biturbo | 300 HP |
| BMW 328i (F30) | 2.0L N20 TwinPower | 245 HP |
| Audi A6 3.0 TFSI | V6 3.0L S/C | 300 HP |
| Ford Escape 2.0 EcoBoost | L4 2.0L Turbo | 245 HP |
