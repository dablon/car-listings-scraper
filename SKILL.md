---
name: car-listings-scraper
description: "Scrape vehicle listings from Facebook Marketplace or TuCarro/MercadoLibre Colombia. Use when user wants to find cars/SUVs/4x4s by price, location, brand, or specs."
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

Find vehicles in Colombia from Facebook Marketplace or TuCarro.com.co.

## THE PROBLEM

**Facebook Marketplace blocks most automated access.** Direct requests return 400 errors. But there are workarounds.

## SOLUTION 1: Facebook Marketplace (via Google + Touch)

### Step 1 — Find listing IDs via Google

Use web_search to find indexed listings:

```
site:facebook.com/marketplace/item "Jeep Wrangler" Medellin
```

Collect the listing IDs (numeric IDs like `1543118877472637`).

### Step 2 — Fetch via touch.facebook.com

Facebook's mobile touch version is more permissive:

```bash
curl -A "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15..." \
  "https://touch.facebook.com/marketplace/item/1543118877472637/"
```

Extract from response:
- `og:title` → vehicle name
- `og:description` → basic details
- `og:image` → photo URL

### Step 3 — Parse Google snippets

Search snippets often contain:
- Price: `COP 75,000,000`
- Year: `2012`
- Km: `82 mil km`

### Step 4 — Known working patterns

These Facebook Marketplace listings work in Medellín:

| Model | Year | Price | Link |
|-------|------|-------|------|
| Jeep Wrangler | 2007 | $65.9M | marketplace/item/ (Rubicon 168K km) |
| Jeep Wrangler | 2010 | $75M | marketplace/item/ |
| Jeep Wrangler | 2014 | $98.9M | marketplace/item/ |
| Jeep Cherokee | 2015 | $54.9M | marketplace/item/ |

## SOLUTION 2: TuCarro.com.co (Guaranteed)

**TuCarro.com.co (MercadoLibre) never blocks scraping.**

### Step 1 — Search

```
site:articulo.tucarro.com.co "Jeep Wrangler" Medellin precio
```

### Step 2 — Extract URLs

Collect `articulo.tucarro.com.co/MCO-XXXXXXXX` URLs.

### Step 3 — Fetch details

```bash
curl "https://articulo.tucarro.com.co/MCO-3896512808" | grep -E '(price|year|km|HP|Motor)'
```

## Python Scripts

```bash
# Facebook Marketplace scraper
python3 scripts/scrape_facebook.py "Jeep Wrangler" --location Medellin

# TuCarro scraper  
python3 scripts/scrape_tucarro.py "Jeep Wrangler" --location Medellin --max-price 50000000
```

## Hard Rules

1. **Never invent data.** Only report what you actually fetched.
2. **web_fetch blocked?** → Try touch.facebook.com variant
3. **Google snippet has price/km?** → Report it
4. **HP not in snippet?** → Estimate from engine displacement
5. **TuCarro always works** → Prefer it when Facebook fails

## Sources That Work

| Source | URL Pattern | Status |
|--------|-------------|--------|
| TuCarro.com.co | `articulo.tucarro.com.co/MCO-*` | ✅ Always works |
| Facebook Touch | `touch.facebook.com/marketplace/item/*` | ⚠️ Sometimes works |
| Facebook Desktop | `facebook.com/marketplace/item/*` | ❌ Blocked |
| Google indexed snippets | `site:facebook.com/marketplace/item` | ✅ Works via web_search |

## Example Output

```
🚗 JEEP WRANGLER 2012 — 3.6L SPORT
🔗 https://www.facebook.com/marketplace/item/1543118877472637/
💰 Price: ~$79-95M COP (from snippet)
⚡ HP: 285 (estimated from 3.6L)
🛣️ Km: 82,000 km (from snippet)
📍 Location: Medellín

SOURCE: Google indexed snippet from Facebook Marketplace
```
