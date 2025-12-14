"""
GIF 02 - Price Scatter Buildup
Animated scatter plot showing laptops appearing by price
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import os
import io

# Setup paths
script_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(script_dir)
data_path = os.path.join(project_dir, 'laptops.csv')
output_path = os.path.join(project_dir, 'gifs', '02_price_scatter.gif')

# Load data
df = pd.read_csv(data_path)
df['price'] = df['Price'].str.replace('$', '', regex=False).str.replace(',', '', regex=False).str.strip()
df['price'] = pd.to_numeric(df['price'], errors='coerce')
df['ram_gb'] = df['ram'].str.extract(r'(\d+)').astype(float)

# Filter valid
df_valid = df[(df['price'] >= 100) & (df['price'] <= 5000) & 
              (df['rating'] >= 1) & (df['ram_gb'].notna())].copy()

# Sample for performance
df_sample = df_valid.sample(n=min(500, len(df_valid)), random_state=42)
df_sample = df_sample.sort_values('price')

# Create frames
frames = []
n_frames = 40
chunk_size = len(df_sample) // n_frames

for i in range(n_frames + 1):
    fig, ax = plt.subplots(figsize=(12, 8))
    fig.patch.set_facecolor('#0d1117')
    ax.set_facecolor('#0d1117')
    
    # Show points up to current frame
    n_points = min(i * chunk_size + chunk_size, len(df_sample))
    subset = df_sample.iloc[:n_points]
    
    if len(subset) > 0:
        scatter = ax.scatter(subset['price'], subset['rating'], 
                            c=subset['ram_gb'], cmap='viridis',
                            s=50, alpha=0.7, edgecolors='white', linewidth=0.5)
        
        if i == n_frames:
            cbar = plt.colorbar(scatter, ax=ax, shrink=0.8)
            cbar.set_label('RAM (GB)', color='white', fontsize=10)
            cbar.ax.tick_params(colors='white')
    
    ax.set_xlim(0, 5200)
    ax.set_ylim(0.5, 5.5)
    ax.set_xlabel('Price ($)', color='white', fontsize=12)
    ax.set_ylabel('Rating', color='white', fontsize=12)
    ax.set_title(f'💻 Laptop Market Overview\n{n_points:,} laptops shown', 
                 color='white', fontsize=16, fontweight='bold')
    ax.tick_params(colors='white')
    for spine in ax.spines.values():
        spine.set_color('#30363d')
    
    # Save frame
    buf = io.BytesIO()
    plt.savefig(buf, format='png', facecolor='#0d1117', bbox_inches='tight', dpi=100)
    buf.seek(0)
    frames.append(Image.open(buf).copy())
    buf.close()
    plt.close()

# Hold last frame
for _ in range(15):
    frames.append(frames[-1])

# Save GIF
frames[0].save(output_path, save_all=True, append_images=frames[1:], 
               duration=100, loop=0, optimize=True)

print(f"✅ Saved: {output_path}")
