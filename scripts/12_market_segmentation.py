"""
12 - Market Segmentation (K-Means)
Segments laptops into market categories
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import os
import warnings
warnings.filterwarnings('ignore')

# Setup paths
script_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(script_dir)
data_path = os.path.join(project_dir, 'laptops.csv')
output_path = os.path.join(project_dir, 'graphs', '12_market_segmentation.png')

print("Loading data...")
df = pd.read_csv(data_path)

# Clean price column
df['Price'] = pd.to_numeric(df['Price'].astype(str).str.replace('$', '').str.replace(',', '').str.strip(), errors='coerce')

# Clean and prepare data
df = df.dropna(subset=['Price'])
df = df[df['Price'] > 0]

# Feature engineering
df['RAM_GB'] = pd.to_numeric(df['ram'].astype(str).str.extract(r'(\d+)')[0], errors='coerce').fillna(8)
df['Screen_Inches'] = pd.to_numeric(df['screen_size'].astype(str).str.extract(r'([\d.]+)')[0], errors='coerce').fillna(15.6)

# Features for clustering
features = ['Price', 'RAM_GB', 'Screen_Inches']
X = df[features].fillna(0)

# Scale
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Find optimal k
inertias = []
K_range = range(2, 8)
for k in K_range:
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    km.fit(X_scaled)
    inertias.append(km.inertia_)

# Use 4 clusters
n_clusters = 4
print(f"Clustering with {n_clusters} segments...")
kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
df['Segment'] = kmeans.fit_predict(X_scaled)

# PCA for viz
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)
df['pca1'] = X_pca[:, 0]
df['pca2'] = X_pca[:, 1]

# Segment profiles
segment_stats = df.groupby('Segment').agg({
    'Price': 'mean',
    'RAM_GB': 'mean',
    'Screen_Inches': 'mean',
    'brand': 'count'
}).rename(columns={'brand': 'Count'})

# Name segments
segment_names = {}
sorted_by_price = segment_stats.sort_values('Price')
segment_names[sorted_by_price.index[0]] = 'Budget'
segment_names[sorted_by_price.index[1]] = 'Entry'
segment_names[sorted_by_price.index[2]] = 'Professional'
segment_names[sorted_by_price.index[3]] = 'Premium'

df['Segment_Name'] = df['Segment'].map(segment_names)

colors = ['#4ecdc4', '#45b7d1', '#ff6b6b', '#ffd93d']

# Create visualization
fig, axes = plt.subplots(2, 2, figsize=(16, 14))
fig.patch.set_facecolor('#0d1117')
fig.suptitle('Market Segmentation (K-Means)', fontsize=22, fontweight='bold', color='white', y=0.98)

# Plot 1: PCA scatter
ax1 = axes[0, 0]
ax1.set_facecolor('#0d1117')
for i, (seg_id, name) in enumerate(segment_names.items()):
    mask = df['Segment'] == seg_id
    ax1.scatter(df.loc[mask, 'pca1'], df.loc[mask, 'pca2'], 
                c=colors[i], s=30, alpha=0.6, label=name)
ax1.set_xlabel('PC1', color='white')
ax1.set_ylabel('PC2', color='white')
ax1.set_title('Market Segments (PCA)', color='white', fontsize=14, fontweight='bold')
ax1.legend(facecolor='#161b22', labelcolor='white')
ax1.tick_params(colors='white')
for spine in ax1.spines.values(): spine.set_color('#30363d')

# Plot 2: Segment sizes
ax2 = axes[0, 1]
ax2.set_facecolor('#0d1117')
segment_counts = df['Segment_Name'].value_counts().reindex(['Budget', 'Entry', 'Professional', 'Premium'])
wedges, texts, autotexts = ax2.pie(segment_counts.values, labels=segment_counts.index,
                                    autopct='%1.1f%%', colors=colors,
                                    textprops={'color': 'white'})
ax2.set_title('Segment Distribution', color='white', fontsize=14, fontweight='bold')

# Plot 3: Avg price by segment
ax3 = axes[1, 0]
ax3.set_facecolor('#0d1117')
segment_order = ['Budget', 'Entry', 'Professional', 'Premium']
prices = [segment_stats.loc[k, 'Price'] for k, v in segment_names.items() if v in segment_order]
bars = ax3.bar(segment_order, sorted(prices), color=colors)
for bar, price in zip(bars, sorted(prices)):
    ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 20, f'${price:.0f}',
             ha='center', color='white', fontsize=10, fontweight='bold')
ax3.set_ylabel('Avg Price ($)', color='white')
ax3.set_title('Average Price by Segment', color='white', fontsize=14, fontweight='bold')
ax3.tick_params(colors='white')
for spine in ax3.spines.values(): spine.set_color('#30363d')

# Plot 4: Elbow
ax4 = axes[1, 1]
ax4.set_facecolor('#0d1117')
ax4.plot(list(K_range), inertias, 'o-', color='#4ecdc4', linewidth=2, markersize=8)
ax4.axvline(x=n_clusters, color='#ff6b6b', linestyle='--', linewidth=2, label=f'K={n_clusters}')
ax4.set_xlabel('K', color='white')
ax4.set_ylabel('Inertia', color='white')
ax4.set_title('Elbow Method', color='white', fontsize=14, fontweight='bold')
ax4.legend(facecolor='#161b22', labelcolor='white')
ax4.tick_params(colors='white')
for spine in ax4.spines.values(): spine.set_color('#30363d')

plt.tight_layout()
plt.subplots_adjust(top=0.92)
plt.savefig(output_path, dpi=150, facecolor='#0d1117', bbox_inches='tight')
plt.close()

print(f"Saved: {output_path}")
