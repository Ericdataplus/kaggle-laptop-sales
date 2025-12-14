"""
11 - Brand Market Analysis
Analyzes laptop brands and what drives prices in this dataset
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import warnings
warnings.filterwarnings('ignore')

# Setup paths
script_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(script_dir)
data_path = os.path.join(project_dir, 'laptops.csv')
output_path = os.path.join(project_dir, 'graphs', '11_price_prediction.png')

print("Loading data...")
df = pd.read_csv(data_path)

# Clean price column
df['Price'] = pd.to_numeric(df['Price'].astype(str).str.replace('$', '').str.replace(',', '').str.strip(), errors='coerce')
df = df.dropna(subset=['Price'])
df = df[df['Price'] > 100]
df = df[df['Price'] < 5000]

# Clean brand
df['brand_clean'] = df['brand'].str.upper().str.strip()

# Extract RAM
df['RAM_GB'] = pd.to_numeric(df['ram'].astype(str).str.extract(r'(\d+)')[0], errors='coerce').fillna(8)

# Processor tier
def get_processor_tier(cpu):
    cpu = str(cpu).lower()
    if 'i9' in cpu or 'ryzen 9' in cpu: return 'i9/Ryzen 9'
    if 'i7' in cpu or 'ryzen 7' in cpu: return 'i7/Ryzen 7'
    if 'i5' in cpu or 'ryzen 5' in cpu: return 'i5/Ryzen 5'
    if 'i3' in cpu or 'ryzen 3' in cpu: return 'i3/Ryzen 3'
    return 'Other'

df['Processor_Tier'] = df['cpu'].apply(get_processor_tier)

print(f"Analyzing {len(df):,} laptops")

# Brand statistics
brand_stats = df.groupby('brand_clean').agg({
    'Price': ['mean', 'median', 'count', 'std'],
    'RAM_GB': 'mean'
}).round(2)
brand_stats.columns = ['avg_price', 'median_price', 'count', 'price_std', 'avg_ram']
brand_stats = brand_stats[brand_stats['count'] >= 20].sort_values('avg_price', ascending=False)

# Processor price impact
proc_stats = df.groupby('Processor_Tier').agg({
    'Price': ['mean', 'count']
}).round(0)
proc_stats.columns = ['avg_price', 'count']
proc_stats = proc_stats.sort_values('avg_price', ascending=False)

# RAM impact
ram_stats = df.groupby('RAM_GB').agg({
    'Price': 'mean'
}).round(0)

# Create visualization
fig, axes = plt.subplots(2, 2, figsize=(16, 14))
fig.patch.set_facecolor('#0d1117')
fig.suptitle('Laptop Market Analysis: What Drives Price?', fontsize=22, fontweight='bold', color='white', y=0.98)

# Plot 1: Brand pricing
ax1 = axes[0, 0]
ax1.set_facecolor('#0d1117')
top_brands = brand_stats.head(10)
colors = plt.cm.viridis(np.linspace(0.9, 0.3, len(top_brands)))
bars = ax1.barh(range(len(top_brands)), top_brands['avg_price'], color=colors)
ax1.set_yticks(range(len(top_brands)))
ax1.set_yticklabels(top_brands.index, color='white', fontsize=10)
ax1.set_xlabel('Average Price ($)', color='white')
ax1.set_title('Average Price by Brand', color='white', fontsize=14, fontweight='bold')
ax1.tick_params(colors='white')
ax1.invert_yaxis()
for spine in ax1.spines.values(): spine.set_color('#30363d')

# Add price labels
for i, (bar, price) in enumerate(zip(bars, top_brands['avg_price'])):
    ax1.text(bar.get_width() + 20, bar.get_y() + bar.get_height()/2, f'${price:.0f}',
             va='center', color='white', fontsize=9, fontweight='bold')

# Plot 2: Processor impact on price
ax2 = axes[0, 1]
ax2.set_facecolor('#0d1117')
proc_order = ['i9/Ryzen 9', 'i7/Ryzen 7', 'i5/Ryzen 5', 'i3/Ryzen 3', 'Other']
proc_prices = [proc_stats.loc[p, 'avg_price'] if p in proc_stats.index else 0 for p in proc_order]
colors2 = ['#ff6b6b', '#ffd93d', '#4ecdc4', '#45b7d1', '#96ceb4']
bars2 = ax2.bar(proc_order, proc_prices, color=colors2)
ax2.set_xlabel('Processor Tier', color='white')
ax2.set_ylabel('Average Price ($)', color='white')
ax2.set_title('Price by Processor Type', color='white', fontsize=14, fontweight='bold')
ax2.tick_params(colors='white', labelsize=8)
ax2.set_xticklabels(proc_order, rotation=15, ha='right')
for spine in ax2.spines.values(): spine.set_color('#30363d')

# Add value labels
for bar, val in zip(bars2, proc_prices):
    if val > 0:
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 30, f'${val:.0f}',
                 ha='center', color='white', fontsize=10, fontweight='bold')

# Plot 3: RAM impact on price
ax3 = axes[1, 0]
ax3.set_facecolor('#0d1117')
ram_vals = ram_stats.index.tolist()
ram_prices = ram_stats['Price'].values
ax3.plot(ram_vals, ram_prices, 'o-', color='#4ecdc4', linewidth=2, markersize=8)
ax3.fill_between(ram_vals, ram_prices, alpha=0.3, color='#4ecdc4')
ax3.set_xlabel('RAM (GB)', color='white')
ax3.set_ylabel('Average Price ($)', color='white')
ax3.set_title('RAM vs Price Relationship', color='white', fontsize=14, fontweight='bold')
ax3.tick_params(colors='white')
for spine in ax3.spines.values(): spine.set_color('#30363d')

# Plot 4: Key Insights
ax4 = axes[1, 1]
ax4.set_facecolor('#161b22')
ax4.set_xticks([])
ax4.set_yticks([])
for spine in ax4.spines.values(): spine.set_color('#30363d')

ax4.text(0.5, 0.95, 'Key Market Insights', fontsize=16, fontweight='bold', ha='center', color='white', transform=ax4.transAxes)

most_expensive = brand_stats.index[0]
cheapest = brand_stats.index[-1]
i7_premium = proc_stats.loc['i7/Ryzen 7', 'avg_price'] - proc_stats.loc['i5/Ryzen 5', 'avg_price'] if 'i7/Ryzen 7' in proc_stats.index and 'i5/Ryzen 5' in proc_stats.index else 0

insights = [
    ('Total Laptops:', f'{len(df):,}', '#ffd700'),
    ('Average Price:', f'${df["Price"].mean():.0f}', '#58a6ff'),
    ('Most Expensive Brand:', most_expensive, '#ff6b6b'),
    ('Budget Brand:', cheapest, '#4ecdc4'),
    ('i7 vs i5 Premium:', f'+${i7_premium:.0f}', '#56d364'),
    ('Price Range:', f'${df["Price"].min():.0f} - ${df["Price"].max():.0f}', '#a371f7'),
]

for i, (label, value, color) in enumerate(insights):
    y_pos = 0.80 - i * 0.11
    ax4.text(0.08, y_pos, label, fontsize=11, color='#8b949e', transform=ax4.transAxes, va='center')
    ax4.text(0.55, y_pos, value, fontsize=11, color=color, fontweight='bold', transform=ax4.transAxes, va='center')

plt.tight_layout()
plt.subplots_adjust(top=0.92)
plt.savefig(output_path, dpi=150, facecolor='#0d1117', bbox_inches='tight')
plt.close()

print(f"\nSaved: {output_path}")
print(f"\nKey Findings:")
print(f"  Most expensive brand: {most_expensive} (${brand_stats.loc[most_expensive, 'avg_price']:.0f})")
print(f"  i7 premium over i5: +${i7_premium:.0f}")
