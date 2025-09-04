import re
import json
import sys

# Säkerställ UTF-8 utskrift i konsolen
sys.stdout.reconfigure(encoding="utf-8")

# Läs JSON från output.txt
with open("output.txt", "r", encoding="utf-8") as f:
    obj = json.load(f)

# Hämta markdown-strängen
markdown = obj["data"]["markdown"]

# Begränsa till den första låtens sektion (innan rekommendationerna)
song_section = markdown.split("## Recommendations")[0]

def find_value(label, section):
    lines = section.split('\n')
    for i, line in enumerate(lines):
        if line.strip().lower() == label.lower():
            # Leta upp nästa rad som inte är tom
            for j in range(i + 1, len(lines)):
                value = lines[j].strip()
                if value:
                    match = re.search(r'[\d\.]+', value)
                    return match.group(0) if match else value
            break
    return "Ej hittad"

# Hitta Key och BPM i den första låtens block
key = re.search(r'###\s*([A-G][#♯♭b]?\s*(?:major|minor|Maj|Min))', song_section)
bpm = re.search(r'###\s*(\d+)\s*[\n ]*BPM', song_section)

# Hitta övriga värden
popularity = find_value("Popularity", song_section)
energy = find_value("Energy", song_section)
danceability = find_value("Danceability", song_section)
happiness = find_value("Happiness", song_section)
acousticness = find_value("Acousticness", song_section)
instrumentalness = find_value("Instrumentalness", song_section)
liveness = find_value("Liveness", song_section)
speechiness = find_value("Speechiness", song_section)

# Skriv ut resultaten
print("Key:", key.group(1) if key else "Ej hittad")
print("BPM:", bpm.group(1) if bpm else "Ej hittad")
# print("Popularity:", popularity)
print("Energy:", popularity)
print("Danceability:", energy)
print("Happiness:", danceability)
print("Acousticness:", happiness)
print("Instrumentalness:", acousticness)
print("Liveness:", instrumentalness)
print("Speechiness:", liveness)
