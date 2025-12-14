"""
07 - Top Selling Laptops Analysis
Identifies best sellers by total sales revenue
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# Setup paths
script_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(script_dir)
data_path = os.path.join(project_dir, 'laptops.csv')
output_path = os.path.join(project_dir, 'graphs', '07_top_sellers.png')

# Load data
df = pd.read_csv(data_path)

# Clean price and sales columns
df['price_clean'] = df['Price'].str.replace('$', '', regex=False).str.replace(',', '', regex=False).str.strip()
df['price_clean'] = pd.to_numeric(df['price_clean'], errors='coerce')

# Total Sales is already numeric
df['total_sales_clean'] = pd.to_numeric(df['Total Sales'], errors='coerce')

# Create a label for each laptop
df['label'] = df['brand'].fillna('') + ' ' + df['model'].fillna('')
df['label'] = df['label'].str.strip()

# Filter valid data
df_valid = df[(df['total_sales_clean'] > 0) & (df['price_clean'] > 0)].copy()

# Top 10 by total sales
top_revenue = df_valid.nlargest(10, 'total_sales_clean')[['label', 'brand', 'total_sales_clean', 'price_clean', 'Sale Product Count']]

# Create figure
fig, axes = plt.subplots(1, 2, figsize=(16, 8))
fig.patch.set_facecolor('#1a1a2e')

# ----- Plot 1: Top 10 by Revenue -----
ax1 = axes[0]
ax1.set_facecolor('#1a1a2e')

colors = plt.cm.RdYlGn(np.linspace(0.3, 0.9, len(top_revenue)))[::-1]
bars = ax1.barh(range(len(top_revenue)), top_revenue['total_sales_clean'] / 1000, color=colors)

# Truncate long labels
labels = [l[:30] + '...' if len(l) > 30 else l for l in top_revenue['label']]

# Add value labels
for i, (bar, val) in enumerate(zip(bars, top_revenue['total_sales_clean'])):
    ax1.text(bar.get_width() + 2, bar.get_y() + bar.get_height()/2, f'${val/1000:,.0f}K',
             va='center', ha='left', color='white', fontsize=10, fontweight='bold')

ax1.set_yticks(range(len(top_revenue)))
ax1.set_yticklabels(labels, color='white', fontsize=9)
ax1.invert_yaxis()
ax1.set_xlabel('Total Sales Revenue ($K)', color='white', fontsize=12)
ax1.set_title('🏆 Top 10 Laptops by Revenue', color='white', fontsize=16, fontweight='bold')
ax1.tick_params(colors='white')
for spine in ax1.spines.values():
    spine.set_color('#444')
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)

# ----- Plot 2: Brand Revenue Share -----
ax2 = axes[1]
ax2.set_facecolor('#1a1a2e')

# Aggregate by brand
brand_revenue = df_valid.groupby('brand')['total_sales_clean'].sum().sort_values(ascending=False).head(8)

colors2 = plt.cm.cool(np.linspace(0.2, 0.8, len(brand_revenue)))
bars2 = ax2.barh(range(len(brand_revenue)), brand_revenue.values / 1000, color=colors2)

# Add value labels
for i, (bar, val) in enumerate(zip(bars2, brand_revenue.values)):
    ax2.text(bar.get_width() + 5, bar.get_y() + bar.get_height()/2, f'${val/1000:,.0f}K',
             va='center', ha='left', color='white', fontsize=10, fontweight='bold')

ax2.set_yticks(range(len(brand_revenue)))
ax2.set_yticklabels(brand_revenue.index, color='white', fontsize=11)
ax2.invert_yaxis()
ax2.set_xlabel('Total Revenue ($K)', color='white', fontsize=12)
ax2.set_title('💰 Top Brands by Total Revenue', color='white', fontsize=16, fontweight='bold')
ax2.tick_params(colors='white')
for spine in ax2.spines.values():
    spine.set_color('#444')
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig(output_path, dpi=150, facecolor='#1a1a2e', edgecolor='none', bbox_inches='tight')
plt.close()

print(f"✅ Saved: {output_path}")
print(f"   #1 Revenue: {top_revenue.iloc[0]['label']} (${top_revenue.iloc[0]['total_sales_clean']:,.0f})")
print(f"   Top brand: {brand_revenue.index[0]} (${brand_revenue.values[0]:,.0f})")
