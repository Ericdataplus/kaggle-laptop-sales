"""
DEEP ANALYSIS - Advanced Insights for Amazon Laptop Sales
This creates impressive analyses that go beyond typical dashboards
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import os

# Setup paths
script_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(script_dir)
data_path = os.path.join(project_dir, 'laptops.csv')

# Load and clean data
df = pd.read_csv(data_path)

# ===== DATA CLEANING =====
# Price
df['price'] = df['Price'].str.replace('$', '', regex=False).str.replace(',', '', regex=False).str.strip()
df['price'] = pd.to_numeric(df['price'], errors='coerce')

# RAM (extract number)
df['ram_gb'] = df['ram'].str.extract(r'(\d+)').astype(float)

# Storage (extract number)
df['storage_gb'] = df['harddisk'].str.extract(r'(\d+)').astype(float)

# Screen size
df['screen'] = df['screen_size'].str.extract(r'([\d.]+)').astype(float)

# Brand (clean)
df['brand_clean'] = df['brand'].str.upper().str.strip()

# Graphics type
def get_graphics_type(g):
    if pd.isna(g): return 'Unknown'
    g = str(g).lower()
    if any(x in g for x in ['dedicated', 'rtx', 'gtx', 'nvidia', 'geforce', 'radeon rx']): return 'Dedicated'
    return 'Integrated'

df['gpu_type'] = df['graphics'].apply(get_graphics_type)

# CPU category
def get_cpu_tier(cpu):
    if pd.isna(cpu): return 'Unknown'
    cpu = str(cpu).lower()
    if any(x in cpu for x in ['i9', 'ryzen 9', 'm2 max', 'm2 pro']): return 'Flagship'
    if any(x in cpu for x in ['i7', 'ryzen 7', 'm2', 'm1 pro']): return 'High-End'
    if any(x in cpu for x in ['i5', 'ryzen 5', 'm1']): return 'Mid-Range'
    if any(x in cpu for x in ['i3', 'ryzen 3']): return 'Entry'
    if any(x in cpu for x in ['celeron', 'pentium', 'athlon']): return 'Budget'
    return 'Other'

df['cpu_tier'] = df['cpu'].apply(get_cpu_tier)

# Sales data
df['units_sold'] = pd.to_numeric(df['Sale Product Count'], errors='coerce')
df['revenue'] = pd.to_numeric(df['Total Sales'], errors='coerce')
df['stock'] = pd.to_numeric(df['Available Stock'], errors='coerce')

# Filter valid data
df_valid = df[(df['price'] >= 100) & (df['price'] <= 8000) & (df['rating'] >= 1)].copy()

print(f"Loaded {len(df):,} laptops, {len(df_valid):,} with valid price/rating")

# ===== ADVANCED ANALYSIS 1: VALUE SCORE =====
# Calculate a "value score" based on specs relative to price
print("\n" + "="*60)
print("🎯 VALUE ANALYSIS - Finding the Best Deals")
print("="*60)

# Normalize specs (0-1 scale)
df_valid['ram_norm'] = (df_valid['ram_gb'] - df_valid['ram_gb'].min()) / (df_valid['ram_gb'].max() - df_valid['ram_gb'].min())
df_valid['storage_norm'] = (df_valid['storage_gb'] - df_valid['storage_gb'].min()) / (df_valid['storage_gb'].max() - df_valid['storage_gb'].min())
df_valid['rating_norm'] = (df_valid['rating'] - 1) / 4  # 1-5 to 0-1
df_valid['gpu_score'] = df_valid['gpu_type'].map({'Dedicated': 1, 'Integrated': 0.3, 'Unknown': 0.2})

# CPU tier score
cpu_scores = {'Flagship': 1.0, 'High-End': 0.8, 'Mid-Range': 0.6, 'Entry': 0.4, 'Budget': 0.2, 'Other': 0.3, 'Unknown': 0.2}
df_valid['cpu_score'] = df_valid['cpu_tier'].map(cpu_scores)

# Value score = (specs + rating) / price
df_valid['spec_score'] = (
    df_valid['ram_norm'].fillna(0) * 0.25 +
    df_valid['storage_norm'].fillna(0) * 0.15 +
    df_valid['rating_norm'].fillna(0) * 0.25 +
    df_valid['gpu_score'].fillna(0) * 0.20 +
    df_valid['cpu_score'].fillna(0) * 0.15
)

# Value = spec score per $100
df_valid['value_score'] = df_valid['spec_score'] / (df_valid['price'] / 100)

# Top value laptops
print("\n🏆 TOP 10 BEST VALUE LAPTOPS (High specs, Low price, Good rating):")
top_value = df_valid.nlargest(10, 'value_score')[['brand', 'model', 'price', 'ram_gb', 'rating', 'gpu_type', 'value_score']]
for i, row in enumerate(top_value.itertuples(), 1):
    print(f"{i}. {row.brand} {row.model[:30] if pd.notna(row.model) else 'N/A'}")
    print(f"   💰 ${row.price:,.0f} | 🧠 {row.ram_gb:.0f}GB RAM | ⭐ {row.rating:.1f} | 🎮 {row.gpu_type}")
    print(f"   📊 Value Score: {row.value_score:.3f}")

# ===== ADVANCED ANALYSIS 2: MARKET SEGMENTATION =====
print("\n" + "="*60)
print("📊 MARKET SEGMENTATION")
print("="*60)

# Define segments based on price and features
def segment_laptop(row):
    price = row['price']
    gpu = row['gpu_type']
    cpu = row['cpu_tier']
    
    if gpu == 'Dedicated' and cpu in ['Flagship', 'High-End'] and price > 1500:
        return 'Gaming/Workstation'
    elif gpu == 'Dedicated' and price > 800:
        return 'Gaming Budget'
    elif cpu in ['Flagship', 'High-End'] and price > 1200:
        return 'Business Premium'
    elif price < 400:
        return 'Budget'
    elif price < 800:
        return 'Mid-Range'
    else:
        return 'Standard'

df_valid['segment'] = df_valid.apply(segment_laptop, axis=1)

segment_stats = df_valid.groupby('segment').agg({
    'price': ['mean', 'median', 'count'],
    'rating': 'mean',
    'revenue': 'sum'
}).round(2)

print("\nMarket Segments:")
for seg in df_valid['segment'].value_counts().index:
    subset = df_valid[df_valid['segment'] == seg]
    print(f"\n🔹 {seg.upper()}")
    print(f"   Count: {len(subset):,} laptops ({len(subset)/len(df_valid)*100:.1f}%)")
    print(f"   Avg Price: ${subset['price'].mean():,.0f}")
    print(f"   Avg Rating: {subset['rating'].mean():.2f} ⭐")
    print(f"   Total Revenue: ${subset['revenue'].sum():,.0f}")

# ===== ADVANCED ANALYSIS 3: PRICE ANOMALIES =====
print("\n" + "="*60)
print("🔍 PRICE ANOMALY DETECTION")
print("="*60)

# Calculate expected price based on specs using simple regression
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler

# Prepare features for price prediction
features = ['ram_gb', 'storage_gb', 'screen', 'gpu_score', 'cpu_score']
df_model = df_valid.dropna(subset=features + ['price'])

X = df_model[features].fillna(0)
y = df_model['price']

# Fit model
model = LinearRegression()
model.fit(X, y)
df_model['predicted_price'] = model.predict(X)
df_model['price_diff'] = df_model['price'] - df_model['predicted_price']
df_model['price_diff_pct'] = (df_model['price_diff'] / df_model['predicted_price']) * 100

# Overpriced (paying 50%+ more than expected)
overpriced = df_model[df_model['price_diff_pct'] > 50].nlargest(5, 'price_diff_pct')
print("\n⚠️ MOST OVERPRICED (50%+ above expected):")
for i, row in enumerate(overpriced.itertuples(), 1):
    print(f"{i}. {row.brand} - ${row.price:,.0f} (Expected: ${row.predicted_price:,.0f}, +{row.price_diff_pct:.0f}%)")

# Underpriced (paying 30%+ less than expected) - DEALS!
underpriced = df_model[df_model['price_diff_pct'] < -30].nsmallest(5, 'price_diff_pct')
print("\n🎉 BEST DEALS (30%+ below expected):")
for i, row in enumerate(underpriced.itertuples(), 1):
    print(f"{i}. {row.brand} - ${row.price:,.0f} (Expected: ${row.predicted_price:,.0f}, {row.price_diff_pct:.0f}%)")

# ===== ADVANCED ANALYSIS 4: BRAND POSITIONING =====
print("\n" + "="*60)
print("🗺️ BRAND POSITIONING ANALYSIS")
print("="*60)

brand_positioning = df_valid.groupby('brand_clean').agg({
    'price': 'median',
    'rating': 'mean',
    'revenue': 'sum',
    'brand': 'count'
}).rename(columns={'brand': 'count'})

# Filter brands with 20+ listings
brand_positioning = brand_positioning[brand_positioning['count'] >= 20]
brand_positioning = brand_positioning.sort_values('revenue', ascending=False)

print("\nBrand Positioning (Median Price vs Avg Rating):")
print("-" * 60)
for brand in brand_positioning.head(10).index:
    row = brand_positioning.loc[brand]
    price_tier = "💎 Premium" if row['price'] > 1000 else "💰 Mid" if row['price'] > 500 else "🏷️ Budget"
    rating_tier = "⭐⭐⭐" if row['rating'] > 4.3 else "⭐⭐" if row['rating'] > 4.0 else "⭐"
    print(f"{brand:12} | ${row['price']:>7,.0f} {price_tier:12} | {row['rating']:.2f} {rating_tier} | Revenue: ${row['revenue']/1000:,.0f}K")

# ===== ADVANCED ANALYSIS 5: FEATURE IMPACT ON SALES =====
print("\n" + "="*60)
print("📈 FEATURE IMPACT ON SALES SUCCESS")
print("="*60)

# Which features correlate with higher sales?
df_sales = df_valid.dropna(subset=['units_sold', 'rating'])

# Correlation analysis
correlations = {
    'RAM': df_sales['ram_gb'].corr(df_sales['units_sold']),
    'Price': df_sales['price'].corr(df_sales['units_sold']),
    'Rating': df_sales['rating'].corr(df_sales['units_sold']),
    'Screen Size': df_sales['screen'].corr(df_sales['units_sold']),
}

print("\nCorrelation with Units Sold:")
for feature, corr in sorted(correlations.items(), key=lambda x: abs(x[1]), reverse=True):
    direction = "📈" if corr > 0 else "📉"
    strength = "Strong" if abs(corr) > 0.3 else "Moderate" if abs(corr) > 0.1 else "Weak"
    print(f"  {direction} {feature}: {corr:+.3f} ({strength})")

# ===== ADVANCED ANALYSIS 6: HIDDEN GEMS =====
print("\n" + "="*60)
print("💎 HIDDEN GEMS - Underrated Laptops")
print("="*60)

# High rating, low stock, low sales but great specs
df_gems = df_valid[
    (df_valid['rating'] >= 4.5) & 
    (df_valid['units_sold'] < df_valid['units_sold'].quantile(0.3)) &
    (df_valid['price'] < df_valid['price'].median())
].nlargest(10, 'value_score')

print("\n🔮 Underrated laptops with great ratings but low sales:")
for i, row in enumerate(df_gems.itertuples(), 1):
    print(f"{i}. {row.brand} {str(row.model)[:25] if pd.notna(row.model) else 'N/A'}")
    print(f"   💰 ${row.price:,.0f} | ⭐ {row.rating:.1f} | 📦 Only {row.units_sold:.0f} sold")

# ===== SAVE INSIGHTS TO FILE =====
output_path = os.path.join(project_dir, 'deep_insights.txt')
with open(output_path, 'w', encoding='utf-8') as f:
    f.write("AMAZON LAPTOP SALES - DEEP ANALYSIS INSIGHTS\n")
    f.write("=" * 60 + "\n\n")
    
    f.write("KEY FINDINGS:\n\n")
    
    f.write("1. VALUE ANALYSIS\n")
    f.write(f"   - Best value brand: {top_value.iloc[0]['brand']}\n")
    f.write(f"   - Average value laptop costs: ${df_valid['price'].median():,.0f}\n\n")
    
    f.write("2. MARKET SEGMENTS\n")
    for seg, count in df_valid['segment'].value_counts().items():
        f.write(f"   - {seg}: {count:,} laptops ({count/len(df_valid)*100:.1f}%)\n")
    f.write("\n")
    
    f.write("3. BRAND INSIGHTS\n")
    f.write(f"   - Total brands analyzed: {df_valid['brand_clean'].nunique()}\n")
    f.write(f"   - Top revenue brand: {brand_positioning.index[0]}\n")
    f.write(f"   - Highest rated brand (20+ listings): {brand_positioning['rating'].idxmax()}\n\n")
    
    f.write("4. PRICING INSIGHTS\n")
    f.write(f"   - Median laptop price: ${df_valid['price'].median():,.0f}\n")
    f.write(f"   - Price range: ${df_valid['price'].min():,.0f} - ${df_valid['price'].max():,.0f}\n")
    f.write(f"   - Overpriced listings detected: {len(df_model[df_model['price_diff_pct'] > 50]):,}\n")
    f.write(f"   - Deal listings detected: {len(df_model[df_model['price_diff_pct'] < -30]):,}\n\n")
    
    f.write("5. SALES DRIVERS\n")
    for feature, corr in sorted(correlations.items(), key=lambda x: abs(x[1]), reverse=True):
        f.write(f"   - {feature}: {corr:+.3f} correlation with sales\n")

print(f"\n✅ Deep insights saved to: {output_path}")
