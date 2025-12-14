"""
GIF 03 - Stats Counter
Animated statistics counter showing key metrics
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
output_path = os.path.join(project_dir, 'gifs', '03_stats_counter.gif')

# Load data
df = pd.read_csv(data_path)
df['price'] = df['Price'].str.replace('$', '', regex=False).str.replace(',', '', regex=False).str.strip()
df['price'] = pd.to_numeric(df['price'], errors='coerce')
df['revenue'] = pd.to_numeric(df['Total Sales'], errors='coerce')

# Target values
targets = {
    'Total Laptops': len(df),
    'Brands': df['brand'].nunique(),
    'Avg Price': df['price'].median(),
    'Total Revenue': df['revenue'].sum() / 1e6,
}

# Create frames
frames = []
n_frames = 40

for frame in range(n_frames + 1):
    fig, ax = plt.subplots(figsize=(12, 8))
    fig.patch.set_facecolor('#0d1117')
    ax.set_facecolor('#0d1117')
    ax.axis('off')
    
    progress = frame / n_frames
    eased = 1 - (1 - progress) ** 3  # Ease out cubic
    
    # Draw stats
    y_positions = [0.75, 0.55, 0.35, 0.15]
    emojis = ['📦', '🏢', '💰', '📈']
    
    for i, (label, target) in enumerate(targets.items()):
        current_val = target * eased
        
        # Emoji
        ax.text(0.15, y_positions[i], emojis[i], fontsize=50, ha='center', va='center',
                transform=ax.transAxes)
        
        # Value
        if label == 'Total Laptops':
            val_text = f'{int(current_val):,}'
        elif label == 'Brands':
            val_text = f'{int(current_val)}'
        elif label == 'Avg Price':
            val_text = f'${current_val:,.0f}'
        else:
            val_text = f'${current_val:.1f}M'
        
        ax.text(0.45, y_positions[i], val_text, fontsize=36, ha='left', va='center',
                transform=ax.transAxes, color='#00d4ff', fontweight='bold')
        
        # Label
        ax.text(0.85, y_positions[i], label, fontsize=18, ha='right', va='center',
                transform=ax.transAxes, color='#8b949e')
    
    # Title
    ax.text(0.5, 0.92, '📊 Amazon Laptop Sales - Key Metrics', fontsize=22, 
            ha='center', va='center', transform=ax.transAxes, 
            color='white', fontweight='bold')
    
    # Save frame
    buf = io.BytesIO()
    plt.savefig(buf, format='png', facecolor='#0d1117', bbox_inches='tight', dpi=100)
    buf.seek(0)
    frames.append(Image.open(buf).copy())
    buf.close()
    plt.close()

# Hold last frame
for _ in range(20):
    frames.append(frames[-1])

# Save GIF
frames[0].save(output_path, save_all=True, append_images=frames[1:], 
               duration=60, loop=0, optimize=True)

print(f"✅ Saved: {output_path}")
