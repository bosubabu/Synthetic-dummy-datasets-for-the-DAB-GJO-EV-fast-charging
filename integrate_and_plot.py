"""
This script demonstrates the critical data mixing step used in the main KAN/PPO pipeline.
To protect the confidentiality of the real-world historical grid consumption data, 
this script uses a mock diurnal base load (a generic sine wave) to demonstrate 
how the synthetic EV load is perfectly aligned by hourly timestamp and added to create the 'LoadEVs' target.
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

print("1. Generating Mock Base Load (for demonstration purposes)...")
# Since real load values are confidential, we generate a synthetic diurnal base load
# spanning the same date range to demonstrate the mixing mechanics.
date_rng = pd.date_range(start='2020-01-01', end='2022-11-07', freq='h')
# Create a generic daily pattern (peaking in the evening)
hours = date_rng.hour
mock_forbrug = 40 + 20 * np.sin((hours - 12) * (2 * np.pi / 24))
df_base = pd.DataFrame({'Timestamp': date_rng, 'Forbrug': mock_forbrug})
df_base.set_index('Timestamp', inplace=True)

print("2. Loading Synthetic EV Profiles...")
# Load the generated synthetic EV profiles
try:
    df_ev = pd.read_csv('standalone_ev_profiles.csv')
except FileNotFoundError:
    print("Error: 'standalone_ev_profiles.csv' not found. Please run 'generate_ev_profiles.py' first.")
    exit(1)

df_ev['Timestamp'] = pd.to_datetime(df_ev['Timestamp'])
# Aggregate EV energy across all charging points for each hour
df_ev_agg = df_ev.groupby('Timestamp')['Energy Consumed (kWh)'].sum().to_frame()
df_ev_agg.columns = ['EV_Load']

print("3. Mixing Data (Aligning by Timestamp)...")
# Inner join ensures perfect time-step alignment between base load and EV load
df_merged = df_base.join(df_ev_agg, how='inner')

# The core integration math from KANPPO.py: LoadEVs = Forbrug + EVs.Values
df_merged['LoadEVs'] = df_merged['Forbrug'] + df_merged['EV_Load']

print("4. Plotting the Integration (Winter Week: Feb 2020)...")
# Pick a representative 1-week interval to clearly show the diurnal overlap
start_date = '2020-02-10'
end_date = '2020-02-17'
week_data = df_merged[(df_merged.index >= start_date) & (df_merged.index < end_date)]

fig, axes = plt.subplots(3, 1, figsize=(15, 12), sharex=True)

# Plot 1: Mock Base Load
axes[0].plot(week_data.index, week_data['Forbrug'], linewidth=2.5, color='#d95f02', label='Mock Base Load (Forbrug)')
axes[0].set_title('Step 1: Mock Diurnal Base Load (Real data removed for confidentiality)', fontsize=14, fontweight='bold')
axes[0].set_ylabel('Consumption (kWh)')
axes[0].grid(True, linestyle='--', alpha=0.5)
axes[0].legend(loc='upper right')

# Plot 2: Total Synthetic EV Load
axes[1].plot(week_data.index, week_data['EV_Load'], linewidth=2.5, color='#4C72B0', label='Total Synthetic EV Load')
axes[1].set_title('Step 2: Synthetically Generated EV Load', fontsize=14, fontweight='bold')
axes[1].set_ylabel('Energy Consumed (kWh)')
axes[1].grid(True, linestyle='--', alpha=0.5)
axes[1].legend(loc='upper right')

# Plot 3: The Mixed Result (LoadEVs)
axes[2].plot(week_data.index, week_data['LoadEVs'], linewidth=2.5, color='#e41a1c', label='Augmented Target Load (LoadEVs)')
axes[2].set_title('Step 3: The Final Augmented Load (LoadEVs = Base + EV)', fontsize=14, fontweight='bold')
axes[2].set_ylabel('Total Consumption (kWh)')
axes[2].set_xlabel('Timestamp')
axes[2].grid(True, linestyle='--', alpha=0.5)
axes[2].legend(loc='upper right')

plt.tight_layout()
out_path = 'mixed_integration_trends.png'
plt.savefig(out_path, dpi=300)
print(f"Plot successfully saved to {out_path}")
