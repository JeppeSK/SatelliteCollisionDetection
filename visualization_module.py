import plotly.graph_objects as go
import numpy as np

def visualize_with_plotly(df, collision_pairs):
    fig = go.Figure()

    # Plot Earth as a sphere
    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 100)
    x = 6371 * np.outer(np.cos(u), np.sin(v))
    y = 6371 * np.outer(np.sin(u), np.sin(v))
    z = 6371 * np.outer(np.ones_like(u), np.cos(v))

    fig.add_trace(go.Surface(x=x, y=y, z=z, colorscale='Blues', opacity=0.3, name='Earth'))

    # Filter the DataFrame to only include satellites involved in predicted collisions
    collision_indices = set()
    for sat1, sat2 in collision_pairs:
        collision_indices.update([sat1, sat2])
    collision_df = df.loc[df.index.isin(collision_indices)]

    # Plot the satellites that are involved in collisions
    if 'x' in collision_df.columns and 'y' in collision_df.columns and 'z' in collision_df.columns:
        fig.add_trace(go.Scatter3d(
            x=collision_df['x'],
            y=collision_df['y'],
            z=collision_df['z'],
            mode='markers',
            marker=dict(size=4, color='green', opacity=0.8),
            name='Satellites'
        ))

        # Display the satellite positions in the terminal for reference
        for index, row in collision_df.iterrows():
            print(f"Collision satellite position: x={row['x']}, y={row['y']}, z={row['z']}")
    else:
        print("No satellite position data found in the DataFrame.")

    # Plot collision paths using satellite names
    for sat1, sat2 in collision_pairs:
        if sat1 in collision_df.index and sat2 in collision_df.index:
            sat1_name = collision_df.loc[sat1, 'name']
            sat2_name = collision_df.loc[sat2, 'name']
            fig.add_trace(go.Scatter3d(
                x=[collision_df.loc[sat1, 'x'], collision_df.loc[sat2, 'x']],
                y=[collision_df.loc[sat1, 'y'], collision_df.loc[sat2, 'y']],
                z=[collision_df.loc[sat1, 'z'], collision_df.loc[sat2, 'z']],
                mode='lines',
                line=dict(color='red', width=3),
                name=f'Collision Path {sat1_name} - {sat2_name}'
            ))

    fig.update_layout(
        scene=dict(
            xaxis_title='X (km)',
            yaxis_title='Y (km)',
            zaxis_title='Z (km)',
            aspectmode='data'
        ),
        title='Satellites and Predicted Collisions',
        width=1980,
        height=1080
    )

    fig.show()
