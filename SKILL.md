---
name: car-listings-scraper
description: "Scrape vehicle listings from TuCarro/MercadoLibre Colombia by location, price, HP, and type. Alternative to blocked Facebook Marketplace."
metadata:
  openclaw:
    emoji: "🚗"
    requires:
      bins:
        - python3
        - curl
      pip:
        - requests
---

# Car Listings Scraper

Scrape vehicle listings from Colombian marketplaces. Use when user wants to find cars/SUVs/4x4s in Colombia by price, location, brand, or specs (HP, km).

## The Problem

**Facebook Marketplace blocks automated access.** Every attempt to scrape it fails — requests return 400 errors or blank pages. This is a hard blocker.

## The Solution

Use **TuCarro.com.co** instead. It's MercadoLibre's classifieds platform and has the **same listings** without blocking.

## Workflow

### Step 1 — Search for listings

Use `web_search` with TuCarro queries:

```
site:articulo.tucarro.com.co "Jeep Wrangler" Medellin precio
site:articulo.tucarro.com.co "BMW 335i" Medellin
site:articulo.tucarro.com.co "Audi A6" Medellin 2012
```

### Step 2 — Extract listing URLs

From search results, collect the `articulo.tucarro.com.co/MCO-XXXXXXXX` URLs.

### Step 3 — Fetch each listing

Use `web_fetch` with `maxChars=5000` on each URL:

```
web_fetch url="https://articulo.tucarro.com.co/MCO-XXXXXXXX" maxChars=5000
```

### Step 4 — Parse and present

Extract from the fetched HTML:
- **Price** — look for `$XX,XXX,XXX` patterns
- **Year** — look for `Año` table row
- **Km** — look for `Kilómetros` row
- **HP** — look for `Potencia` row (or estimate from engine displacement)
- **Engine** — look for `Motor` row
- **Transmission** — look for `Transmisión` row
- **Drivetrain** — look for `Control de tracción` or `Tracción`
- **Location** — city name in text

### Step 5 — Report with recommendation

For each vehicle:
- Model, year, price
- HP (✅ if meets requirement, ⚠️ if borderline, ❌ if below)
- Km, transmission, drivetrain
- Direct link to listing
- Recommendation comment

## Hard Rules

1. **Never invent data.** Only report what you actually fetched.
2. **web_fetch returning cookie notice?** → Page needs JavaScript, skip and try another URL.
3. **"Publicación finalizada" in text?** → Listing ended, still report specs if available.
4. **HP not in page?** → Estimate from engine displacement using the HP reference below.
5. **web_search returning no results?** → Try broader query without location filter.

## Sources

| Source | URL Pattern | Works? |
|--------|-------------|---------|
| TuCarro.com.co | `articulo.tucarro.com.co/MCO-*` | ✅ Yes |
| MercadoLibre Cars | `carros.mercadolibre.com.co` | ✅ Yes |
| Facebook Marketplace | `facebook.com/marketplace/item/*` | ❌ Blocked |

## Python Script (Optional)

For deeper scraping, use the included script:

```bash
# Install dependencies
pip install requests

# Search
python3 scripts/scrape_tucarro.py "Jeep Wrangler" --location Medellin --max-price 50000000

# Search with HP filter
python3 scripts/scrape_tucarro.py "BMW 335i" --hp-min 200 --max-price 60000000

# Save to JSON
python3 scripts/scrape_tucarro.py "Audi A6" --output results.json
```

## HP Quick Reference (Colombian Market)

| Model | Engine | HP |
|-------|--------|-----|
| Jeep Wrangler 3.6 | V6 3.6L | 285 |
| Jeep Wrangler 3.8 | V6 3.8L | 202 |
| BMW 335i | 3.0L N55 Biturbo | 300 |
| BMW 328i | 2.0L N20 Turbo | 245 |
| Audi A6 3.0 TFSI | V6 3.0L S/C | 300 |
| Ford Escape 2.0 EcoBoost | L4 2.0L Turbo | 245 |
| Toyota FJ Cruiser | V6 4.0L | 260 |

Full reference: `references/hp_guide.md`

## Example Output

```
🚗 JEEP WRANGLER 2012 — 3.6L SPORT
🔗 https://articulo.tucarro.com.co/MCO-3896512808
💰 Price: ~$79-108M COP
⚡ HP: 285 ✅ (exceeds 200 min)
🛣️ Km: 100,000
⚙️  Transmission: Automatic
🧠 Drivetrain: 4x4
📍 Location: Medellin

RECOMMENDATION: ⭐⭐⭐ TOP — Best option found
```
