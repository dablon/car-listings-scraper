---
name: car-listings-scraper
description: "Scrape vehicle listings from TuCarro/MercadoLibre Colombia by location, price, HP, and type. Alternative to blocked Facebook Marketplace."
---

# Car Listings Scraper

Scrape vehicle listings from Colombian marketplaces. Use when user wants to find cars/SUVs/4x4s in Colombia by price, location, brand, or specs (HP, km).

## Approach

**Facebook Marketplace blocks automated access.** Use TuCarro.com.co instead — it's MercadoLibre's classifieds platform and has the same listings without blocking.

### Step 1 — Find listings

Use `web_search` with TuCarro queries:

```
site:articulo.tucarro.com.co "KEYWORD" Medellin precio
```

Common search patterns:
```
site:articulo.tucarro.com.co "Jeep Wrangler" Medellin
site:articulo.tucarro.com.co "BMW 335i" Medellin
site:articulo.tucarro.com.co "Audi A6" Medellin
```

TuCarro URL patterns:
```
https://carros.tucarro.com.co/jeep/wrangler/
https://carros.tucarro.com.co/bmw/series-3/
https://carros.tucarro.com.co/medellin/suv/
```

### Step 2 — Extract listing details

Once you have an `articulo.tucarro.com.co` URL, use `web_fetch` with `maxChars=5000` to get:
- Price
- Year, km, HP, engine
- Transmission, drivetrain
- Location
- Extras/description

### Step 3 — Present results

For each vehicle include:
- Model, year, price
- HP (look for "Potencia" field)
- Km
- Link to listing
- Recommendation (✅/⚠️/❌ based on HP requirements and price)

## Hard rules

- Never invent listing data. Only report what you actually fetched.
- If web_fetch returns "Al navegar en este sitio aceptas las cookies", the page requires JavaScript — skip it and try a different listing URL.
- If a listing shows "Publicación finalizada", note it but still report specs.
- Always specify HP range for the engine type (e.g., Jeep Wrangler 3.6 = 285 HP, 3.8 = 202 HP).

## Sources that work

| Source | URL Pattern | Works? |
|--------|-------------|--------|
| TuCarro.com.co | `articulo.tucarro.com.co/MCO-*` | ✅ Yes |
| MercadoLibre Cars | `carros.mercadolibre.com.co` | ✅ Yes |
| Facebook Marketplace | `facebook.com/marketplace/item/*` | ❌ Blocked |

## Example workflow

1. `web_search`: "site:articulo.tucarro.com.co Jeep Wrangler Medellin 2012 precio"
2. Find listing URL from results
3. `web_fetch` the URL to get full specs
4. Report with HP, price, km, recommendation
