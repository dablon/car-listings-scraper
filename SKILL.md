---
name: car-listings-scraper
description: "Scrape FB Marketplace Colombia for vehicles."
---

# Car Listings Scraper

## CONFIRMED METHOD

Use l.facebook.com (Facebook Lite).

1. Find IDs via web_search:
   site:facebook.com/marketplace/item "Jeep Wrangler" Medellin

2. Scrape:
curl -sL -A "Mozilla/5.0 (Linux; Android 10; SM-G960F)..."
  -H "Accept-Language: es-CO,es,en;q=0.9"
  "https://l.facebook.com/marketplace/item/{ID}/"

3. Parse: og:title, og:description, class=f3 price span

## Python Script

python3 scripts/scrape_facebook.py <listing_id>
python3 scripts/scrape_facebook.py 2303743683308429

## HARD RULES
1. Never fabricate data - only report what was fetched
2. HP is ESTIMATED from engine displacement - use hp_estimate field
3. Transmission inferred from "Caja mecanica"/"automática"
4. Drivetrain inferred from "4x4"/"4x2" keywords

## Sources
l.facebook.com - BEST (confirmed working)
touch.facebook.com - partial
Google site search - discovery only

## HP Reference (estimated)
3.6L V6 = 285 HP | 3.8L V6 = 202 HP | 3.2L V6 = 271 HP
2.0L Turbo = 270-285 HP | 1.4L = 95-97 HP | 1.3L = 85 HP

## Example Output
python3 scripts/scrape_facebook.py 2303743683308429
Returns: Suzuki Jimny 2014, $44.9M, 143,900km, Mecanica, 4x4
