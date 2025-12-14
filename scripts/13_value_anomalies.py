"""
13 - Value Anomaly Detection
Finds overpriced and undervalued laptops
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler, LabelEncoder
import os
import warnings
warnings.filterwarnings('ignore')

# Setup paths
script_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(script_dir)
data_path = os.path.join(project_dir, 'laptops.csv')
output_path = os.path.join(project_dir, 'graphs', '13_value_anomalies.png')

print("Loading data...")
df = pd.read_csv(data_path)

# Clean price column
df['Price'] = pd.to_numeric(df['Price'].astype(str).str.replace('$', '').str.replace(',', '').str.strip(), errors='coerce')

# Clean
df = df.dropna(subset=['Price'])
df = df[df['Price'] > 0]

# Features
df['RAM_GB'] = pd.to_numeric(df['ram'].astype(str).str.extract(r'(\d+)')[0], errors='coerce').fillna(8)
df['Screen_Inches'] = pd.to_numeric(df['screen_size'].astype(str).str.extract(r'([\d.]+)')[0], errors='coerce').fillna(15.6)
le = LabelEncoder()
df['Brand_Encoded'] = le.fit_transform(df['brand'].fillna('Unknown'))

features = ['Price', 'RAM_GB', 'Screen_Inches', 'Brand_Encoded']
X = df[features].fillna(0)

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

print("Running Isolation Forest...")
iso = IsolationForest(contamination=0.05, random_state=42, n_jobs=-1)
df['Anomaly'] = iso.fit_predict(X_scaled)
df['Anomaly_Score'] = iso.decision_function(X_scaled)

# Calculate expected price
avg_by_ram = df.groupby('RAM_GB')['Price'].mean()
df['Expected_Price'] = df['RAM_GB'].map(avg_by_ram).fillna(df['Price'].mean())
df['Price_Diff'] = df['Price'] - df['Expected_Price']
df['Price_Diff_Pct'] = (df['Price_Diff'] / df['Expected_Price']) * 100

anomalies = df[df['Anomaly'] == -1].copy()
normal = df[df['Anomaly'] == 1]
anomalies['Type'] = anomalies['Price_Diff'].apply(lambda x: 'Overpriced' if x > 0 else 'Undervalued')

print(f"Found {len(anomalies)} anomalies")

# Create visualization
fig, axes = plt.subplots(2, 2, figsize=(16, 14))
fig.patch.set_facecolor('#0d1117')
fig.suptitle('Value Anomaly Detection (Isolation Forest)', fontsize=22, fontweight='bold', color='white', y=0.98)

# Plot 1: Price vs RAM with anomalies
ax1 = axes[0, 0]
ax1.set_facecolor('#0d1117')
ax1.scatter(normal['RAM_GB'], normal['Price'], c='#4ecdc4', s=20, alpha=0.4, label='Normal')
ax1.scatter(anomalies['RAM_GB'], anomalies['Price'], c='#ff6b6b', s=50, alpha=0.8, marker='x', label='Anomaly')
ax1.set_xlabel('RAM (GB)', color='white')
ax1.set_ylabel('Price ($)', color='white')
ax1.set_title('Price vs RAM (Anomalies Highlighted)', color='white', fontsize=14, fontweight='bold')
ax1.legend(facecolor='#161b22', labelcolor='white')
ax1.tick_params(colors='white')
for spine in ax1.spines.values(): spine.set_color('#30363d')

# Plot 2: Anomaly score distribution
ax2 = axes[0, 1]
ax2.set_facecolor('#0d1117')
ax2.hist(normal['Anomaly_Score'], bins=30, alpha=0.7, color='#4ecdc4', label='Normal', density=True)
ax2.hist(anomalies['Anomaly_Score'], bins=20, alpha=0.7, color='#ff6b6b', label='Anomaly', density=True)
ax2.set_xlabel('Anomaly Score', color='white')
ax2.set_ylabel('Density', color='white')
ax2.set_title('Anomaly Score Distribution', color='white', fontsize=14, fontweight='bold')
ax2.legend(facecolor='#161b22', labelcolor='white')
ax2.tick_params(colors='white')
for spine in ax2.spines.values(): spine.set_color('#30363d')

# Plot 3: Expected vs Actual
ax3 = axes[1, 0]
ax3.set_facecolor('#0d1117')
sample = df.sample(min(2000, len(df)), random_state=42)
scatter = ax3.scatter(sample['Expected_Price'], sample['Price'], 
                      c=sample['Anomaly_Score'], cmap='RdYlGn', s=15, alpha=0.5)
ax3.plot([0, sample['Expected_Price'].max()], [0, sample['Expected_Price'].max()], 'w--', alpha=0.5)
ax3.set_xlabel('Expected Price ($)', color='white')
ax3.set_ylabel('Actual Price ($)', color='white')
ax3.set_title('Expected vs Actual Price', color='white', fontsize=14, fontweight='bold')
ax3.tick_params(colors='white')
for spine in ax3.spines.values(): spine.set_color('#30363d')
cbar = plt.colorbar(scatter, ax=ax3, shrink=0.8)
cbar.set_label('Score', color='white')
cbar.ax.tick_params(colors='white')

# Plot 4: Summary
ax4 = axes[1, 1]
ax4.set_facecolor('#161b22')
ax4.set_xticks([])
ax4.set_yticks([])
for spine in ax4.spines.values(): spine.set_color('#30363d')

n_over = (anomalies['Type'] == 'Overpriced').sum()
n_under = (anomalies['Type'] == 'Undervalued').sum()

ax4.text(0.5, 0.9, 'Anomaly Detection Results', fontsize=16, fontweight='bold', ha='center', color='white', transform=ax4.transAxes)
summary = [
    ('Algorithm:', 'Isolation Forest', '#d4a72c'),
    ('Total Anomalies:', f'{len(anomalies)}', '#ff6b6b'),
    ('Overpriced:', f'{n_over}', '#ff6b6b'),
    ('Undervalued:', f'{n_under}', '#56d364'),
    ('Normal:', f'{len(normal):,}', '#4ecdc4'),
]
for i, (label, value, color) in enumerate(summary):
    ax4.text(0.1, 0.75 - i*0.12, label, fontsize=12, color='#8b949e', transform=ax4.transAxes)
    ax4.text(0.5, 0.75 - i*0.12, value, fontsize=12, color=color, fontweight='bold', transform=ax4.transAxes)

plt.tight_layout()
plt.subplots_adjust(top=0.92)
plt.savefig(output_path, dpi=150, facecolor='#0d1117', bbox_inches='tight')
plt.close()

print(f"Saved: {output_path}")
