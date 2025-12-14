"""
11 - Price Prediction Model (ML)
Predicts laptop prices using Random Forest
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import os
import warnings
warnings.filterwarnings('ignore')

# Setup paths
script_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(script_dir)
data_path = os.path.join(project_dir, 'laptops.csv')
output_path = os.path.join(project_dir, 'graphs', '11_price_prediction.png')

print("Loading data...")
df = pd.read_csv(data_path)

# Clean price column
df['Price'] = pd.to_numeric(df['Price'].astype(str).str.replace('$', '').str.replace(',', '').str.strip(), errors='coerce')

# Clean data
df = df.dropna(subset=['Price'])
df = df[df['Price'] > 0]

# Feature engineering
df['RAM_GB'] = pd.to_numeric(df['ram'].astype(str).str.extract(r'(\d+)')[0], errors='coerce').fillna(8)
df['Screen_Inches'] = pd.to_numeric(df['screen_size'].astype(str).str.extract(r'([\d.]+)')[0], errors='coerce').fillna(15.6)

# Encode brand
le_brand = LabelEncoder()
df['Brand_Encoded'] = le_brand.fit_transform(df['brand'].fillna('Unknown'))

# Encode processor type
df['Processor_Type'] = df['cpu'].fillna('Unknown').apply(lambda x: 
    'Intel i7' if 'i7' in str(x) else 
    'Intel i5' if 'i5' in str(x) else
    'Intel i3' if 'i3' in str(x) else
    'AMD Ryzen' if 'Ryzen' in str(x) else 'Other')
le_proc = LabelEncoder()
df['Processor_Encoded'] = le_proc.fit_transform(df['Processor_Type'])

# Features
features = ['Brand_Encoded', 'RAM_GB', 'Screen_Inches', 'Processor_Encoded']
X = df[features].fillna(0)
y = df['Price']


# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("Training models...")
models = {
    'Random Forest': RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42, n_jobs=-1),
    'Gradient Boosting': GradientBoostingRegressor(n_estimators=100, max_depth=5, random_state=42),
}

results = {}
for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    results[name] = {
        'mae': mean_absolute_error(y_test, y_pred),
        'r2': r2_score(y_test, y_pred),
        'predictions': y_pred,
        'model': model
    }

best_name = min(results, key=lambda x: results[x]['mae'])
best = results[best_name]

# Feature importance
if hasattr(best['model'], 'feature_importances_'):
    importance = pd.DataFrame({
        'feature': ['Brand', 'RAM', 'Screen Size', 'Processor'],
        'importance': best['model'].feature_importances_
    }).sort_values('importance', ascending=False)

# Create visualization
fig, axes = plt.subplots(2, 2, figsize=(16, 14))
fig.patch.set_facecolor('#0d1117')
fig.suptitle('Laptop Price Prediction Model', fontsize=22, fontweight='bold', color='white', y=0.98)

# Plot 1: Model comparison
ax1 = axes[0, 0]
ax1.set_facecolor('#0d1117')
names = list(results.keys())
maes = [results[n]['mae'] for n in names]
r2s = [results[n]['r2'] * 100 for n in names]
x = np.arange(len(names))
width = 0.35
colors = ['#4ecdc4', '#ff6b6b']

bars1 = ax1.bar(x - width/2, maes, width, color=colors[0], label='MAE ($)')
ax1_twin = ax1.twinx()
bars2 = ax1_twin.bar(x + width/2, r2s, width, color=colors[1], label='R2 (%)')

ax1.set_xticks(x)
ax1.set_xticklabels(names, color='white')
ax1.set_ylabel('MAE ($)', color='white')
ax1_twin.set_ylabel('R2 (%)', color='white')
ax1.set_title('Model Comparison', color='white', fontsize=14, fontweight='bold')
ax1.tick_params(colors='white')
ax1_twin.tick_params(colors='white')
for spine in ax1.spines.values(): spine.set_color('#30363d')
for spine in ax1_twin.spines.values(): spine.set_color('#30363d')

# Plot 2: Feature importance
ax2 = axes[0, 1]
ax2.set_facecolor('#0d1117')
colors = plt.cm.viridis(np.linspace(0.9, 0.3, len(importance)))
bars = ax2.barh(importance['feature'], importance['importance'] * 100, color=colors)
ax2.set_xlabel('Importance (%)', color='white')
ax2.set_title('Feature Importance', color='white', fontsize=14, fontweight='bold')
ax2.tick_params(colors='white')
for spine in ax2.spines.values(): spine.set_color('#30363d')

# Plot 3: Predicted vs Actual
ax3 = axes[1, 0]
ax3.set_facecolor('#0d1117')
ax3.scatter(y_test, best['predictions'], alpha=0.5, s=15, c='#4ecdc4')
ax3.plot([0, y_test.max()], [0, y_test.max()], 'r--', linewidth=2)
ax3.set_xlabel('Actual Price ($)', color='white')
ax3.set_ylabel('Predicted Price ($)', color='white')
ax3.set_title('Predicted vs Actual', color='white', fontsize=14, fontweight='bold')
ax3.tick_params(colors='white')
for spine in ax3.spines.values(): spine.set_color('#30363d')

# Plot 4: Summary
ax4 = axes[1, 1]
ax4.set_facecolor('#161b22')
ax4.set_xticks([])
ax4.set_yticks([])
for spine in ax4.spines.values(): spine.set_color('#30363d')

ax4.text(0.5, 0.9, 'Model Results', fontsize=16, fontweight='bold', ha='center', color='white', transform=ax4.transAxes)
summary = [
    ('Best Model:', best_name, '#d4a72c'),
    ('MAE:', f'${best["mae"]:.0f}', '#ff6b6b'),
    ('R2 Score:', f'{best["r2"]*100:.1f}%', '#4ecdc4'),
    ('Training Samples:', f'{len(X_train):,}', '#58a6ff'),
    ('Top Predictor:', importance.iloc[0]['feature'], '#56d364'),
]
for i, (label, value, color) in enumerate(summary):
    ax4.text(0.1, 0.75 - i*0.12, label, fontsize=12, color='#8b949e', transform=ax4.transAxes)
    ax4.text(0.5, 0.75 - i*0.12, value, fontsize=12, color=color, fontweight='bold', transform=ax4.transAxes)

plt.tight_layout()
plt.subplots_adjust(top=0.92)
plt.savefig(output_path, dpi=150, facecolor='#0d1117', bbox_inches='tight')
plt.close()

print(f"Saved: {output_path}")
print(f"Best: {best_name} - MAE: ${best['mae']:.0f}, R2: {best['r2']*100:.1f}%")
