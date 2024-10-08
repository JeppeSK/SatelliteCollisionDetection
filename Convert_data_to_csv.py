import requests
import csv
from sgp4.api import Satrec
from skyfield.api import EarthSatellite, load

# Load time scale
ts = load.timescale()

# Fetch data from Celestrak
url = "https://celestrak.com/NORAD/elements/gp.php?GROUP=active&FORMAT=tle"
response = requests.get(url)
tle_data = response.text.strip().splitlines()

# Split TLE data into chunks of 3 lines (name, line1, line2)
tle_chunks = [tle_data[i:i + 3] for i in range(0, len(tle_data), 3)]

# Prepare the CSV file
csv_file = "satellites.csv"

with open(csv_file, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Name", "TLE Line 1", "TLE Line 2"])  # Headers

    # Iterate over TLE data
    for chunk in tle_chunks:
        name, line1, line2 = chunk
        writer.writerow([name.strip(), line1.strip(), line2.strip()])

print(f"Data saved to {csv_file}")