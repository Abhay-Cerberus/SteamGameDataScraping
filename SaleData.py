import requests
import csv
import time

# Settings
TOTAL_PAGES = 95
LIMIT = 1000
BASE_URL = "https://api.gamalytic.com/steam-games/list"
# Fields parameter: even though we only need some fields, we include more if desired.
FIELDS = "name,firstReleaseDate,earlyAccessExitDate,earlyAccess,copiesSold,price,revenue,avgPlaytime,reviewScore,publisherClass,publishers,developers,id,steamId,aiContent"
SORT = "copiesSold"
SORT_MODE = "desc"
OUTPUT_FILE = "gamalytic_steam_games.csv"

def fetch_page(page):
    """Fetch a single page of game data from the API."""
    params = {
        "fields": FIELDS,
        "page": page,
        "limit": LIMIT,
        "sort": SORT,
        "sort_mode": SORT_MODE
    }
    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching page {page}: {e}")
        return None

def main():
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["steamId", "price", "copiesSold", "publisherClass", "reviewScore", "aiContent"])
        writer.writeheader()
        
        for page in range(0, TOTAL_PAGES + 1):
            print(f"Processing page {page} of {TOTAL_PAGES}...")
            data = fetch_page(page)
            if data is None:
                print(f"Skipping page {page} due to error.")
                continue
            
            results = data.get("result", [])
            for game in results:
                row = {
                    "steamId": game.get("steamId", "N/A"),
                    "price": game.get("price", "N/A"),
                    "copiesSold": game.get("copiesSold", "N/A"),
                    "publisherClass": game.get("publisherClass", "N/A"),
                    "reviewScore": game.get("reviewScore", "N/A"),
                    "aiContent": game.get("aiContent", "N/A")
                }
                writer.writerow(row)
            
            # Wait a brief moment between pages to be safe.
            time.sleep(0.5)
            
    print(f"Extraction complete. Data saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
