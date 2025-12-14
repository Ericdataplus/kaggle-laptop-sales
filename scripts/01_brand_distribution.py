"""
01 - Brand Distribution Analysis
Visualizes the market share of laptop brands on Amazon
"""
import pandas as pd
import matplotlib.pyplot as plt
import os

# Setup paths
script_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(script_dir)
data_path = os.path.join(project_dir, 'laptops.csv')
output_path = os.path.join(project_dir, 'graphs', '01_brand_distribution.png')

# Load data
df = pd.read_csv(data_path)

# Clean brand names (standardize case)
df['brand_clean'] = df['brand'].str.upper().str.strip()

# Get top 10 brands by count
brand_counts = df['brand_clean'].value_counts().head(10)

# Create figure
fig, ax = plt.subplots(figsize=(12, 8))
fig.patch.set_facecolor('#1a1a2e')
ax.set_facecolor('#1a1a2e')

# Color palette
colors = ['#00d4ff', '#00b4d8', '#0096c7', '#0077b6', '#023e8a', 
          '#03045e', '#240046', '#3c096c', '#5a189a', '#7b2cbf']

# Create horizontal bar chart
bars = ax.barh(range(len(brand_counts)), brand_counts.values, color=colors)

# Add value labels
for i, (bar, val) in enumerate(zip(bars, brand_counts.values)):
    ax.text(val + 20, bar.get_y() + bar.get_height()/2, f'{val:,}', 
            va='center', ha='left', color='white', fontsize=12, fontweight='bold')

# Customize
ax.set_yticks(range(len(brand_counts)))
ax.set_yticklabels(brand_counts.index, color='white', fontsize=12)
ax.invert_yaxis()
ax.set_xlabel('Number of Listings', color='white', fontsize=14)
ax.set_title('🏢 Top 10 Laptop Brands on Amazon', color='white', fontsize=20, fontweight='bold', pad=20)

# Style axes
ax.tick_params(colors='white')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_color('#444')
ax.spines['left'].set_color('#444')

# Add total count annotation
total = len(df)
ax.text(0.98, 0.02, f'Total: {total:,} laptops', transform=ax.transAxes,
        ha='right', va='bottom', color='#888', fontsize=11)

plt.tight_layout()
plt.savefig(output_path, dpi=150, facecolor='#1a1a2e', edgecolor='none', bbox_inches='tight')
plt.close()

print(f"✅ Saved: {output_path}")
print(f"   Top brand: {brand_counts.index[0]} ({brand_counts.values[0]:,} listings)")
