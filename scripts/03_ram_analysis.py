"""
03 - RAM Analysis
Visualizes RAM distribution and RAM vs Price relationship
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# Setup paths
script_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(script_dir)
data_path = os.path.join(project_dir, 'laptops.csv')
output_path = os.path.join(project_dir, 'graphs', '03_ram_analysis.png')

# Load data
df = pd.read_csv(data_path)

# Clean RAM column - extract numeric value
df['ram_gb'] = df['ram'].str.extract(r'(\d+)').astype(float)

# Clean price column
df['price_clean'] = df['Price'].str.replace('$', '', regex=False).str.replace(',', '', regex=False).str.strip()
df['price_clean'] = pd.to_numeric(df['price_clean'], errors='coerce')

# Filter valid data
df_ram = df[(df['ram_gb'].notna()) & (df['price_clean'] >= 50) & (df['price_clean'] <= 10000)].copy()

# Create figure with 2 subplots
fig, axes = plt.subplots(1, 2, figsize=(16, 8))
fig.patch.set_facecolor('#1a1a2e')

# ----- Plot 1: RAM Distribution -----
ax1 = axes[0]
ax1.set_facecolor('#1a1a2e')

ram_counts = df_ram['ram_gb'].value_counts().sort_index()
# Filter to common RAM sizes
common_ram = [4, 8, 12, 16, 20, 32, 64]
ram_counts = ram_counts[ram_counts.index.isin(common_ram)]

colors = plt.cm.viridis(np.linspace(0.2, 0.8, len(ram_counts)))
bars = ax1.bar(ram_counts.index.astype(int).astype(str) + ' GB', ram_counts.values, color=colors)

# Add value labels
for bar, val in zip(bars, ram_counts.values):
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 20, f'{val:,}',
             ha='center', va='bottom', color='white', fontsize=11, fontweight='bold')

ax1.set_xlabel('RAM Size', color='white', fontsize=12)
ax1.set_ylabel('Number of Laptops', color='white', fontsize=12)
ax1.set_title('🧠 RAM Distribution', color='white', fontsize=16, fontweight='bold')
ax1.tick_params(colors='white')
for spine in ax1.spines.values():
    spine.set_color('#444')

# ----- Plot 2: RAM vs Price -----
ax2 = axes[1]
ax2.set_facecolor('#1a1a2e')

# Calculate mean price by RAM
ram_price = df_ram.groupby('ram_gb')['price_clean'].agg(['mean', 'median', 'count'])
ram_price = ram_price[ram_price.index.isin(common_ram)]

# Bar chart for mean price
colors2 = plt.cm.plasma(np.linspace(0.2, 0.8, len(ram_price)))
bars2 = ax2.bar(ram_price.index.astype(int).astype(str) + ' GB', ram_price['mean'], 
                color=colors2, alpha=0.8, label='Mean Price')

# Add mean price labels
for bar, val in zip(bars2, ram_price['mean']):
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 30, f'${val:,.0f}',
             ha='center', va='bottom', color='white', fontsize=10, fontweight='bold')

ax2.set_xlabel('RAM Size', color='white', fontsize=12)
ax2.set_ylabel('Average Price ($)', color='white', fontsize=12)
ax2.set_title('💾 Average Price by RAM', color='white', fontsize=16, fontweight='bold')
ax2.tick_params(colors='white')
for spine in ax2.spines.values():
    spine.set_color('#444')

plt.tight_layout()
plt.savefig(output_path, dpi=150, facecolor='#1a1a2e', edgecolor='none', bbox_inches='tight')
plt.close()

print(f"✅ Saved: {output_path}")
print(f"   Most common RAM: {ram_counts.idxmax():.0f} GB ({ram_counts.max():,} laptops)")
