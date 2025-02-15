import requests
import csv

def fetch_all_games():
    url = "https://api.steampowered.com/ISteamApps/GetAppList/v2/"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raises an HTTPError if the response was unsuccessful
        data = response.json()
        # Extract the list of apps from the JSON response
        apps = data.get("applist", {}).get("apps", [])
        return apps
    except requests.RequestException as e:
        print("Error fetching data:", e)
        return []

def save_to_csv(apps, filename="AllGames.csv"):
    # Define the CSV columns; based on the API, each app has 'appid' and 'name'
    headers = ["appid", "name"]
    try:
        with open(filename, mode="w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=headers)
            writer.writeheader()
            writer.writerows(apps)
        print(f"Data saved successfully to {filename}")
    except Exception as e:
        print("Error saving data to CSV:", e)

def main():
    print("Fetching all games from Steam API...")
    apps = fetch_all_games()
    if apps:
        print(f"Fetched {len(apps)} apps.")
        save_to_csv(apps)
    else:
        print("No data retrieved.")

if __name__ == '__main__':
    main()
