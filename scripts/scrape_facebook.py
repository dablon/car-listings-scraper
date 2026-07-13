#!/usr/bin/env python3
"""
Facebook Marketplace Scraper
============================================
Scrape vehicle listings from Facebook Marketplace.

TECHNIQUE: Facebook blocks direct requests. We use:
1. Google indexed snippets via site:facebook.com/marketplace searches
2. Touch/mobile version (touch.facebook.com) which is more permissive
3. User-Agent spoofing as mobile browser

IMPORTANT: Facebook aggressively blocks scrapers. This works but may be rate-limited.
For heavy use, consider using the Graph API with a valid access token.

Usage:
    python3 scrape_facebook.py "Jeep Wrangler" Medellin --max-price 50000000
"""

import argparse
import json
import re
import sys
import urllib.parse
from datetime import datetime

try:
    import requests
except ImportError:
    print("Error: 'requests' library required. Install: pip install requests")
    sys.exit(1)


class FacebookMarketplaceScraper:
    """Scrape Facebook Marketplace listings."""
    
    # User agents for mobile spoofing
    MOBILE_UA = "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1"
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": self.MOBILE_UA,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "es-ES,es;q=0.9",
        })
    
    def search_via_google(self, query, location=None, max_price=None):
        """
        Search using Google indexed results.
        Returns listing data extracted from search snippets.
        
        Note: This doesn't require Facebook access - Google indexes Facebook listings.
        """
        listings = []
        
        # Build search query
        search_query = f'site:facebook.com/marketplace "{query}"'
        if location:
            search_query += f' "{location}"'
        if max_price:
            search_query += f' "{max_price}"'
        
        print(f"[INFO] Google search: {search_query}")
        print("[INFO] Note: Extract data from Google snippets (Facebook blocks direct scraping)")
        
        # Since we can't use Google Search API here, we'll return instructions
        # The agent should use web_search with this query pattern
        return {
            "method": "google_indexed_search",
            "query": search_query,
            "note": "Use web_search with this query to get indexed listings"
        }
    
    def get_listing_touch(self, listing_id):
        """
        Try to fetch listing via touch.facebook.com mobile version.
        Facebook is more permissive with mobile variants.
        
        listing_id: The numeric ID from the listing URL
        """
        url = f"https://touch.facebook.com/marketplace/item/{listing_id}/"
        
        try:
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                # Extract Open Graph meta tags (they're always present)
                data = self._extract_og_data(response.text)
                return data
            else:
                return {"error": f"HTTP {response.status_code}"}
                
        except requests.RequestException as e:
            return {"error": str(e)}
    
    def _extract_og_data(self, html):
        """Extract Open Graph data from HTML."""
        data = {}
        
        # og:title
        match = re.search(r'<meta property="og:title" content="([^"]+)"', html)
        if match:
            data["title"] = match.group(1)
        
        # og:description  
        match = re.search(r'<meta property="og:description" content="([^"]+)"', html)
        if match:
            data["description"] = match.group(1)
        
        # og:url
        match = re.search(r'<meta property="og:url" content="([^"]+)"', html)
        if match:
            data["url"] = match.group(1)
        
        # og:image
        match = re.search(r'<meta property="og:image" content="([^"]+)"', html)
        if match:
            data["image"] = match.group(1)
        
        return data
    
    def parse_search_snippet(self, snippet):
        """
        Parse a search result snippet for vehicle data.
        Extracts: price, year, km, location.
        """
        data = {}
        
        # Price patterns
        price_patterns = [
            r'COP\s*([\d.,]+)',
            r'\$([\d.,]+)\s*COP',
            r'([\d.,]+)\s*COP',
            r'\$\s*([\d.,]+)',
        ]
        for pattern in price_patterns:
            match = re.search(pattern, snippet)
            if match:
                data["price"] = match.group(1)
                break
        
        # Year patterns
        year_match = re.search(r'\b(19\d{2}|20[0-2]\d)\b', snippet)
        if year_match:
            data["year"] = year_match.group(1)
        
        # Km patterns
        km_patterns = [
            r'(\d+[Kk])\s*km',
            r'(\d+)\s*K\s*km',
            r'(\d+\.\d+)\s*K\s*km',
        ]
        for pattern in km_patterns:
            match = re.search(pattern, snippet)
            if match:
                data["km"] = match.group(1) + "km"
                break
        
        return data


def main():
    parser = argparse.ArgumentParser(
        description="Facebook Marketplace Scraper - Uses Google indexed snippets + mobile touch version"
    )
    parser.add_argument("query", help="Vehicle search query (e.g., 'Jeep Wrangler')")
    parser.add_argument("--location", "-l", help="Location filter (e.g., 'Medellin')")
    parser.add_argument("--max-price", "-p", type=int, help="Maximum price in COP")
    parser.add_argument("--listing-id", "-i", help="Direct listing ID to fetch")
    parser.add_argument("--output", "-o", help="Output file (JSON)")
    parser.add_argument("--debug", action="store_true", help="Debug mode")
    
    args = parser.parse_args()
    
    scraper = FacebookMarketplaceScraper()
    
    print("=" * 60)
    print("FACEBOOK MARKETPLACE SCRAPER")
    print("=" * 60)
    print()
    print("⚠️  IMPORTANT: Facebook blocks most automated requests.")
    print("    This tool uses TWO approaches:")
    print()
    print("    1. GOOGLE INDEXING: Use web_search with:")
    print(f'       site:facebook.com/marketplace "{args.query}"')
    if args.location:
        print(f'       "{args.location}"')
    print()
    print("    2. TOUCH VERSION: For specific listing IDs,")
    print("       try touch.facebook.com which is more permissive")
    print()
    
    if args.listing_id:
        # Try to fetch specific listing
        print(f"[INFO] Fetching listing: {args.listing_id}")
        result = scraper.get_listing_touch(args.listing_id)
        print(json.dumps(result, indent=2))
    else:
        # Return search instructions
        result = scraper.search_via_google(
            query=args.query,
            location=args.location,
            max_price=args.max_price
        )
        print(json.dumps(result, indent=2))
    
    print()
    print("=" * 60)
    print("RECOMMENDED WORKFLOW FOR AGENTS:")
    print("=" * 60)
    print("""
1. Use web_search to find listings:
   web_search query='site:facebook.com/marketplace/item "Jeep Wrangler" Medellin'

2. From results, collect listing IDs (numbers like 1543118877472637)

3. Try touch.facebook.com with each ID:
   curl -A "Mozilla/5.0 (iPhone;...)" "https://touch.facebook.com/marketplace/item/ID/"

4. Extract og:title, og:description from the HTML

5. For full details, use Google cached snippets which often contain
   price, year, km from the original listing description
""")


if __name__ == "__main__":
    main()
