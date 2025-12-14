"""
04 - Operating System Analysis
Visualizes OS market share among laptops on Amazon
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# Setup paths
script_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(script_dir)
data_path = os.path.join(project_dir, 'laptops.csv')
output_path = os.path.join(project_dir, 'graphs', '04_os_analysis.png')

# Load data
df = pd.read_csv(data_path)

# Clean and categorize OS
def categorize_os(os_name):
    if pd.isna(os_name):
        return 'Unknown'
    os_lower = str(os_name).lower()
    if 'windows 11' in os_lower:
        return 'Windows 11'
    elif 'windows 10' in os_lower:
        return 'Windows 10'
    elif 'windows' in os_lower:
        return 'Windows (Other)'
    elif 'chrome' in os_lower:
        return 'Chrome OS'
    elif 'mac' in os_lower:
        return 'macOS'
    else:
        return 'Other'

df['os_category'] = df['OS'].apply(categorize_os)

# Count by OS
os_counts = df['os_category'].value_counts()

# Create figure
fig, axes = plt.subplots(1, 2, figsize=(16, 8))
fig.patch.set_facecolor('#1a1a2e')

# Color mapping
os_colors = {
    'Windows 11': '#0078D4',
    'Windows 10': '#00A4EF', 
    'Windows (Other)': '#5DC2F1',
    'Chrome OS': '#4285F4',
    'macOS': '#A3AAAE',
    'Other': '#666666',
    'Unknown': '#444444'
}

colors = [os_colors.get(os, '#888') for os in os_counts.index]

# ----- Plot 1: Pie Chart -----
ax1 = axes[0]
ax1.set_facecolor('#1a1a2e')

# Filter for pie chart (top 5 + other)
if len(os_counts) > 5:
    top5 = os_counts.head(5)
    other_count = os_counts[5:].sum()
    pie_data = pd.concat([top5, pd.Series({'Other': other_count})])
else:
    pie_data = os_counts

pie_colors = [os_colors.get(os, '#888') for os in pie_data.index]

wedges, texts, autotexts = ax1.pie(pie_data.values, labels=pie_data.index, autopct='%1.1f%%',
                                    colors=pie_colors, explode=[0.02]*len(pie_data),
                                    textprops={'color': 'white', 'fontsize': 11})

for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontweight('bold')

ax1.set_title('🖥️ Operating System Market Share', color='white', fontsize=16, fontweight='bold')

# ----- Plot 2: Bar Chart with details -----
ax2 = axes[1]
ax2.set_facecolor('#1a1a2e')

bars = ax2.barh(range(len(os_counts)), os_counts.values, color=colors)

# Add value labels
for i, (bar, val) in enumerate(zip(bars, os_counts.values)):
    pct = val / os_counts.sum() * 100
    ax2.text(val + 20, bar.get_y() + bar.get_height()/2, f'{val:,} ({pct:.1f}%)',
             va='center', ha='left', color='white', fontsize=11)

ax2.set_yticks(range(len(os_counts)))
ax2.set_yticklabels(os_counts.index, color='white', fontsize=11)
ax2.invert_yaxis()
ax2.set_xlabel('Number of Laptops', color='white', fontsize=12)
ax2.set_title('📊 OS Distribution Details', color='white', fontsize=16, fontweight='bold')
ax2.tick_params(colors='white')
for spine in ax2.spines.values():
    spine.set_color('#444')
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig(output_path, dpi=150, facecolor='#1a1a2e', edgecolor='none', bbox_inches='tight')
plt.close()

print(f"✅ Saved: {output_path}")
print(f"   Most common OS: {os_counts.index[0]} ({os_counts.values[0]:,} laptops, {os_counts.values[0]/len(df)*100:.1f}%)")
