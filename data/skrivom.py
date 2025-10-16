import re
import json
import sys
import csv

# Säkerställ UTF-8 utskrift i konsolen
sys.stdout.reconfigure(encoding="utf-8")

def find_value(label, section):
    lines = section.split('\n')
    for i, line in enumerate(lines):
        if line.strip().lower() == label.lower():
            for j in range(i + 1, len(lines)):
                value = lines[j].strip()
                if value:
                    match = re.search(r'[\d\.]+', value)
                    return match.group(0) if match else value
            break
    return "Ej hittad"

key_map = {
    "C major": 1, "A minor": 1,
    "C# major": 2, "Db major": 2, "A# minor": 2, "Bb minor": 2,
    "D major": 3, "B minor": 3,
    "D# major": 4, "Eb major": 4, "C minor": 4,
    "E major": 5, "C# minor": 5, "Db minor": 5,
    "F major": 6, "D minor": 6,
    "F# major": 7, "Gb major": 7, "D# minor": 7, "Eb minor": 7,
    "G major": 8, "E minor": 8,
    "G# major": 9, "Ab major": 9, "F minor": 9,
    "A major": 10, "F# minor": 10, "Gb minor": 10,
    "A# major": 11, "Bb major": 11, "G minor": 11,
    "B major": 12, "G# minor": 12, "Ab minor": 12
}

results = []

with open("output.txt", "r", encoding="utf-8") as f:
    for line in f:
        if not line.strip():
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            print("⚠️ Hoppar över trasig rad i output.txt")
            continue

        markdown = obj["data"]["markdown"]
        song_section = markdown.split("## Recommendations")[0]

        key_match = re.search(r'###\s*([A-G][#♯♭b]?\s*(?:major|minor|Maj|Min))', song_section, re.IGNORECASE)
        bpm = re.search(r'###\s*(\d+)\s*[\n ]*BPM', song_section)

        if key_match:
            key_text = key_match.group(1).capitalize()
            key_text = key_text.replace("♯", "#").replace("♭", "b")
        else:
            key_text = "Ej hittad"

        key_number = key_map.get(key_text, "Ej hittad")

        data = {
            "Key": key_number,
            "BPM": bpm.group(1) if bpm else "Ej hittad",
            # "Popularity": find_value("Popularity", song_section),
            "Energy": find_value("Popularity", song_section),
            "Danceability": find_value("Energy", song_section),
            "Happiness": find_value("Danceability", song_section),
            "Acousticness": find_value("Happiness", song_section),
            "Instrumentalness": find_value("Acousticness", song_section),
            "Liveness": find_value("Instrumentalness", song_section),
            "Speechiness": find_value("Liveness", song_section)
        }

        results.append(data)

# Skriv allt till CSV
with open("resultat.csv", "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=results[0].keys())
    writer.writeheader()
    writer.writerows(results)

print("✅ Alla resultat har sparats i resultat.csv")
