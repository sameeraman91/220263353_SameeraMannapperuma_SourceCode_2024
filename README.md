

# Call Center Optimization System

This project leverages **Machine Learning** and **Logic-Based Systems** to enhance call center efficiency by predicting call volumes and dynamically allocating agents.

## 🚀 How to Run the Project
1. Ensure you have Python 3.7 or later installed.
2. Install the required modules:
   ```bash
   pip install flask pandas scikit-learn
   ```
3. Open a terminal in the project directory.
4. Run the application:
   ```bash
   python app.py
   ```
5. Open your web browser and go to: [http://127.0.0.1:5000](http://127.0.0.1:5000).

## 📂 Project Structure
- `app.py`: The main application script for the Flask web app.
- `ml_model.py`: Contains functions for machine learning model training and prediction.
- `logic_model.py`: Handles logic-based adjustments and combines ML outputs.
- `summery.csv`: Dataset containing historical call data.

## 📋 Features
- **Login System**: Secure user authentication.
- **Interactive Dashboard**: Visualize call predictions and agent requirements.
- **Dynamic Resource Allocation**: Combines ML predictions with logic adjustments.
- **Machine Learning**: Utilizes Random Forest Regression for predictions.

## 🛠️ Required Modules
Install the following Python modules:
```bash
pip install flask pandas scikit-learn
```

## 🎯 Purpose
Optimize call center operations by:
- Predicting total call volumes, missed calls, and agent requirements.
- Improving resource utilization and customer satisfaction.
- Providing insights for better scheduling and decision-making.

## ✨ Future Improvements
- Expand datasets for better holiday predictions.
- Integrate real-time data streams for live updates.
- Add support for additional languages and call categories.
