#!/usr/bin/env python3
"""
TuCarro Scraper - Vehicle Listings from Colombian Marketplace
==========================================================
Scrape vehicle listings from TuCarro.com.co (MercadoLibre classifieds).
This is the alternative to blocked Facebook Marketplace.

Usage:
    python3 scrape_tucarro.py "Jeep Wrangler" Medellin --max-price 50000000
    python3 scrape_tucarro.py "BMW 335i" --year-min 2012 --hp-min 200
"""

import argparse
import json
import sys
import re
import urllib.parse
from datetime import datetime

try:
    import requests
except ImportError:
    print("Error: 'requests' library required. Install with: pip install requests")
    sys.exit(1)


class TuCarroScraper:
    """Scrape vehicle listings from TuCarro.com.co"""
    
    BASE_SEARCH_URL = "https://carros.tucarro.com.co/"
    BASE_ARTICLE_URL = "https://articulo.tucarro.com.co/"
    
    # Common HP by engine type (Colombian market reference)
    HP_REFERENCE = {
        "jeep_wrangler": {
            "3.6": 285,
            "3.8": 202,
            "2.0 turbo": 270,
        },
        "bmw": {
            "335i": 300,
            "328i": 245,
            "320i": 184,
            "530i": 258,
        },
        "audi": {
            "a6 3.0": 300,
            "a4 1.8": 190,
            "a4 2.0": 220,
        },
        "ford": {
            "escape 2.0": 245,
            "explorer 3.5": 290,
            "ranger 3.0": 200,
        }
    }
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "es-CO,es;q=0.9,en;q=0.8",
        })
    
    def search_listings(self, query, location=None, max_price=None, brand=None):
        """
        Search for vehicle listings.
        
        Args:
            query: Vehicle model/keyword (e.g., "Jeep Wrangler")
            location: City/location filter (e.g., "Medellin")
            max_price: Maximum price in COP
            brand: Brand filter (jeep, bmw, audi, ford, etc.)
        
        Returns:
            List of listing dictionaries with title, price, km, year, link
        """
        # Build search URL
        if brand:
            search_url = f"{self.BASE_SEARCH_URL}{brand}/"
        else:
            # Extract brand from query if possible
            query_lower = query.lower()
            for b in ["jeep", "bmw", "audi", "ford", "toyota", "mercedes", "honda", "nissan", "suzuki"]:
                if b in query_lower:
                    search_url = f"{self.BASE_SEARCH_URL}{b}/"
                    break
            else:
                search_url = f"{self.BASE_SEARCH_URL}"
        
        print(f"[INFO] Searching: {search_url}")
        print(f"[INFO] Query: {query}")
        
        listings = []
        
        try:
            response = self.session.get(search_url, timeout=10)
            response.raise_for_status()
            
            # Parse basic info from search page
            # Note: Full parsing requires BeautifulSoup which may not be installed
            # This is a simplified version
            
            # Try to find listings in the page
            text = response.text
            
            # Look for article IDs (MCO-XXXXXXXX format)
            article_ids = re.findall(r'MCO-\d+', text)
            article_ids = list(set(article_ids))  # Unique
            
            for article_id in article_ids[:20]:  # Limit to 20
                article_url = f"{self.BASE_ARTICLE_URL}{article_id}"
                listing = self.get_listing_details(article_url)
                if listing:
                    listings.append(listing)
                    
        except requests.RequestException as e:
            print(f"[ERROR] Search failed: {e}")
        
        return listings
    
    def get_listing_details(self, url):
        """
        Get details for a single listing.
        
        Returns:
            Dictionary with: title, price, year, km, hp, engine, transmission, 
                          drivetrain, location, extras, link
        """
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            text = response.text
            
            # Check if listing exists
            if "Publicación finalizada" in text:
                print(f"[WARN] Listing ended: {url}")
            
            # Extract price
            price_match = re.search(r'\$(\d{1,3}(?:\.\d{3})+)', text)
            price = price_match.group(1) if price_match else "N/A"
            
            # Extract year
            year_match = re.search(r'Año\s*</td><td>([^<]+)</td>', text)
            year = year_match.group(1) if year_match else "N/A"
            
            # Extract km
            km_match = re.search(r'(?:Kilómetros|km)\s*</td><td>([^<]+)</td>', text)
            km = km_match.group(1) if km_match else "N/A"
            
            # Extract engine/power
            hp_match = re.search(r'Potencia\s*</td><td>(\d+)\s*hp', text)
            hp = hp_match.group(1) if hp_match else None
            
            engine_match = re.search(r'Motor\s*</td><td>([^<]+)</td>', text)
            engine = engine_match.group(1) if engine_match else "N/A"
            
            # Extract transmission
            trans_match = re.search(r'Transmisión\s*</td><td>([^<]+)</td>', text)
            transmission = trans_match.group(1) if trans_match else "N/A"
            
            # Extract drivetrain (4x4, etc)
            drivetrain_match = re.search(r'(?:Control de tracción|Tracción)\s*</td><td>([^<]+)</td>', text)
            drivetrain = drivetrain_match.group(1) if drivetrain_match else "N/A"
            
            # Extract title/description
            title_match = re.search(r'<title>([^<]+)</title>', text)
            title = title_match.group(1) if title_match else "N/A"
            
            # Extract location
            location_patterns = [
                r'Medellín',
                r'Bogotá',
                r'Envigado',
                r'Sabaneta',
                r'Cali',
                r'Barranquilla',
            ]
            location = None
            for loc_pattern in location_patterns:
                if loc_pattern in text:
                    location = loc_pattern
                    break
            
            # Estimate HP if not provided
            if not hp and engine:
                hp = self._estimate_hp(engine, title)
            
            return {
                "title": title,
                "price": price,
                "year": year,
                "km": km,
                "hp": hp,
                "engine": engine,
                "transmission": transmission,
                "drivetrain": drivetrain,
                "location": location,
                "link": url
            }
            
        except requests.RequestException as e:
            print(f"[ERROR] Failed to fetch {url}: {e}")
            return None
    
    def _estimate_hp(self, engine, title):
        """Estimate HP based on engine type."""
        engine_lower = engine.lower() if engine else ""
        title_lower = title.lower() if title else ""
        
        text = engine_lower + " " + title_lower
        
        # Jeep Wrangler
        if "3.6" in text:
            return "285"
        elif "3.8" in text:
            return "202"
        elif "2.0 turbo" in text:
            return "270"
        
        # BMW
        elif "335i" in text:
            return "300"
        elif "328i" in text:
            return "245"
        elif "320i" in text:
            return "184"
        
        # Audi
        elif "a6 3.0" in text:
            return "300"
        elif "a4 1.8" in text:
            return "190"
        elif "a4 2.0" in text:
            return "220"
        
        # Ford
        elif "escape 2.0" in text:
            return "245"
        elif "explorer 3.5" in text:
            return "290"
        
        return "N/A"
    
    def format_output(self, listings, min_hp=None, max_price=None):
        """Format listings for display."""
        output = []
        output.append("=" * 80)
        output.append(f"TUCARRO SCRAPER RESULTS - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        output.append("=" * 80)
        output.append("")
        
        if not listings:
            output.append("No listings found.")
            return "\n".join(output)
        
        output.append(f"Found {len(listings)} listings")
        if min_hp:
            output.append(f"Filter: min HP = {min_hp}")
        if max_price:
            output.append(f"Filter: max price = {max_price:,} COP")
        output.append("")
        
        for i, listing in enumerate(listings, 1):
            output.append(f"{'─' * 80}")
            output.append(f"#{i}: {listing.get('title', 'N/A')}")
            output.append(f"{'─' * 80}")
            output.append(f"  💰 Price: {listing.get('price', 'N/A')}")
            output.append(f"  📅 Year: {listing.get('year', 'N/A')}")
            output.append(f"  🛣️  Km: {listing.get('km', 'N/A')}")
            output.append(f"  ⚡ HP: {listing.get('hp', 'N/A')}")
            output.append(f"  🔧 Engine: {listing.get('engine', 'N/A')}")
            output.append(f"  ⚙️  Transmission: {listing.get('transmission', 'N/A')}")
            output.append(f"  🧠 Drivetrain: {listing.get('drivetrain', 'N/A')}")
            output.append(f"  📍 Location: {listing.get('location', 'N/A')}")
            output.append(f"  🔗 Link: {listing.get('link', 'N/A')}")
            output.append("")
        
        return "\n".join(output)


def main():
    parser = argparse.ArgumentParser(
        description="Scrape vehicle listings from TuCarro.com.co"
    )
    parser.add_argument("query", help="Vehicle search query (e.g., 'Jeep Wrangler')")
    parser.add_argument("--location", "-l", help="Location filter (e.g., 'Medellin')")
    parser.add_argument("--max-price", "-p", type=int, help="Maximum price in COP")
    parser.add_argument("--brand", "-b", help="Brand filter (jeep, bmw, audi, ford, etc.)")
    parser.add_argument("--year-min", type=int, help="Minimum year")
    parser.add_argument("--hp-min", type=int, help="Minimum horsepower")
    parser.add_argument("--output", "-o", help="Output file (JSON)")
    parser.add_argument("--debug", action="store_true", help="Debug mode")
    
    args = parser.parse_args()
    
    scraper = TuCarroScraper()
    
    if args.debug:
        print(f"[DEBUG] Query: {args.query}")
        print(f"[DEBUG] Location: {args.location}")
        print(f"[DEBUG] Max price: {args.max_price}")
        print(f"[DEBUG] Brand: {args.brand}")
    
    print(f"\n[INFO] Searching for: {args.query}")
    if args.location:
        print(f"[INFO] Location: {args.location}")
    
    listings = scraper.search_listings(
        query=args.query,
        location=args.location,
        max_price=args.max_price,
        brand=args.brand
    )
    
    # Filter results
    filtered = listings
    if args.hp_min:
        filtered = [l for l in filtered if l.get('hp') and int(l['hp']) >= args.hp_min]
    if args.max_price:
        # Parse price and compare
        def parse_price(p):
            if not p or p == "N/A":
                return 999999999
            return int(p.replace(".", "").replace(",", ""))
        filtered = [l for l in filtered if parse_price(l.get('price')) <= args.max_price]
    
    # Output
    output = scraper.format_output(filtered, min_hp=args.hp_min, max_price=args.max_price)
    print(f"\n{output}")
    
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(filtered, f, indent=2)
        print(f"\n[INFO] Results saved to: {args.output}")


if __name__ == "__main__":
    main()
