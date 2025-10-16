import requests
import json
import time
from låturl import urls

url = "https://api.firecrawl.dev/v2/scrape"

# headers = {
#     "Authorization": "Bearer fc-666b0b20fdcb43da90e8a0cc21aeb350",
#     "Content-Type": "application/json"
# }

headers = { 
    "Authorization": "Bearer fc-d97ec22c71f64a1eb9d35b320d96b3ff",
    "Content-Type": "application/json"
}

# Väntetid i sekunder mellan requests
DELAY = 15 

with open("output.txt", "w", encoding="utf-8") as f:
    for i, song_url in enumerate(urls, start=1):
        payload = {
            "url": song_url,
            "onlyMainContent": True,
            "maxAge": 172800000,
            "parsers": ["pdf"],
            "formats": ["markdown"]
        }

        try:
            response = requests.post(url, json=payload, headers=headers)

            if response.status_code == 200:
                try:
                    obj = response.json()
                    f.write(json.dumps(obj, ensure_ascii=False) + "\n")
                    print(f"[OK] ({i}/{len(urls)}) Hämtat: {song_url}")
                except Exception as e:
                    print(f"[FEL] JSON-tolkning misslyckades för {song_url}: {e}")
            else:
                print(f"[MISS] ({i}/{len(urls)}) Misslyckades för {song_url}, statuskod: {response.status_code}")

        except requests.exceptions.RequestException as e:
            print(f"[NÄTVERKSFEL] ({i}/{len(urls)}) Kunde inte hämta {song_url}: {e}")

        # Vänta lite innan nästa request
        if i < len(urls):
            time.sleep(DELAY)
