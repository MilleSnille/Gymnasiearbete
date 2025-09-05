# fil: citattecken.py

# Ange filnamn
in_fil = "input.txt"
ut_fil = "output.txt"

with open(in_fil, "r", encoding="utf-8") as f:
    rader = f.readlines()

# Lägg till citattecken runt varje rad + komma på slutet
ny_rader = [f"\"{rad.strip()}\",\n" for rad in rader]

with open(ut_fil, "w", encoding="utf-8") as f:
    f.writelines(ny_rader)

print(f"Klart! Resultatet sparades i {ut_fil}")
