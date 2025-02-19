import os
import requests
import csv
import time
from pandas import read_csv

# Rate limiting: 200 requests per 5 minutes means ~1 request per 1.5 seconds.
DELAY = 1.1
MAX_RETRIES = 10
PROCESSED_FILE = "processed_appids.txt"
ERRORED_FILE = "errored_appids.txt"

def get_app_details(appid, max_retries=MAX_RETRIES):
    """
    Queries the Steam Store API for details about the given appid.
    Retries up to max_retries on network errors.
    Returns the inner "data" dictionary if successful; otherwise, returns None.
    """
    url = f"https://store.steampowered.com/api/appdetails/?appids={appid}&cc=us&l=en"
    attempt = 0
    while attempt < max_retries:
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            app_entry = data.get(str(appid))
            if app_entry and app_entry.get("success"):
                return app_entry.get("data")
            else:
                print(f"No valid data for AppID {appid}.")
                return None
        except requests.RequestException as e:
            attempt += 1
            print(f"Error fetching data for AppID {appid} (attempt {attempt}/{max_retries}): {e}")
            if attempt == max_retries:
                with open(ERRORED_FILE, mode="a", encoding="utf-8") as fail:
                    fail.write(f"{appid},\n")
            else:
                time.sleep(DELAY)
    return None

def extract_base_game_details(details):
    """
    Extracts details for a base game.
    Returns a dictionary with the desired fields and a default 'dlcs' value (0).
    """
    return {
        "steam_appid": details.get("steam_appid", "N/A"),
        "name": details.get("name", "N/A"),
        "windows": details.get("platforms", {}).get("windows", False),
        "mac": details.get("platforms", {}).get("mac", False),
        "linux": details.get("platforms", {}).get("linux", False),
        "metacritic": details.get("metacritic", {}).get("score", "N/A"),
        "steam_achievements": any(cat.get("description", "").strip() == "Steam Achievements" for cat in details.get("categories", [])),
        "steam_trading_cards": any(cat.get("description", "").strip() == "Steam Trading Cards" for cat in details.get("categories", [])),
        "workshop_support": any(cat.get("description", "").strip() == "Steam Workshop" for cat in details.get("categories", [])),
        "genres": ", ".join([g.get("description", "").strip() for g in details.get("genres", [])]) if details.get("genres") else "N/A",
        "achievements_total": details.get("achievements", {}).get("total", "N/A"),
        "release_date": details.get("release_date", {}).get("date", "N/A"),
        "dlcs": 0  # Base games start with 0 DLCs; note: without in‑memory aggregation, this value will remain 0.
    }

def append_to_csv(record, filename, headers):
    """
    Opens the CSV file in append mode (or write mode if it doesn't exist)
    and writes the record. Writes the header if the file is new.
    """
    mode = "a" if os.path.exists(filename) else "w"
    try:
        with open(filename, mode=mode, newline='', encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            if mode == "w":
                writer.writeheader()
            writer.writerow(record)
        print(f"Appended record to {filename}.")
    except Exception as e:
        print(f"Error saving to {filename}: {e}")

def log_processed_appid(appid):
    """Appends a successfully processed appid to processed_appids.txt."""
    try:
        with open(PROCESSED_FILE, mode="a", encoding="utf-8") as f:
            f.write(f"{appid},\n")
    except Exception as e:
        print(f"Error writing appid {appid} to {PROCESSED_FILE}: {e}")

def main():
    # Read the list of appids from a CSV file (e.g., "my_appids.csv").
    # The CSV file must have a column named "appid".
    file_name = input("Enter file name (without .csv): ")
    df = read_csv(file_name + ".csv")
    appids = df["appid"].tolist()
    total_apps = len(appids)
    print(f"Processing {total_apps} app(s)...")

    # Define headers for each CSV file.
    base_headers = ["steam_appid", "name", "windows", "mac", "linux", "metacritic",
                    "steam_achievements", "steam_trading_cards", "workshop_support",
                    "genres", "achievements_total", "release_date", "dlcs"]
    dlc_headers = ["dlc_appid", "base_appid", "name"]
    demo_headers = ["demo_appid", "full_game_appid", "name"]

    for idx, appid in enumerate(appids, start=1):
        print(f"\nProcessing {idx}/{total_apps}: AppID {appid}...")
        details = get_app_details(appid)
        if not details:
            print(f"Skipping AppID {appid} due to missing data.")
            time.sleep(DELAY)
            continue

        log_processed_appid(appid)
        app_type = details.get("type", "").lower()

        if app_type == "dlc":
            fullgame = details.get("fullgame")
            if fullgame and fullgame.get("appid"):
                base_appid = str(fullgame.get("appid")).strip()
                record = {
                    "dlc_appid": details.get("steam_appid", "N/A"),
                    "base_appid": base_appid,
                    "name": details.get("name", "N/A")
                }
                append_to_csv(record, "dlcs.csv", dlc_headers)
                print(f"Processed DLC (AppID {appid}) for base game {base_appid}.")
            else:
                print(f"DLC {appid} missing valid 'fullgame' info; skipping.")
        elif app_type == "demo":
            fullgame = details.get("fullgame")
            if fullgame and fullgame.get("appid"):
                record = {
                    "demo_appid": details.get("steam_appid", "N/A"),
                    "full_game_appid": str(fullgame.get("appid")).strip(),
                    "name": details.get("name", "N/A")
                }
                append_to_csv(record, "demos.csv", demo_headers)
                print(f"Processed demo (AppID {appid}).")
            else:
                print(f"Demo {appid} missing valid 'fullgame' info; skipping.")
        elif app_type == "game":
            record = extract_base_game_details(details)
            append_to_csv(record, "base_games.csv", base_headers)
            print(f"Processed base game (AppID {appid}).")
        else:
            print(f"Skipping AppID {appid} with unknown type '{app_type}'.")

        time.sleep(DELAY)

    print("Processing complete.")

if __name__ == "__main__":
    main()
