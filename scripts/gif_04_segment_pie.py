"""
GIF 04 - Segment Pie Animation
Animated pie chart showing market segments
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
output_path = os.path.join(project_dir, 'gifs', '04_segment_pie.gif')

# Load data
df = pd.read_csv(data_path)
df['price'] = df['Price'].str.replace('$', '', regex=False).str.replace(',', '', regex=False).str.strip()
df['price'] = pd.to_numeric(df['price'], errors='coerce')

def get_gpu(g):
    if pd.isna(g): return 'Unknown'
    g = str(g).lower()
    if any(x in g for x in ['dedicated', 'rtx', 'gtx', 'nvidia']): return 'Dedicated'
    return 'Integrated'

df['gpu_type'] = df['graphics'].apply(get_gpu)

def segment(row):
    p = row['price'] if pd.notna(row['price']) else 500
    gpu = row['gpu_type']
    if gpu == 'Dedicated' and p > 1200: return 'Gaming/Workstation'
    elif gpu == 'Dedicated': return 'Gaming Budget'
    elif p > 1200: return 'Business Premium'
    elif p < 400: return 'Budget'
    elif p < 800: return 'Mid-Range'
    return 'Standard'

df['segment'] = df.apply(segment, axis=1)

# Segment data
seg_counts = df['segment'].value_counts()

# Colors
colors = {
    'Gaming/Workstation': '#76b900',
    'Gaming Budget': '#a4d65e', 
    'Business Premium': '#0078D4',
    'Standard': '#6e7681',
    'Mid-Range': '#58a6ff',
    'Budget': '#f97583'
}

# Create frames - pie growing
frames = []
n_frames = 30

for frame in range(n_frames + 1):
    fig, ax = plt.subplots(figsize=(10, 10))
    fig.patch.set_facecolor('#0d1117')
    ax.set_facecolor('#0d1117')
    
    progress = frame / n_frames
    
    # Animate by showing portion of pie
    if progress > 0:
        # Calculate visible portions
        visible = [min(v * progress * 1.5, v) for v in seg_counts.values]
        c = [colors.get(s, '#888') for s in seg_counts.index]
        
        wedges, texts = ax.pie(visible, colors=c, 
                               startangle=90, counterclock=False)
        
        # Add legend at the end
        if frame == n_frames:
            legend_labels = [f'{s}: {v:,} ({v/sum(seg_counts)*100:.1f}%)' 
                           for s, v in seg_counts.items()]
            ax.legend(wedges, legend_labels, loc='lower center', 
                     bbox_to_anchor=(0.5, -0.1), ncol=2,
                     facecolor='#161b22', labelcolor='white', fontsize=10)
    
    ax.set_title(f'📊 Market Segments', color='white', fontsize=20, fontweight='bold')
    
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
               duration=80, loop=0, optimize=True)

print(f"✅ Saved: {output_path}")
