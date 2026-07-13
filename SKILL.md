---
name: facebook-marketplace-scraper
description: "Scrape any listing from FB Marketplace via l.facebook.com. Extract title, price, description."
---

# Facebook Marketplace Scraper

## Method: l.facebook.com

FB blocks direct access. Use Facebook Lite redirect.

### Step 1 — Find Listing IDs

Discovery via web_search:
site:facebook.com/marketplace/item "keyword" city

Examples:
site:facebook.com/marketplace/item "iPhone" Bogota
site:facebook.com/marketplace/item "PS5" Colombia

Extract numeric ID from URL:
facebook.com/marketplace/item/1234567890/ -> ID: 1234567890

### Step 2 — Scrape the Listing

curl -s -L \
  -A "Mozilla/5.0 (Linux; Android 10; SM-G960F) AppleWebKit/537.36"
  -H "Accept-Language: es-CO,es,en;q=0.9" \
  "https://l.facebook.com/marketplace/item/{ID}/"

### Step 3 — Parse

og:title -> title
og:description -> description
class="f3" span -> price (often "X por articulo")
Listed in ... -> location

## Python Script

python3 scripts/scrape_facebook.py <listing_id>
python3 scripts/scrape_facebook.py 2303743683308429

## HARD RULES

1. Never fabricate data - only report what was fetched
2. Price from class="f3" span often contains "por articulo" - strip if needed
3. Description may be empty for some listings - handle gracefully
4. Always include the listing link in output

## Output Format

json with fields: id, title, price, year, km, engine,
transmission, drivetrain, hp_estimate, location,
description, link, source

Note: vehicle-specific fields (km, transmission, drivetrain)
may be empty for non-vehicle items.

## Alternative

TuCarro fallback:
python3 scripts/scrape_tucarro.py "terms" --location City --max-price 50000000

## Sources

l.facebook.com - BEST (confirmed working)
touch.facebook.com - partial
Google site search - discovery only
