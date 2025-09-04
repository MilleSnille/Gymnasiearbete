import requests

url = "https://api.firecrawl.dev/v2/scrape"

payload = {
  "url": "https://tunebat.com/Info/WAP-feat-Megan-Thee-Stallion-Cardi-B-Megan-Thee-Stallion/4Oun2ylbjFKMPTiaSbbCih",
  "onlyMainContent": True,
  "maxAge": 172800000,
  "parsers": [
    "pdf"
  ],
  "formats": [
    "markdown"
  ]
}

headers = {
    "Authorization": "Bearer fc-666b0b20fdcb43da90e8a0cc21aeb350",
    "Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

with open("output.txt", "w", encoding="utf-8") as f:
    f.write(response.text)