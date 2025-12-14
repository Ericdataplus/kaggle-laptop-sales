"""
09 - Advanced Visualizations
Creates impressive, professional-grade charts for portfolio
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle
from matplotlib.collections import PatchCollection
import matplotlib.patheffects as path_effects
import os

# Setup paths
script_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(script_dir)
data_path = os.path.join(project_dir, 'laptops.csv')

# Load and clean data
df = pd.read_csv(data_path)

# Clean data
df['price'] = df['Price'].str.replace('$', '', regex=False).str.replace(',', '', regex=False).str.strip()
df['price'] = pd.to_numeric(df['price'], errors='coerce')
df['ram_gb'] = df['ram'].str.extract(r'(\d+)').astype(float)
df['brand_clean'] = df['brand'].str.upper().str.strip()
df['revenue'] = pd.to_numeric(df['Total Sales'], errors='coerce')

# Filter valid
df_valid = df[(df['price'] >= 100) & (df['price'] <= 8000) & (df['rating'] >= 1)].copy()

# GPU type
def get_gpu(g):
    if pd.isna(g): return 'Unknown'
    g = str(g).lower()
    if any(x in g for x in ['dedicated', 'rtx', 'gtx', 'nvidia', 'geforce']): return 'Dedicated'
    return 'Integrated'
df_valid['gpu_type'] = df_valid['graphics'].apply(get_gpu)

# ===== VISUALIZATION 1: BRAND POSITIONING SCATTER =====
output1 = os.path.join(project_dir, 'graphs', '09a_brand_positioning.png')

fig, ax = plt.subplots(figsize=(14, 10))
fig.patch.set_facecolor('#0d1117')
ax.set_facecolor('#0d1117')

# Calculate brand stats
brand_stats = df_valid.groupby('brand_clean').agg({
    'price': 'median',
    'rating': 'mean',
    'revenue': 'sum',
    'brand': 'count'
}).rename(columns={'brand': 'count'})

# Filter brands with 15+ listings
brand_stats = brand_stats[brand_stats['count'] >= 15]

# Bubble size based on revenue (normalized)
size_scale = (brand_stats['revenue'] / brand_stats['revenue'].max()) * 2000 + 100

# Color based on value (rating/price ratio)
brand_stats['value'] = brand_stats['rating'] / (brand_stats['price'] / 1000)
colors = plt.cm.RdYlGn((brand_stats['value'] - brand_stats['value'].min()) / 
                        (brand_stats['value'].max() - brand_stats['value'].min()))

scatter = ax.scatter(brand_stats['price'], brand_stats['rating'], 
                     s=size_scale, c=colors, alpha=0.7, edgecolors='white', linewidth=2)

# Add labels
for brand, row in brand_stats.iterrows():
    ax.annotate(brand, (row['price'], row['rating']), 
                fontsize=9, color='white', fontweight='bold',
                ha='center', va='bottom', 
                xytext=(0, 8), textcoords='offset points')

# Add quadrant lines
ax.axhline(y=brand_stats['rating'].median(), color='#30363d', linestyle='--', alpha=0.7)
ax.axvline(x=brand_stats['price'].median(), color='#30363d', linestyle='--', alpha=0.7)

# Quadrant labels
ax.text(0.05, 0.95, '🏆 HIGH VALUE\nHigh Rating, Low Price', transform=ax.transAxes,
        fontsize=10, color='#58a6ff', va='top', ha='left', style='italic')
ax.text(0.95, 0.95, '💎 PREMIUM\nHigh Rating, High Price', transform=ax.transAxes,
        fontsize=10, color='#56d364', va='top', ha='right', style='italic')
ax.text(0.05, 0.05, '⚠️ BUDGET\nLow Rating, Low Price', transform=ax.transAxes,
        fontsize=10, color='#f97583', va='bottom', ha='left', style='italic')
ax.text(0.95, 0.05, '❌ OVERPRICED\nLow Rating, High Price', transform=ax.transAxes,
        fontsize=10, color='#ffa657', va='bottom', ha='right', style='italic')

ax.set_xlabel('Median Price ($)', fontsize=12, color='white')
ax.set_ylabel('Average Rating', fontsize=12, color='white')
ax.set_title('🗺️ Brand Positioning Map\nBubble size = Total Revenue', 
             fontsize=16, color='white', fontweight='bold', pad=20)

ax.tick_params(colors='white')
for spine in ax.spines.values():
    spine.set_color('#30363d')

plt.tight_layout()
plt.savefig(output1, dpi=150, facecolor='#0d1117', bbox_inches='tight')
plt.close()
print(f"✅ Saved: {output1}")

# ===== VISUALIZATION 2: PRICE-SPEC HEATMAP =====
output2 = os.path.join(project_dir, 'graphs', '09b_spec_heatmap.png')

fig, ax = plt.subplots(figsize=(12, 8))
fig.patch.set_facecolor('#0d1117')
ax.set_facecolor('#0d1117')

# Create RAM vs Price bins
ram_bins = [0, 4, 8, 16, 32, 64, 128]
ram_labels = ['≤4GB', '5-8GB', '9-16GB', '17-32GB', '33-64GB', '65+GB']
price_bins = [0, 400, 600, 800, 1000, 1500, 2000, 10000]
price_labels = ['<$400', '$400-600', '$600-800', '$800-1K', '$1-1.5K', '$1.5-2K', '>$2K']

df_valid['ram_bin'] = pd.cut(df_valid['ram_gb'], bins=ram_bins, labels=ram_labels)
df_valid['price_bin'] = pd.cut(df_valid['price'], bins=price_bins, labels=price_labels)

# Create pivot table
heatmap_data = df_valid.pivot_table(values='rating', index='price_bin', columns='ram_bin', aggfunc='mean')

# Plot heatmap
im = ax.imshow(heatmap_data.values, cmap='RdYlGn', aspect='auto', vmin=3.5, vmax=4.8)

# Add colorbar
cbar = plt.colorbar(im, ax=ax, shrink=0.8)
cbar.set_label('Avg Rating', color='white', fontsize=11)
cbar.ax.tick_params(colors='white')

# Labels
ax.set_xticks(range(len(heatmap_data.columns)))
ax.set_xticklabels(heatmap_data.columns, color='white', fontsize=10)
ax.set_yticks(range(len(heatmap_data.index)))
ax.set_yticklabels(heatmap_data.index, color='white', fontsize=10)

# Add values
for i in range(len(heatmap_data.index)):
    for j in range(len(heatmap_data.columns)):
        val = heatmap_data.iloc[i, j]
        if pd.notna(val):
            text = ax.text(j, i, f'{val:.2f}', ha='center', va='center', 
                          color='white' if val < 4.2 else 'black', fontsize=10, fontweight='bold')

ax.set_xlabel('RAM', fontsize=12, color='white')
ax.set_ylabel('Price Range', fontsize=12, color='white')
ax.set_title('📊 Average Rating by Price & RAM\nFinding the Sweet Spot', 
             fontsize=16, color='white', fontweight='bold', pad=20)

plt.tight_layout()
plt.savefig(output2, dpi=150, facecolor='#0d1117', bbox_inches='tight')
plt.close()
print(f"✅ Saved: {output2}")

# ===== VISUALIZATION 3: SEGMENT BREAKDOWN =====
output3 = os.path.join(project_dir, 'graphs', '09c_market_segments.png')

fig, axes = plt.subplots(1, 2, figsize=(16, 8))
fig.patch.set_facecolor('#0d1117')

# Define segments
def segment(row):
    p = row['price']
    gpu = row['gpu_type']
    if gpu == 'Dedicated' and p > 1200: return 'Gaming/Workstation'
    elif gpu == 'Dedicated': return 'Gaming Budget'
    elif p > 1200: return 'Business Premium'
    elif p < 400: return 'Budget'
    elif p < 800: return 'Mid-Range'
    return 'Standard'

df_valid['segment'] = df_valid.apply(segment, axis=1)

segment_colors = {
    'Gaming/Workstation': '#76b900',
    'Gaming Budget': '#a4d65e',
    'Business Premium': '#0078D4',
    'Standard': '#6e7681',
    'Mid-Range': '#58a6ff',
    'Budget': '#f97583'
}

# Pie chart
ax1 = axes[0]
ax1.set_facecolor('#0d1117')

seg_counts = df_valid['segment'].value_counts()
colors = [segment_colors.get(s, '#888') for s in seg_counts.index]

wedges, texts, autotexts = ax1.pie(seg_counts.values, labels=seg_counts.index,
                                    autopct='%1.1f%%', colors=colors,
                                    explode=[0.02]*len(seg_counts),
                                    textprops={'color': 'white', 'fontsize': 11})
for at in autotexts:
    at.set_fontweight('bold')

ax1.set_title('📦 Market Segment Distribution', color='white', fontsize=14, fontweight='bold')

# Revenue by segment
ax2 = axes[1]
ax2.set_facecolor('#0d1117')

seg_revenue = df_valid.groupby('segment')['revenue'].sum().sort_values()
colors2 = [segment_colors.get(s, '#888') for s in seg_revenue.index]

bars = ax2.barh(range(len(seg_revenue)), seg_revenue.values / 1e6, color=colors2)

for i, (bar, val) in enumerate(zip(bars, seg_revenue.values)):
    ax2.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2,
             f'${val/1e6:.1f}M', va='center', color='white', fontsize=11, fontweight='bold')

ax2.set_yticks(range(len(seg_revenue)))
ax2.set_yticklabels(seg_revenue.index, color='white', fontsize=11)
ax2.set_xlabel('Total Revenue ($ Millions)', color='white', fontsize=12)
ax2.set_title('💰 Revenue by Segment', color='white', fontsize=14, fontweight='bold')
ax2.tick_params(colors='white')
for spine in ax2.spines.values():
    spine.set_color('#30363d')

plt.tight_layout()
plt.savefig(output3, dpi=150, facecolor='#0d1117', bbox_inches='tight')
plt.close()
print(f"✅ Saved: {output3}")

# ===== VISUALIZATION 4: VALUE SCORE DISTRIBUTION =====
output4 = os.path.join(project_dir, 'graphs', '09d_value_analysis.png')

fig, ax = plt.subplots(figsize=(14, 8))
fig.patch.set_facecolor('#0d1117')
ax.set_facecolor('#0d1117')

# Calculate value score
df_valid['ram_norm'] = df_valid['ram_gb'].fillna(8) / 64
df_valid['rating_norm'] = (df_valid['rating'] - 1) / 4
df_valid['gpu_score'] = df_valid['gpu_type'].map({'Dedicated': 1, 'Integrated': 0.4, 'Unknown': 0.3})
df_valid['value_score'] = (df_valid['ram_norm'] * 0.3 + df_valid['rating_norm'] * 0.4 + 
                           df_valid['gpu_score'] * 0.3) / (df_valid['price'] / 1000)

# Scatter: Price vs Rating, color by value score
scatter = ax.scatter(df_valid['price'], df_valid['rating'], 
                     c=df_valid['value_score'], cmap='RdYlGn', 
                     alpha=0.6, s=30, edgecolors='none')

cbar = plt.colorbar(scatter, ax=ax, shrink=0.8)
cbar.set_label('Value Score\n(Higher = Better Deal)', color='white', fontsize=11)
cbar.ax.tick_params(colors='white')

# Highlight top deals
top_deals = df_valid.nlargest(5, 'value_score')
for _, row in top_deals.iterrows():
    ax.scatter(row['price'], row['rating'], s=200, facecolors='none', 
               edgecolors='#00ff00', linewidth=3)
    ax.annotate(f"🔥 {row['brand']}", (row['price'], row['rating']),
                color='#00ff00', fontsize=9, fontweight='bold',
                xytext=(10, 10), textcoords='offset points')

ax.set_xlabel('Price ($)', fontsize=12, color='white')
ax.set_ylabel('Rating', fontsize=12, color='white')
ax.set_title('💎 Value Analysis: Finding the Best Deals\nGreen = High Value, Red = Low Value, Circles = Top 5 Deals',
             fontsize=14, color='white', fontweight='bold', pad=20)

ax.tick_params(colors='white')
for spine in ax.spines.values():
    spine.set_color('#30363d')

plt.tight_layout()
plt.savefig(output4, dpi=150, facecolor='#0d1117', bbox_inches='tight')
plt.close()
print(f"✅ Saved: {output4}")

print("\n🎉 All advanced visualizations complete!")
