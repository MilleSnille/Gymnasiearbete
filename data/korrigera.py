import csv

# Namn på originalfilen och nya filen
input_file = 'melodifestivalen.csv'
output_file = 'mello.csv'

# Öppna originalfilen för läsning
with open(input_file, mode='r', newline='', encoding='utf-8') as infile:
    reader = csv.DictReader(infile)
    
    # Skapa en lista på kolumner utan 'Speechiness'
    fieldnames = [field for field in reader.fieldnames if field != 'Speechiness']
    
    # Öppna ny fil för skrivning
    with open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        
        # Skriv varje rad utan 'Speechiness'
        for row in reader:
            row.pop('Speechiness', None)
            writer.writerow(row)

print(f"Ny CSV-fil skapad utan 'Speechiness': {output_file}")
