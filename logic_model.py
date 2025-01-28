import pandas as pd

# Load dataset
data = pd.read_csv("summary.csv", parse_dates=["date"], dayfirst=True)

# Define future holiday dictionary
future_holidays = {
    1: "2024-01-01",
    2: "2024-04-14",
    # Add more holidays here
}

def is_holiday(selected_date):
    """Check if the selected date is a holiday."""
    return pd.to_datetime(selected_date) in pd.to_datetime(list(future_holidays.values()))

def holiday_logic(selected_date):
    """Process logic for holidays."""
    holiday_key = list(future_holidays.keys())[list(future_holidays.values()).index(selected_date)]
    holiday_rows = data[data["day_type"] == "Holiday"].copy()
    holiday_rows["key"] = holiday_rows.groupby(holiday_rows["date"].dt.year).cumcount() + 1
    return holiday_rows[holiday_rows["key"] == holiday_key]

def weekday_logic(selected_date):
    """Process logic for weekdays."""
    selected_date = pd.to_datetime(selected_date)
    day_type = selected_date.strftime("%A")
    month = selected_date.month

    # Get rows for the same month and day type
    rows = data[(data["date"].dt.month == month) & (data["day_type"] == day_type)].copy()

    # Determine position of the selected day in the month
    selected_day_position = (selected_date.day - 1) // 7 + 1
    rows["position"] = (rows["date"].dt.day - 1) // 7 + 1

    # Filter by position, adjust if missing
    while rows[rows["position"] == selected_day_position].empty and selected_day_position > 0:
        selected_day_position -= 1

    return rows[rows["position"] == selected_day_position]

def combine_logic(selected_date):
    """Combine logic for holidays and weekdays."""
    if is_holiday(selected_date):
        return holiday_logic(selected_date)
    else:
        return weekday_logic(selected_date)
