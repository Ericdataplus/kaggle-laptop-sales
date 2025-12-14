"""
05 - Screen Size Analysis
Visualizes screen size distribution and trends
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# Setup paths
script_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(script_dir)
data_path = os.path.join(project_dir, 'laptops.csv')
output_path = os.path.join(project_dir, 'graphs', '05_screen_size_analysis.png')

# Load data
df = pd.read_csv(data_path)

# Extract screen size (numeric)
df['screen_inches'] = df['screen_size'].str.extract(r'([\d.]+)').astype(float)

# Filter valid screen sizes
df_screen = df[(df['screen_inches'] >= 10) & (df['screen_inches'] <= 18)].copy()

# Bin screen sizes
bins = [10, 12, 13, 14, 15, 16, 17, 18]
labels = ['10-12"', '12-13"', '13-14"', '14-15"', '15-16"', '16-17"', '17-18"']
df_screen['screen_bin'] = pd.cut(df_screen['screen_inches'], bins=bins, labels=labels, right=True)

# Create figure
fig, axes = plt.subplots(1, 2, figsize=(16, 8))
fig.patch.set_facecolor('#1a1a2e')

# ----- Plot 1: Screen Size Distribution -----
ax1 = axes[0]
ax1.set_facecolor('#1a1a2e')

# Most common exact sizes
exact_sizes = df_screen['screen_inches'].value_counts().head(8)

colors = plt.cm.cool(np.linspace(0.2, 0.8, len(exact_sizes)))
bars = ax1.bar([f'{s}"' for s in exact_sizes.index], exact_sizes.values, color=colors)

# Add value labels
for bar, val in zip(bars, exact_sizes.values):
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 20, f'{val:,}',
             ha='center', va='bottom', color='white', fontsize=10, fontweight='bold')

ax1.set_xlabel('Screen Size', color='white', fontsize=12)
ax1.set_ylabel('Number of Laptops', color='white', fontsize=12)
ax1.set_title('📺 Most Common Screen Sizes', color='white', fontsize=16, fontweight='bold')
ax1.tick_params(colors='white')
for spine in ax1.spines.values():
    spine.set_color('#444')

# ----- Plot 2: Screen Size Ranges -----
ax2 = axes[1]
ax2.set_facecolor('#1a1a2e')

bin_counts = df_screen['screen_bin'].value_counts().sort_index()
colors2 = plt.cm.viridis(np.linspace(0.2, 0.9, len(bin_counts)))

# Horizontal bar chart
bars2 = ax2.barh(range(len(bin_counts)), bin_counts.values, color=colors2)

# Add value labels
for i, (bar, val) in enumerate(zip(bars2, bin_counts.values)):
    pct = val / bin_counts.sum() * 100
    ax2.text(val + 20, bar.get_y() + bar.get_height()/2, f'{val:,} ({pct:.1f}%)',
             va='center', ha='left', color='white', fontsize=11)

ax2.set_yticks(range(len(bin_counts)))
ax2.set_yticklabels(bin_counts.index, color='white', fontsize=11)
ax2.set_xlabel('Number of Laptops', color='white', fontsize=12)
ax2.set_title('📏 Screen Size Categories', color='white', fontsize=16, fontweight='bold')
ax2.tick_params(colors='white')
for spine in ax2.spines.values():
    spine.set_color('#444')
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig(output_path, dpi=150, facecolor='#1a1a2e', edgecolor='none', bbox_inches='tight')
plt.close()

print(f"✅ Saved: {output_path}")
print(f"   Most common size: {exact_sizes.index[0]}\" ({exact_sizes.values[0]:,} laptops)")
