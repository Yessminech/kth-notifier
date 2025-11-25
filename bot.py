import requests
import telegram
import json
import os
from datetime import datetime

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = telegram.Bot(token=BOT_TOKEN)

API_PAGE = "https://kth-exjobb.powerappsportals.com/en-US/#"
STATE_FILE = "seen.json"

if not os.path.exists(STATE_FILE):
    with open(STATE_FILE, "w") as f:
        json.dump([], f)

def load_seen():
    try:
        with open(STATE_FILE) as f:
            return set(json.load(f))
    except:
        return set()

def save_seen(seen):
    with open(STATE_FILE, "w") as f:
        json.dump(list(seen), f)

def find_api_endpoint():
    html = requests.get(API_PAGE).text
    if "entity/list/" not in html:
        return None
    part = html.split("entity/list/")[1].split('"')[0]
    return "https://kth-exjobb.powerappsportals.com/_services/entity/list/" + part

def fetch_offers():
    endpoint = find_api_endpoint()
    if not endpoint:
        return []
    data = requests.get(endpoint).json()
    offers = []
    for row in data.get("value", []):
        title = row.get("adx_name")
        url = row.get("adx_url")
        offers.append((title, url))
    return offers

def run():
    print("🔍 Starting KTH Offer Check...")

    seen = load_seen()
    print(f"Seen offers so far: {len(seen)}")

    offers = fetch_offers()

    if not offers:
        print("⚠️ No offers fetched. Possibly API changed or blocked.")
        return

    print(f"Fetched {len(offers)} offers from portal.")

    new_offers = []

    for title, url in offers:
        if title not in seen:
            new_offers.append((title, url))

    if not new_offers:
        print("ℹ️ No new offers found.")
    else:
        print(f"🔥 {len(new_offers)} new offer(s) found. Sending notifications...")

    for title, url in new_offers:
        msg = f"🔥 New KTH thesis offer:\n\n{title}\n➡️ {url}"
        bot.send_message(chat_id=CHAT_ID, text=msg)
        seen.add(title)
        print(f"📩 Sent: {title}")

    save_seen(seen)
    print("✅ Finished run.")


if __name__ == "__main__":
    run()