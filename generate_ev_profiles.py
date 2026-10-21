"""
Standalone script to generate synthetic Electric Vehicle (EV) charging profiles.
This reproduces the EV-augmentation logic used in the paper for the KAN/PPO models.
"""
import numpy as np
import pandas as pd
import random
from datetime import datetime, timedelta

print("Initializing EV Profile Generation...")

# --- 1. Simulation Parameters ---
num_charging_points = 20           # Total number of charging points at the modeled station
start_date = datetime(2020, 1, 1)  # Simulation start date
end_date = datetime(2022, 11, 7)   # Simulation end date
hours_per_day = 24
max_capacity_per_point = 8         # Maximum energy consumption per charging point (kWh/hour)

# --- 2. Stochastic Charging Model ---
def generate_hourly_data(hour, charging_point):
    """
    Generates stochastic charging behavior based on time of day.
    """
    # Define high vs low demand hours (nighttime charging probability is significantly higher)
    if 1 <= hour.hour <= 18:
        probability_of_use = 0.2  # 20% chance of usage during daytime (1 AM to 6 PM)
    else:
        probability_of_use = 0.8  # 80% chance of usage at night (7 PM to Midnight)

    # Determine if this specific charging point is occupied during this hour
    if random.random() < probability_of_use:
        duration = random.randint(1, 2)  # Charging session lasts between 1-2 hours
        energy_consumed = random.uniform(1, max_capacity_per_point)  # Random energy draw up to 8 kWh
        return [charging_point, hour, duration, energy_consumed]
    else:
        # Charging point is unoccupied
        return [charging_point, hour, 0, 0]

# --- 3. Run Simulation ---
print(f"Simulating {num_charging_points} charging points from {start_date.date()} to {end_date.date()}...")
data = []

# Iterate over every charging point for every hour in the date range
for charging_point in range(1, num_charging_points + 1):
    current_time = start_date
    while current_time < end_date:
        for hour in range(hours_per_day):
            current_hour = current_time + timedelta(hours=hour)
            data.append(generate_hourly_data(current_hour, charging_point))
        current_time += timedelta(days=1)

# --- 4. Process and Aggregate Data ---
print("Aggregating load profiles across all charging points...")
columns = ['Charging Point', 'Timestamp', 'Duration (hours)', 'Energy Consumed (kWh)']
ev_charging_df = pd.DataFrame(data, columns=columns)

# Group by the timestamp and sum the energy consumption across all 20 charging points
total_energy_by_hour = ev_charging_df.groupby('Timestamp')['Energy Consumed (kWh)'].sum()

# Map the aggregated total energy back to the original DataFrame
ev_charging_df['Total Energy Consumption (kWh)'] = ev_charging_df['Timestamp'].map(total_energy_by_hour)

# Calculate ratio against max peak consumption
max_energy = ev_charging_df['Total Energy Consumption (kWh)'].max()
ev_charging_df['ratio'] = ev_charging_df['Total Energy Consumption (kWh)'] / max_energy

# --- 5. Export ---
output_file = 'standalone_ev_profiles.csv'
ev_charging_df.to_csv(output_file, index=False)
print(f"Success! Generated EV profile dataset saved to: {output_file}")
print("In the main pipeline, this aggregated 'Total Energy Consumption' is added directly to the historical base grid load (Forbrug).")
