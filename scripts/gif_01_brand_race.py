"""
GIF 01 - Brand Race Animation
Animated bar chart race showing brands by revenue
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from PIL import Image
import os
import io

# Setup paths
script_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(script_dir)
data_path = os.path.join(project_dir, 'laptops.csv')
output_path = os.path.join(project_dir, 'gifs', '01_brand_race.gif')

# Load data
df = pd.read_csv(data_path)
df['brand_clean'] = df['brand'].str.upper().str.strip()
df['revenue'] = pd.to_numeric(df['Total Sales'], errors='coerce')

# Get top 8 brands by revenue
brand_revenue = df.groupby('brand_clean')['revenue'].sum().sort_values(ascending=False).head(8)

# Create frames for animation
frames = []
n_steps = 30

# Color mapping
colors = ['#00d4ff', '#00b4d8', '#0096c7', '#0077b6', '#023e8a', '#7b2cbf', '#9d4edd', '#c77dff']

for step in range(n_steps + 1):
    fig, ax = plt.subplots(figsize=(12, 6))
    fig.patch.set_facecolor('#0d1117')
    ax.set_facecolor('#0d1117')
    
    # Animate revenue growing
    progress = step / n_steps
    current_revenue = brand_revenue * progress
    
    # Sort and get top 8
    sorted_rev = current_revenue.sort_values(ascending=True)
    
    # Draw bars
    bars = ax.barh(range(len(sorted_rev)), sorted_rev.values / 1000, color=colors[::-1])
    
    # Add labels
    for i, (bar, (brand, val)) in enumerate(zip(bars, sorted_rev.items())):
        if val > 0:
            ax.text(bar.get_width() + 5, bar.get_y() + bar.get_height()/2,
                    f'${val/1000:,.0f}K', va='center', color='white', fontsize=10, fontweight='bold')
    
    ax.set_yticks(range(len(sorted_rev)))
    ax.set_yticklabels(sorted_rev.index, color='white', fontsize=11)
    ax.set_xlabel('Total Revenue ($K)', color='white', fontsize=12)
    ax.set_title(f'🏆 Brand Revenue Race\n{int(progress*100)}% Complete', 
                 color='white', fontsize=16, fontweight='bold')
    ax.set_xlim(0, brand_revenue.max() / 1000 * 1.15)
    ax.tick_params(colors='white')
    for spine in ax.spines.values():
        spine.set_color('#30363d')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    # Save frame to buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png', facecolor='#0d1117', bbox_inches='tight', dpi=100)
    buf.seek(0)
    frames.append(Image.open(buf).copy())
    buf.close()
    plt.close()

# Add pause at end
for _ in range(10):
    frames.append(frames[-1])

# Save GIF
frames[0].save(output_path, save_all=True, append_images=frames[1:], 
               duration=80, loop=0, optimize=True)

print(f"✅ Saved: {output_path}")
print(f"   Frames: {len(frames)}")
