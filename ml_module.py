from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib

# Function to train the machine learning model
def train_model(df):
    X = df[['x', 'y', 'z', 'vx', 'vy', 'vz']]
    y = df['collision']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestClassifier()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    print(classification_report(y_test, y_pred))

    # Save the trained model
    model_path = "satellite_collision_model.joblib"
    joblib.dump(model, model_path)
    print(f"Model saved to {model_path}")

    return model

# Function to load the saved machine learning model
def load_model(model_path):
    model = joblib.load(model_path)
    return model

# Function to predict collisions using the trained model
def predict_collisions(df, model):
    X = df[['x', 'y', 'z', 'vx', 'vy', 'vz']]
    y_pred = model.predict(X)

    collision_pairs = []
    for i in range(len(X)):
        if y_pred[i] == 1:
            for j in range(i+1, len(X)):  # Compare to other satellites
                if y_pred[j] == 1:
                    collision_pairs.append((i, j))

    return collision_pairs