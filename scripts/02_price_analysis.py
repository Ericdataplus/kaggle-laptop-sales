"""
02 - Price Analysis
Visualizes laptop price distribution and price by brand
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# Setup paths
script_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(script_dir)
data_path = os.path.join(project_dir, 'laptops.csv')
output_path = os.path.join(project_dir, 'graphs', '02_price_analysis.png')

# Load data
df = pd.read_csv(data_path)

# Clean price column - remove $ and commas, convert to float
df['price_clean'] = df['Price'].str.replace('$', '', regex=False).str.replace(',', '', regex=False).str.strip()
df['price_clean'] = pd.to_numeric(df['price_clean'], errors='coerce')

# Remove outliers (prices > $10,000 or < $50)
df_price = df[(df['price_clean'] >= 50) & (df['price_clean'] <= 10000)].copy()

# Create figure with 2 subplots
fig, axes = plt.subplots(1, 2, figsize=(16, 8))
fig.patch.set_facecolor('#1a1a2e')

# Color palette
hist_color = '#00d4ff'
box_colors = ['#00d4ff', '#00b4d8', '#0096c7', '#0077b6', '#023e8a', '#7b2cbf']

# ----- Plot 1: Price Distribution Histogram -----
ax1 = axes[0]
ax1.set_facecolor('#1a1a2e')

# Create histogram
n, bins, patches = ax1.hist(df_price['price_clean'], bins=50, color=hist_color, 
                            edgecolor='#1a1a2e', alpha=0.8)

# Add gradient effect to bars
for i, patch in enumerate(patches):
    patch.set_facecolor(plt.cm.cool(i / len(patches)))

ax1.axvline(df_price['price_clean'].median(), color='#ff6b6b', linestyle='--', 
            linewidth=2, label=f"Median: ${df_price['price_clean'].median():,.0f}")
ax1.axvline(df_price['price_clean'].mean(), color='#ffd93d', linestyle='--', 
            linewidth=2, label=f"Mean: ${df_price['price_clean'].mean():,.0f}")

ax1.set_xlabel('Price ($)', color='white', fontsize=12)
ax1.set_ylabel('Number of Laptops', color='white', fontsize=12)
ax1.set_title('💰 Price Distribution', color='white', fontsize=16, fontweight='bold')
ax1.legend(loc='upper right', facecolor='#2a2a4e', labelcolor='white')
ax1.tick_params(colors='white')
for spine in ax1.spines.values():
    spine.set_color('#444')

# ----- Plot 2: Price by Top Brands -----
ax2 = axes[1]
ax2.set_facecolor('#1a1a2e')

# Get top 6 brands
df_price['brand_clean'] = df_price['brand'].str.upper().str.strip()
top_brands = df_price['brand_clean'].value_counts().head(6).index.tolist()
df_top = df_price[df_price['brand_clean'].isin(top_brands)]

# Calculate median price by brand and sort
brand_medians = df_top.groupby('brand_clean')['price_clean'].median().sort_values(ascending=True)

# Box plot
bp = ax2.boxplot([df_top[df_top['brand_clean'] == brand]['price_clean'].dropna() 
                  for brand in brand_medians.index],
                 labels=brand_medians.index, patch_artist=True, vert=True)

# Color the boxes
for patch, color in zip(bp['boxes'], box_colors):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)
for whisker in bp['whiskers']:
    whisker.set_color('white')
for cap in bp['caps']:
    cap.set_color('white')
for median in bp['medians']:
    median.set_color('#ff6b6b')
    median.set_linewidth(2)
for flier in bp['fliers']:
    flier.set(marker='o', markerfacecolor='#666', markersize=3, alpha=0.5)

ax2.set_ylabel('Price ($)', color='white', fontsize=12)
ax2.set_title('💵 Price by Brand (Top 6)', color='white', fontsize=16, fontweight='bold')
ax2.tick_params(colors='white', axis='both')
for spine in ax2.spines.values():
    spine.set_color('#444')

# Add median labels
for i, (brand, median) in enumerate(brand_medians.items()):
    ax2.text(i + 1, median + 100, f'${median:,.0f}', ha='center', color='white', fontsize=9)

plt.tight_layout()
plt.savefig(output_path, dpi=150, facecolor='#1a1a2e', edgecolor='none', bbox_inches='tight')
plt.close()

print(f"✅ Saved: {output_path}")
print(f"   Median price: ${df_price['price_clean'].median():,.2f}")
print(f"   Price range: ${df_price['price_clean'].min():,.2f} - ${df_price['price_clean'].max():,.2f}")
