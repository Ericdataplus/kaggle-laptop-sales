import kagglehub
import pandas as pd
import os

# Download/locate the dataset
path = kagglehub.dataset_download('kamali2727/laptop-sales-by-amazon')
files = [f for f in os.listdir(path) if f.endswith('.csv')]
print("CSV files:", files)

# Load the data
df = pd.read_csv(os.path.join(path, files[0]))

# Also copy CSV to local folder for the dashboard
df.to_csv('laptops.csv', index=False)
print("\n✅ Copied data to laptops.csv")

print("\n" + "="*60)
print("LAPTOP SALES DATASET - EXPLORATION")
print("="*60)

print(f"\n📊 Dataset Size: {len(df):,} laptops")
print(f"📋 Columns: {len(df.columns)}")

print("\n🏷️ COLUMNS:")
for col in df.columns:
    print(f"  • {col} ({df[col].dtype})")

print("\n📝 SAMPLE DATA (first 3 rows):")
print(df.head(3).to_string())

print("\n📈 NUMERIC STATS:")
print(df.describe().to_string())

print("\n🔢 UNIQUE VALUES PER COLUMN:")
for col in df.columns:
    unique = df[col].nunique()
    sample = df[col].dropna().iloc[0] if len(df[col].dropna()) > 0 else 'N/A'
    print(f"  • {col}: {unique} unique (example: {sample})")

# Check for brands if there's a brand column
brand_cols = [c for c in df.columns if 'brand' in c.lower()]
if brand_cols:
    print(f"\n🏢 TOP BRANDS:")
    print(df[brand_cols[0]].value_counts().head(10).to_string())
