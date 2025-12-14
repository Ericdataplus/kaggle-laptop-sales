"""
10 - Summary Dashboard
Creates a comprehensive summary of all laptop data insights
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# Setup paths
script_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(script_dir)
data_path = os.path.join(project_dir, 'laptops.csv')
output_path = os.path.join(project_dir, 'graphs', '10_summary_dashboard.png')

# Load data
df = pd.read_csv(data_path)

# Clean data
df['price_clean'] = df['Price'].str.replace('$', '', regex=False).str.replace(',', '', regex=False).str.strip()
df['price_clean'] = pd.to_numeric(df['price_clean'], errors='coerce')
df['ram_gb'] = df['ram'].str.extract(r'(\d+)').astype(float)
df['brand_clean'] = df['brand'].str.upper().str.strip()
df['total_sales_clean'] = pd.to_numeric(df['Total Sales'], errors='coerce')

# Filter valid prices for stats
df_valid = df[(df['price_clean'] >= 50) & (df['price_clean'] <= 10000)]

# Create figure
fig = plt.figure(figsize=(20, 12))
fig.patch.set_facecolor('#1a1a2e')

# Title
fig.suptitle('💻 Amazon Laptop Sales - Dashboard', fontsize=28, fontweight='bold', 
             color='white', y=0.98)

# Create grid
gs = fig.add_gridspec(3, 4, hspace=0.35, wspace=0.3, 
                      left=0.05, right=0.95, top=0.90, bottom=0.05)

# ===== ROW 1: Key Stats =====
# Stat boxes
stats = [
    ('Total Laptops', f'{len(df):,}', '📦'),
    ('Brands', f'{df["brand"].nunique()}', '🏢'),
    ('Avg Price', f'${df_valid["price_clean"].mean():,.0f}', '💰'),
    ('Total Revenue', f'${df["total_sales_clean"].sum()/1e6:,.1f}M', '📈'),
]

for i, (label, value, emoji) in enumerate(stats):
    ax = fig.add_subplot(gs[0, i])
    ax.set_facecolor('#2a2a4e')
    ax.text(0.5, 0.65, emoji, fontsize=40, ha='center', va='center', transform=ax.transAxes)
    ax.text(0.5, 0.35, value, fontsize=24, fontweight='bold', ha='center', va='center', 
            transform=ax.transAxes, color='#00d4ff')
    ax.text(0.5, 0.12, label, fontsize=12, ha='center', va='center', 
            transform=ax.transAxes, color='#888')
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_color('#444')
        spine.set_linewidth(2)

# ===== ROW 2: Charts =====
# Brand distribution pie
ax1 = fig.add_subplot(gs[1, 0:2])
ax1.set_facecolor('#1a1a2e')

brand_counts = df['brand_clean'].value_counts().head(6)
colors = ['#00d4ff', '#00b4d8', '#0096c7', '#0077b6', '#023e8a', '#7b2cbf']
wedges, texts, autotexts = ax1.pie(brand_counts.values, labels=brand_counts.index, 
                                    autopct='%1.1f%%', colors=colors,
                                    textprops={'color': 'white', 'fontsize': 10})
for autotext in autotexts:
    autotext.set_fontsize(9)
    autotext.set_fontweight('bold')
ax1.set_title('Top 6 Brands', color='white', fontsize=14, fontweight='bold')

# Price distribution
ax2 = fig.add_subplot(gs[1, 2:4])
ax2.set_facecolor('#1a1a2e')

n, bins, patches = ax2.hist(df_valid['price_clean'], bins=30, color='#00d4ff', 
                            edgecolor='#1a1a2e', alpha=0.8)
for i, patch in enumerate(patches):
    patch.set_facecolor(plt.cm.cool(i / len(patches)))
    
ax2.axvline(df_valid['price_clean'].median(), color='#ff6b6b', linestyle='--', linewidth=2)
ax2.set_xlabel('Price ($)', color='white', fontsize=11)
ax2.set_ylabel('Count', color='white', fontsize=11)
ax2.set_title(f'Price Distribution (Median: ${df_valid["price_clean"].median():,.0f})', 
              color='white', fontsize=14, fontweight='bold')
ax2.tick_params(colors='white')
for spine in ax2.spines.values():
    spine.set_color('#444')

# ===== ROW 3: More Charts =====
# RAM distribution
ax3 = fig.add_subplot(gs[2, 0:2])
ax3.set_facecolor('#1a1a2e')

ram_counts = df['ram_gb'].value_counts().sort_index()
common_ram = [4, 8, 16, 32, 64]
ram_counts = ram_counts[ram_counts.index.isin(common_ram)]

bars = ax3.bar([f'{int(r)}GB' for r in ram_counts.index], ram_counts.values, 
               color=plt.cm.viridis(np.linspace(0.2, 0.8, len(ram_counts))))
ax3.set_xlabel('RAM', color='white', fontsize=11)
ax3.set_ylabel('Count', color='white', fontsize=11)
ax3.set_title('RAM Distribution', color='white', fontsize=14, fontweight='bold')
ax3.tick_params(colors='white')
for spine in ax3.spines.values():
    spine.set_color('#444')

# Top brands by revenue
ax4 = fig.add_subplot(gs[2, 2:4])
ax4.set_facecolor('#1a1a2e')

brand_revenue = df.groupby('brand_clean')['total_sales_clean'].sum().sort_values(ascending=True).tail(6)
colors2 = plt.cm.plasma(np.linspace(0.2, 0.8, len(brand_revenue)))
ax4.barh(range(len(brand_revenue)), brand_revenue.values / 1000, color=colors2)
ax4.set_yticks(range(len(brand_revenue)))
ax4.set_yticklabels(brand_revenue.index, color='white', fontsize=10)
ax4.set_xlabel('Revenue ($K)', color='white', fontsize=11)
ax4.set_title('Top Brands by Revenue', color='white', fontsize=14, fontweight='bold')
ax4.tick_params(colors='white')
for spine in ax4.spines.values():
    spine.set_color('#444')

plt.savefig(output_path, dpi=150, facecolor='#1a1a2e', edgecolor='none', bbox_inches='tight')
plt.close()

print(f"✅ Saved: {output_path}")
print(f"   Dashboard generated with {len(df):,} laptops")
