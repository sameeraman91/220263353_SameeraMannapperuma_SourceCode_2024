from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import pandas as pd

# Load dataset
data = pd.read_csv("summary.csv", parse_dates=["date"], dayfirst=True)

def prepare_training_data(day_type, dataset):
    """Prepare training data based on the day type."""
    filtered_data = dataset[dataset["day_type"] == day_type]
    X = filtered_data[
        [
            "total_calls_for_date",
            "S1_english_calls", "S1_sinhala_calls", "S1_tamil_calls",
            "S2_english_calls", "S2_sinhala_calls", "S2_tamil_calls",
            "S3_english_calls", "S3_sinhala_calls", "S3_tamil_calls",
        ]
    ]
    y = filtered_data[
        [
            "S1_agents_needed_C1", "S1_agents_needed_C2", "S1_agents_needed_C3",
            "S2_agents_needed_C1", "S2_agents_needed_C2", "S2_agents_needed_C3",
            "S3_agents_needed_C1", "S3_agents_needed_C2", "S3_agents_needed_C3",
        ]
    ]
    return X, y

def train_model(day_type, dataset):
    """Train a RandomForest model for agent predictions."""
    X, y = prepare_training_data(day_type, dataset)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestRegressor(random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    print("MSE:", mean_squared_error(y_test, y_pred))
    return model

def predict_agents(selected_rows, model):
    """Predict agent allocation using the trained model."""
    X_predict = selected_rows[
        [
            "total_calls_for_date",
            "S1_english_calls", "S1_sinhala_calls", "S1_tamil_calls",
            "S2_english_calls", "S2_sinhala_calls", "S2_tamil_calls",
            "S3_english_calls", "S3_sinhala_calls", "S3_tamil_calls",
        ]
    ]
    return model.predict(X_predict)
