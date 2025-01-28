import pandas as pd
from datetime import datetime

# Load the dataset
data = pd.read_csv('dataset.csv')

# Step 1: Preprocessing - Convert date and time columns to datetime
data['date'] = pd.to_datetime(data['date'], format='%Y/%m/%d')
data['call_incoming_time'] = pd.to_datetime(data['date'].astype(str) + ' ' + data['call_incoming_time'], format='%Y-%m-%d %H:%M')
data['call_answered_time'] = pd.to_datetime(data['date'].astype(str) + ' ' + data['call_answered_time'], format='%Y-%m-%d %H:%M', errors='coerce')
data['call_ended_time'] = pd.to_datetime(data['date'].astype(str) + ' ' + data['call_ended_time'], format='%Y-%m-%d %H:%M', errors='coerce')

# Save the preprocessed dataset to CSV
data.to_csv('preprocessed_dataset.csv', index=False)
print("Step 1: Preprocessed data saved to 'preprocessed_dataset.csv'.")

# Define shifts and agent categories
shifts = {
    'S1': (datetime.strptime('00:00', '%H:%M').time(), datetime.strptime('08:00', '%H:%M').time()),
    'S2': (datetime.strptime('08:00', '%H:%M').time(), datetime.strptime('16:00', '%H:%M').time()),
    'S3': (datetime.strptime('16:00', '%H:%M').time(), datetime.strptime('23:59', '%H:%M').time())
}

agent_categories = {
    'C1': {'languages': ['English', 'Sinhala']},
    'C2': {'languages': ['English', 'Tamil']},
    'C3': {'languages': ['Sinhala', 'Tamil']}
}

missed_call_threshold = 5  # Define a threshold for adding extra agents based on missed calls

# Function to allocate agents and track missed calls by language
def allocate_agents_for_shift(shift_data, agent_status):
    agents_needed = {'C1': 0, 'C2': 0, 'C3': 0}
    missed_calls_count = 0
    missed_calls_by_language = {}

    for _, call in shift_data.iterrows():
        language = call['call_language']
        call_start = call['call_incoming_time']
        call_end = call['call_ended_time']
        
        # Count missed calls and skip unanswered calls for allocation
        if pd.isnull(call['call_answered_time']):
            missed_calls_count += 1
            missed_calls_by_language[language] = missed_calls_by_language.get(language, 0) + 1
            continue

        assigned_agent = None
        for category, status in agent_status.items():
            if language in agent_categories[category]['languages']:
                for agent in status:
                    if agent['available'] <= call_start:
                        assigned_agent = agent
                        agent['available'] = call_end
                        break
                if assigned_agent:
                    break

        if not assigned_agent:
            for category, languages in agent_categories.items():
                if language in languages['languages']:
                    agents_needed[category] += 1
                    agent_status[category].append({'available': call_end})
                    break

    return agents_needed, missed_calls_count, missed_calls_by_language

# Generate summary for each day
summary_data = []
daily_agent_requirements = []
missed_calls_summary = []

for day in data['date'].dt.date.unique():
    day_data = data[data['date'].dt.date == day]
    day_summary = {'date': day.strftime('%d/%m/%Y')}
    day_summary['day_type'] = day_data['day_type'].iloc[0] if 'day_type' in day_data else 'Weekday'
    day_summary['total_calls_for_date'] = len(day_data)
    day_missed_calls = 0
    missed_calls_by_language_for_day = {}

    for shift, (start, end) in shifts.items():
        shift_data = day_data[(day_data['call_incoming_time'].dt.time >= start) & 
                              (day_data['call_incoming_time'].dt.time <= end)]
        
        agent_status = {category: [] for category in agent_categories}
        agents_needed, missed_calls, missed_calls_by_language = allocate_agents_for_shift(shift_data, agent_status)

        day_missed_calls += missed_calls
        for lang, count in missed_calls_by_language.items():
            missed_calls_by_language_for_day[lang] = missed_calls_by_language_for_day.get(lang, 0) + count

        # Count calls by language in each shift
        day_summary[f"{shift}_english_calls"] = len(shift_data[shift_data['call_language'] == 'English'])
        day_summary[f"{shift}_sinhala_calls"] = len(shift_data[shift_data['call_language'] == 'Sinhala'])
        day_summary[f"{shift}_tamil_calls"] = len(shift_data[shift_data['call_language'] == 'Tamil'])

        # Agents needed in each shift per category
        agent_requirements = {}
        for category in agents_needed:
            day_summary[f"{shift}_agents_needed_{category}"] = agents_needed[category]
            agent_requirements[f"{shift}_agents_needed_{category}"] = agents_needed[category]
        
        # Append agent requirements for the day
        daily_agent_requirements.append(agent_requirements)

    day_summary['missed_call_for_day'] = day_missed_calls
    missed_calls_summary.append({'date': day_summary['date'], 'missed_calls_by_language': missed_calls_by_language_for_day})
    summary_data.append(day_summary)

# Convert final daily results to DataFrame for analysis or reporting
summary_df = pd.DataFrame(summary_data)
summary_df.to_csv("summary.csv", index=False)
print("Summary data saved to 'summary.csv'.")

# Convert and save additional files

# Daily agent requirements saved as CSV
agent_requirements_df = pd.json_normalize(daily_agent_requirements, sep='_')
agent_requirements_df.to_csv("daily_agent_requirements.csv", index=False)
print("Daily agent requirements saved to 'daily_agent_requirements.csv'.")

# Save missed calls summary to CSV
missed_calls_df = pd.DataFrame(missed_calls_summary)
missed_calls_df.to_csv("missed_calls_summary.csv", index=False)
print("Missed calls summary saved to 'missed_calls_summary.csv'.")

# Save detailed missed calls by language for further analysis
missed_calls_by_language_df = pd.DataFrame(missed_calls_summary).explode('missed_calls_by_language')
missed_calls_by_language_df.to_csv("missed_calls_by_language_summary.csv", index=False)
print("Missed calls by language summary saved to 'missed_calls_by_language_summary.csv'.")

# Save all preprocessed data along with agent requirements and missed calls to "alldata.csv"
alldata_df = pd.concat([data, agent_requirements_df, missed_calls_df], axis=1)
alldata_df.to_csv("alldata.csv", index=False)
print("All data saved to 'alldata.csv'.")
