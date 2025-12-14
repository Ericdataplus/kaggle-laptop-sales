"""
08 - Rating Analysis
Analyzes customer ratings distribution and ratings by brand
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# Setup paths
script_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(script_dir)
data_path = os.path.join(project_dir, 'laptops.csv')
output_path = os.path.join(project_dir, 'graphs', '08_rating_analysis.png')

# Load data
df = pd.read_csv(data_path)

# Filter valid ratings (1-5)
df_rated = df[(df['rating'] >= 1) & (df['rating'] <= 5)].copy()

# Create figure
fig, axes = plt.subplots(1, 2, figsize=(16, 8))
fig.patch.set_facecolor('#1a1a2e')

# ----- Plot 1: Rating Distribution -----
ax1 = axes[0]
ax1.set_facecolor('#1a1a2e')

# Histogram of ratings
n, bins, patches = ax1.hist(df_rated['rating'], bins=20, color='#00d4ff', 
                            edgecolor='#1a1a2e', alpha=0.8)

# Color gradient
for i, patch in enumerate(patches):
    patch.set_facecolor(plt.cm.RdYlGn(bins[i] / 5))

# Add mean and median lines
mean_rating = df_rated['rating'].mean()
median_rating = df_rated['rating'].median()

ax1.axvline(mean_rating, color='#ffd93d', linestyle='--', linewidth=2, 
            label=f'Mean: {mean_rating:.2f}')
ax1.axvline(median_rating, color='#ff6b6b', linestyle='--', linewidth=2, 
            label=f'Median: {median_rating:.2f}')

ax1.set_xlabel('Rating', color='white', fontsize=12)
ax1.set_ylabel('Number of Laptops', color='white', fontsize=12)
ax1.set_title('⭐ Rating Distribution', color='white', fontsize=16, fontweight='bold')
ax1.legend(loc='upper left', facecolor='#2a2a4e', labelcolor='white')
ax1.tick_params(colors='white')
for spine in ax1.spines.values():
    spine.set_color('#444')

# ----- Plot 2: Average Rating by Brand -----
ax2 = axes[1]
ax2.set_facecolor('#1a1a2e')

# Get top brands and their average ratings
df_rated['brand_clean'] = df_rated['brand'].str.upper().str.strip()
brand_ratings = df_rated.groupby('brand_clean').agg({
    'rating': ['mean', 'count']
}).droplevel(0, axis=1)
brand_ratings.columns = ['avg_rating', 'count']

# Filter brands with at least 20 listings
brand_ratings = brand_ratings[brand_ratings['count'] >= 20]
brand_ratings = brand_ratings.sort_values('avg_rating', ascending=True).tail(10)

# Color based on rating
colors = [plt.cm.RdYlGn(r/5) for r in brand_ratings['avg_rating']]
bars = ax2.barh(range(len(brand_ratings)), brand_ratings['avg_rating'], color=colors)

# Add value labels
for i, (bar, row) in enumerate(zip(bars, brand_ratings.itertuples())):
    ax2.text(bar.get_width() + 0.05, bar.get_y() + bar.get_height()/2, 
             f'{row.avg_rating:.2f} ⭐ (n={row.count})',
             va='center', ha='left', color='white', fontsize=10)

ax2.set_yticks(range(len(brand_ratings)))
ax2.set_yticklabels(brand_ratings.index, color='white', fontsize=11)
ax2.set_xlabel('Average Rating', color='white', fontsize=12)
ax2.set_xlim(0, 5.5)
ax2.set_title('🏅 Top 10 Brands by Rating (min 20 listings)', color='white', fontsize=16, fontweight='bold')
ax2.tick_params(colors='white')
for spine in ax2.spines.values():
    spine.set_color('#444')
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig(output_path, dpi=150, facecolor='#1a1a2e', edgecolor='none', bbox_inches='tight')
plt.close()

print(f"✅ Saved: {output_path}")
print(f"   Average rating: {mean_rating:.2f} ⭐")
print(f"   Top rated brand: {brand_ratings.index[-1]} ({brand_ratings['avg_rating'].iloc[-1]:.2f})")
