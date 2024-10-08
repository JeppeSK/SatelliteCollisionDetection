from skyfield.api import load
from ml_module import train_model, load_model, predict_collisions
from satellite_module import load_tle_from_csv, create_satellite_objects, calculate_positions_and_collisions, check_collisions
from visualization_module import visualize_with_plotly

# Main function
def main():
    csv_file = "satellites.csv"  # Path to your CSV file
    tle_line1, tle_line2, satellite_names = load_tle_from_csv(csv_file)

    ts = load.timescale()
    times = ts.utc(2024, 1, 1, 0, range(0, 120, 1))

    # Create satellite objects and calculate positions
    satellites = create_satellite_objects(tle_line1, tle_line2, ts)
    df = calculate_positions_and_collisions(satellites, times, satellite_names)
    df, collision_pairs = check_collisions(df)

    print("\nPredicted satellite collisions:")
    for pair in collision_pairs:
        print(f"Satellite {satellite_names[pair[0]]} will possibly collide with Satellite {satellite_names[pair[1]]}")

    # Load or train the machine learning model
    model_path = "satellite_collision_model.joblib"
    try:
        model = load_model(model_path)
        print("Model loaded from file.")
    except FileNotFoundError:
        print("Training model from scratch...")
        model = train_model(df)
    
    # Predict collisions using the trained model
    collision_pairs = predict_collisions(df, model)

    print("Collision Pairs:", collision_pairs)

    # Call the Mayavi visualization function
    visualize_with_plotly(df, collision_pairs)

if __name__ == "__main__":
    main()