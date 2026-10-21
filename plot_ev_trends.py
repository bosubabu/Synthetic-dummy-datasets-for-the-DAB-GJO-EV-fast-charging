import pandas as pd
import matplotlib.pyplot as plt
import os

print("Loading standalone EV profile dataset...")
try:
    df = pd.read_csv('standalone_ev_profiles.csv')
except FileNotFoundError:
    print("Error: 'standalone_ev_profiles.csv' not found. Please run 'generate_ev_profiles.py' first.")
    exit(1)

df['Timestamp'] = pd.to_datetime(df['Timestamp'])

print("Pivoting data for individual EV charging points...")
# Pivot table to have Timestamp as index and Charging Points as columns
pivot_df = df.pivot(index='Timestamp', columns='Charging Point', values='Energy Consumed (kWh)').fillna(0)

# Pick 3 different 1-week intervals to show trends across different times of the year
weeks = [
    ('2020-02-10', '2020-02-17', 'Winter Week (Feb 10 - Feb 17, 2020)'),
    ('2020-07-13', '2020-07-20', 'Summer Week (Jul 13 - Jul 20, 2020)'),
    ('2021-04-12', '2021-04-19', 'Spring Week (Apr 12 - Apr 19, 2021)')
]

print("Generating stacked area plots...")
fig, axes = plt.subplots(3, 1, figsize=(15, 12), sharey=True)

for ax, (start, end, title) in zip(axes, weeks):
    week_data = pivot_df[(pivot_df.index >= start) & (pivot_df.index < end)]
    
    # Plot as a stacked area chart to show individual EVs (charging points) and total trend
    week_data.plot.area(ax=ax, colormap='tab20', alpha=0.8, linewidth=0)
    
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.set_ylabel('Energy Consumed (kWh)', fontsize=12)
    ax.set_xlabel('Timestamp', fontsize=12)
    
    # Position the legend outside the plot area
    ax.legend(title='Charging Point', bbox_to_anchor=(1.01, 1), loc='upper left', ncol=2)
    ax.grid(True, linestyle='--', alpha=0.5)

plt.tight_layout()

# Save the plot
out_path = 'ev_weekly_trends.png'
plt.savefig(out_path, dpi=300)
print(f"Plot successfully saved to {out_path}")
