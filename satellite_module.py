import pandas as pd
from skyfield.sgp4lib import EarthSatellite
from joblib import Parallel, delayed
import numpy as np
from tqdm import tqdm

# Function to load TLE data from CSV file
def load_tle_from_csv(csv_file):
    tle_data = pd.read_csv(csv_file)
    return tle_data['TLE Line 1'].tolist(), tle_data['TLE Line 2'].tolist(), tle_data['Name'].tolist()

# Function to create satellite objects and calculate positions
def create_satellite_objects(tle_line1, tle_line2, ts):
    satellites = []
    for line1, line2 in zip(tle_line1, tle_line2):
        satellite = EarthSatellite(line1.strip(), line2.strip(), 'Satellite', ts)
        satellites.append(satellite)
    return satellites

# Function to calculate average positions and velocities over time
def calculate_positions_and_collisions(satellites, times, satellite_names):
    collision_data = []
    for i, (satellite, name) in enumerate(zip(satellites, satellite_names)):
        geocentric = satellite.at(times)
        x = np.mean(geocentric.position.km[0])
        y = np.mean(geocentric.position.km[1])
        z = np.mean(geocentric.position.km[2])
        vx = np.mean(geocentric.velocity.km_per_s[0])
        vy = np.mean(geocentric.velocity.km_per_s[1])
        vz = np.mean(geocentric.velocity.km_per_s[2])

        collision_data.append({
            'satellite_id': i,
            'name': name,
            'x': x,
            'y': y,
            'z': z,
            'vx': vx,
            'vy': vy,
            'vz': vz
        })

    return pd.DataFrame(collision_data)

# Function to check collisions with parallel processing
def check_collisions(df, collision_distance=1.0):
    def check_collision_for_satellite(index, row, df, collision_distance):
        collision = False
        collision_pairs = set()
        for other_index, other_row in df.iterrows():
            if index != other_index:
                distance = np.sqrt((row['x'] - other_row['x']) ** 2 +
                                   (row['y'] - other_row['y']) ** 2 +
                                   (row['z'] - other_row['z']) ** 2)

                if distance < collision_distance:
                    collision = True
                    collision_pairs.add(tuple(sorted((index, other_index))))
                    break

        return int(collision), collision_pairs

    results = Parallel(n_jobs=-1)(
        delayed(check_collision_for_satellite)(index, row, df, collision_distance) 
        for index, row in tqdm(df.iterrows(), total=len(df), desc="Processing satellites")
    )

    labels = [result[0] for result in results]
    collision_pairs = set()

    for result in results:
        collision_pairs.update(result[1])

    df['collision'] = labels
    return df, list(collision_pairs)
