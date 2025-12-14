"""
06 - Graphics Card Analysis
Compares Integrated vs Dedicated graphics and top GPU brands
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# Setup paths
script_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(script_dir)
data_path = os.path.join(project_dir, 'laptops.csv')
output_path = os.path.join(project_dir, 'graphs', '06_graphics_analysis.png')

# Load data
df = pd.read_csv(data_path)

# Categorize graphics
def categorize_graphics(g):
    if pd.isna(g):
        return 'Unknown'
    g_lower = str(g).lower()
    if 'dedicated' in g_lower or 'rtx' in g_lower or 'nvidia' in g_lower or 'geforce' in g_lower:
        return 'Dedicated'
    elif 'integrated' in g_lower or 'intel' in g_lower or 'uhd' in g_lower or 'iris' in g_lower:
        return 'Integrated'
    else:
        return 'Other'

df['graphics_type'] = df['graphics'].apply(categorize_graphics)

# Clean price
df['price_clean'] = df['Price'].str.replace('$', '', regex=False).str.replace(',', '', regex=False).str.strip()
df['price_clean'] = pd.to_numeric(df['price_clean'], errors='coerce')

# Create figure
fig, axes = plt.subplots(1, 2, figsize=(16, 8))
fig.patch.set_facecolor('#1a1a2e')

# ----- Plot 1: Graphics Type Distribution -----
ax1 = axes[0]
ax1.set_facecolor('#1a1a2e')

graphics_counts = df['graphics_type'].value_counts()
colors = {'Dedicated': '#76b900', 'Integrated': '#0071c5', 'Other': '#666', 'Unknown': '#444'}
pie_colors = [colors.get(t, '#888') for t in graphics_counts.index]

wedges, texts, autotexts = ax1.pie(graphics_counts.values, labels=graphics_counts.index, 
                                    autopct='%1.1f%%', colors=pie_colors,
                                    explode=[0.02]*len(graphics_counts),
                                    textprops={'color': 'white', 'fontsize': 12})

for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontweight('bold')

ax1.set_title('🎮 Graphics Type Distribution', color='white', fontsize=16, fontweight='bold')

# Legend with icons
ax1.legend(['🟢 Dedicated (Gaming)', '🔵 Integrated', '⚫ Other/Unknown'], 
           loc='lower right', facecolor='#2a2a4e', labelcolor='white')

# ----- Plot 2: Price by Graphics Type -----
ax2 = axes[1]
ax2.set_facecolor('#1a1a2e')

# Filter valid prices
df_valid = df[(df['price_clean'] >= 50) & (df['price_clean'] <= 10000)].copy()

# Calculate stats by graphics type
stats = df_valid.groupby('graphics_type')['price_clean'].agg(['mean', 'median', 'count'])
stats = stats.sort_values('mean', ascending=True)

bar_colors = [colors.get(t, '#888') for t in stats.index]
bars = ax2.barh(range(len(stats)), stats['mean'], color=bar_colors)

# Add value labels
for i, (bar, row) in enumerate(zip(bars, stats.itertuples())):
    ax2.text(bar.get_width() + 30, bar.get_y() + bar.get_height()/2, 
             f'${row.mean:,.0f} (n={row.count:,})',
             va='center', ha='left', color='white', fontsize=11)

ax2.set_yticks(range(len(stats)))
ax2.set_yticklabels(stats.index, color='white', fontsize=12)
ax2.set_xlabel('Average Price ($)', color='white', fontsize=12)
ax2.set_title('💰 Average Price by Graphics Type', color='white', fontsize=16, fontweight='bold')
ax2.tick_params(colors='white')
for spine in ax2.spines.values():
    spine.set_color('#444')
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig(output_path, dpi=150, facecolor='#1a1a2e', edgecolor='none', bbox_inches='tight')
plt.close()

print(f"✅ Saved: {output_path}")
dedicated = graphics_counts.get('Dedicated', 0)
integrated = graphics_counts.get('Integrated', 0)
print(f"   Dedicated GPUs: {dedicated:,} ({dedicated/len(df)*100:.1f}%)")
print(f"   Integrated GPUs: {integrated:,} ({integrated/len(df)*100:.1f}%)")
