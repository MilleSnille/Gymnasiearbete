import re
import json
import sys
import csv
import os

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

# Mappning från tonart till siffra
key_map = {
    "C major": "1", "B# major": "1", "A minor": "1",
    "G major": "2", "E minor": "2",
    "D major": "3", "B minor": "3",
    "A major": "4", "F# minor": "4", "Gb minor": "4",
    "E major": "5", "C# minor": "5", "Db minor": "5",
    "B major": "6", "G# minor": "6", "Cb major": "6",
    "F# major": "7", "Gb major": "7", "D# minor": "7", "Eb minor": "7",
    "C# major": "8", "Db major": "8", "A# minor": "8", "Bb minor": "8",
    "F major": "9", "D minor": "9",
    "Bb major": "10", "A# major": "10", "G minor": "10",
    "Eb major": "11", "D# major": "11", "C minor": "11",
    "Ab major": "12", "G# major": "12", "F minor": "12"
}

# Hitta Key och BPM i den första låtens block
key_match = re.search(r'###\s*([A-G][#♯♭b]?\s*(?:major|minor|Maj|Min))', song_section)
bpm = re.search(r'###\s*(\d+)\s*[\n ]*BPM', song_section)

# Normalisera och slå upp i key_map
if key_match:
    key_text = key_match.group(1).replace("Maj", "major").replace("Min", "minor")
    key_number = key_map.get(key_text, "Ej hittad")
else:
    key_number = "Ej hittad"

# Hitta övriga värden
popularity = find_value("Popularity", song_section)
energy = find_value("Popularity", song_section)
danceability = find_value("Energy", song_section)
happiness = find_value("Danceability", song_section)
acousticness = find_value("Happiness", song_section)
instrumentalness = find_value("Acousticness", song_section)
liveness = find_value("Instrumentalness", song_section)
speechiness = find_value("Liveness", song_section)

# Samla alla värden i en dictionary
data = {
    "Key": key_number,
    "BPM": bpm.group(1) if bpm else "Ej hittad",
    # "Popularity": popularity,
    "Energy": energy,
    "Danceability": danceability,
    "Happiness": happiness,
    "Acousticness": acousticness,
    "Instrumentalness": instrumentalness,
    "Liveness": liveness,
    "Speechiness": speechiness
}

# Skriv till resultat.csv
csv_file = os.path.join(os.path.dirname(__file__), "resultat.csv")

with open(csv_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=data.keys())
    writer.writeheader()
    writer.writerow(data)

print(f"Resultaten sparades i {csv_file}")
