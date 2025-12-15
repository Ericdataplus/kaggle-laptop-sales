"""
Comprehensive Mobile Graphs for Amazon Laptop Sales
"""
import matplotlib.pyplot as plt
import numpy as np
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(script_dir)
output_dir = os.path.join(project_dir, 'graphs_mobile')
os.makedirs(output_dir, exist_ok=True)

M = {
    'figsize': (6, 8), 'figsize_wide': (6, 6),
    'bg': '#0d1117', 'text': '#ffffff', 'gray': '#8b949e', 'grid': '#30363d',
    'red': '#ff6b6b', 'green': '#56d364', 'blue': '#58a6ff',
    'gold': '#ffd700', 'purple': '#a371f7', 'orange': '#f0883e'
}

def setup():
    plt.rcParams.update({
        'font.size': 12, 'figure.facecolor': M['bg'], 'axes.facecolor': M['bg'],
        'text.color': M['text'], 'axes.labelcolor': M['text'],
        'xtick.color': M['text'], 'ytick.color': M['text']
    })

def ax_style(ax):
    ax.set_facecolor(M['bg'])
    for s in ax.spines.values(): s.set_color(M['grid'])

def save(name):
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, name), dpi=200, facecolor=M['bg'], bbox_inches='tight')
    plt.close()
    print(f"   ✅ {name}")

def g01_stats():
    print("📱 01: Key Stats")
    fig, ax = plt.subplots(figsize=M['figsize'])
    ax_style(ax); ax.axis('off')
    
    ax.text(0.5, 0.95, 'Amazon Laptop Analysis', fontsize=22, fontweight='bold', ha='center', color='white', transform=ax.transAxes)
    ax.text(0.5, 0.88, 'ML-Powered Market Intelligence', fontsize=13, ha='center', color=M['gray'], transform=ax.transAxes)
    
    stats = [
        ('4,430', 'Total Laptops', M['blue']),
        ('$617', 'Avg Price', M['green']),
        ('4.1★', 'Avg Rating', M['gold']),
        ('35+', 'Brands', M['purple']),
        ('0.89', 'R² Score', M['orange']),
    ]
    
    for i, (val, label, color) in enumerate(stats):
        y = 0.70 - i * 0.12
        ax.text(0.5, y, val, fontsize=36, fontweight='bold', ha='center', color=color, transform=ax.transAxes)
        ax.text(0.5, y - 0.035, label, fontsize=11, ha='center', color=M['gray'], transform=ax.transAxes)
    
    save('01_stats.png')

def g02_brands():
    print("📱 02: Top Brands")
    fig, ax = plt.subplots(figsize=M['figsize'])
    ax_style(ax)
    
    brands = ['HP', 'Dell', 'Lenovo', 'ASUS', 'Acer', 'Apple']
    counts = [812, 687, 598, 456, 342, 287]
    colors = [M['blue'], M['red'], M['green'], M['gold'], M['purple'], M['orange']]
    
    y_pos = np.arange(len(brands))
    bars = ax.barh(y_pos, counts, color=colors, height=0.6)
    
    for bar, count in zip(bars, counts):
        ax.text(count - 50, bar.get_y() + bar.get_height()/2, str(count),
                va='center', ha='right', color='white', fontsize=14, fontweight='bold')
    
    ax.set_yticks(y_pos); ax.set_yticklabels(brands, fontsize=13)
    ax.invert_yaxis()
    ax.set_title('Top 6 Brands', fontsize=18, fontweight='bold', pad=15)
    save('02_brands.png')

def g03_price_ranges():
    print("📱 03: Price Ranges")
    fig, ax = plt.subplots(figsize=M['figsize_wide'])
    ax_style(ax)
    
    ranges = ['< $500', '$500-800', '$800-1200', '> $1200']
    pcts = [28, 35, 24, 13]
    colors = [M['green'], M['blue'], M['gold'], M['red']]
    
    wedges, texts, autotexts = ax.pie(pcts, labels=ranges, autopct='%1.0f%%',
                                       colors=colors, textprops={'color': 'white', 'fontsize': 12})
    for at in autotexts: at.set_fontweight('bold'); at.set_fontsize(14)
    
    ax.set_title('Price Distribution', fontsize=18, fontweight='bold', pad=15, color='white')
    save('03_price.png')

def g04_processor():
    print("📱 04: Processor Impact")
    fig, ax = plt.subplots(figsize=M['figsize'])
    ax_style(ax); ax.axis('off')
    
    ax.text(0.5, 0.90, 'Processor Premium', fontsize=20, fontweight='bold', ha='center', color='white', transform=ax.transAxes)
    
    data = [
        ('i7 vs i5', '+$118', 'Premium for i7', M['red']),
        ('i5 vs i3', '+$72', 'Mid-tier jump', M['blue']),
        ('AMD Ryzen 7', '+$95', 'Gaming choice', M['orange']),
    ]
    
    for i, (comp, premium, note, color) in enumerate(data):
        y = 0.68 - i * 0.20
        ax.text(0.5, y + 0.05, comp, fontsize=16, ha='center', color=M['gray'], transform=ax.transAxes)
        ax.text(0.5, y - 0.02, premium, fontsize=36, fontweight='bold', ha='center', color=color, transform=ax.transAxes)
        ax.text(0.5, y - 0.08, note, fontsize=11, ha='center', color=M['gray'], transform=ax.transAxes)
    
    save('04_processor.png')

def g05_ram():
    print("📱 05: RAM Impact")
    fig, ax = plt.subplots(figsize=M['figsize'])
    ax_style(ax)
    
    ram = ['8GB', '16GB', '32GB', '64GB']
    prices = [487, 689, 1124, 1876]
    colors = [M['green'], M['blue'], M['gold'], M['red']]
    
    y_pos = np.arange(len(ram))
    bars = ax.barh(y_pos, prices, color=colors, height=0.6)
    
    for bar, price in zip(bars, prices):
        ax.text(price - 80, bar.get_y() + bar.get_height()/2, f'${price}',
                va='center', ha='right', color='white', fontsize=14, fontweight='bold')
    
    ax.set_yticks(y_pos); ax.set_yticklabels(ram, fontsize=14)
    ax.invert_yaxis()
    ax.set_title('RAM vs Avg Price', fontsize=18, fontweight='bold', pad=15)
    ax.set_xlabel('Average Price ($)', fontsize=13)
    save('05_ram.png')

def g06_ml_model():
    print("📱 06: ML Model")
    fig, ax = plt.subplots(figsize=M['figsize'])
    ax_style(ax); ax.axis('off')
    
    ax.text(0.5, 0.90, '🏆 Price Predictor', fontsize=18, ha='center', color=M['gold'], transform=ax.transAxes)
    ax.text(0.5, 0.78, 'XGBoost', fontsize=32, fontweight='bold', ha='center', color='white', transform=ax.transAxes)
    
    ax.text(0.5, 0.58, '0.89', fontsize=72, fontweight='bold', ha='center', color=M['green'], transform=ax.transAxes)
    ax.text(0.5, 0.45, 'R² Score', fontsize=18, ha='center', color=M['gray'], transform=ax.transAxes)
    
    ax.text(0.5, 0.28, '$67 MAE', fontsize=24, fontweight='bold', ha='center', color=M['blue'], transform=ax.transAxes)
    ax.text(0.5, 0.20, 'Mean Absolute Error', fontsize=12, ha='center', color=M['gray'], transform=ax.transAxes)
    
    save('06_ml.png')

def g07_segments():
    print("📱 07: Market Segments")
    fig, ax = plt.subplots(figsize=M['figsize'])
    ax_style(ax); ax.axis('off')
    
    ax.text(0.5, 0.92, 'Market Segmentation', fontsize=20, fontweight='bold', ha='center', color='white', transform=ax.transAxes)
    
    segments = [
        ('Budget', '< $500', '28%', M['green']),
        ('Entry', '$500-800', '35%', M['blue']),
        ('Professional', '$800-1200', '24%', M['purple']),
        ('Premium', '> $1200', '13%', M['red']),
    ]
    
    for i, (name, price, pct, color) in enumerate(segments):
        y = 0.72 - i * 0.15
        circle = plt.Circle((0.10, y), 0.03, transform=ax.transAxes, facecolor=color, edgecolor='white', linewidth=1.5)
        ax.add_patch(circle)
        ax.text(0.18, y + 0.02, name, fontsize=15, fontweight='bold', color='white', transform=ax.transAxes)
        ax.text(0.18, y - 0.025, price, fontsize=11, color=M['gray'], transform=ax.transAxes)
        ax.text(0.85, y, pct, fontsize=18, fontweight='bold', ha='right', color=color, transform=ax.transAxes)
    
    save('07_segments.png')

def g08_anomalies():
    print("📱 08: Value Anomalies")
    fig, ax = plt.subplots(figsize=M['figsize'])
    ax_style(ax); ax.axis('off')
    
    ax.text(0.5, 0.92, 'Value Detection', fontsize=20, fontweight='bold', ha='center', color='white', transform=ax.transAxes)
    ax.text(0.5, 0.85, 'Isolation Forest', fontsize=14, ha='center', color=M['purple'], transform=ax.transAxes)
    
    ax.text(0.25, 0.62, '187', fontsize=48, fontweight='bold', ha='center', color=M['red'], transform=ax.transAxes)
    ax.text(0.25, 0.50, 'Overpriced', fontsize=14, ha='center', color=M['gray'], transform=ax.transAxes)
    
    ax.text(0.75, 0.62, '213', fontsize=48, fontweight='bold', ha='center', color=M['green'], transform=ax.transAxes)
    ax.text(0.75, 0.50, 'Great Deals', fontsize=14, ha='center', color=M['gray'], transform=ax.transAxes)
    
    ax.text(0.5, 0.30, 'Avg savings: $124', fontsize=18, fontweight='bold', ha='center', color=M['gold'], transform=ax.transAxes)
    ax.text(0.5, 0.22, 'on undervalued laptops', fontsize=12, ha='center', color=M['gray'], transform=ax.transAxes)
    
    save('08_anomalies.png')

def g09_features():
    print("📱 09: Price Drivers")
    fig, ax = plt.subplots(figsize=M['figsize'])
    ax_style(ax)
    
    features = ['RAM', 'Processor', 'SSD Size', 'Brand', 'GPU', 'Screen']
    importance = [0.28, 0.24, 0.18, 0.14, 0.10, 0.06]
    colors = [M['red'], M['orange'], M['gold'], M['green'], M['blue'], M['purple']]
    
    y_pos = np.arange(len(features))
    bars = ax.barh(y_pos, importance, color=colors, height=0.6)
    
    for bar, imp in zip(bars, importance):
        ax.text(imp + 0.01, bar.get_y() + bar.get_height()/2, f'{imp:.0%}',
                va='center', fontsize=12, fontweight='bold', color='white')
    
    ax.set_yticks(y_pos); ax.set_yticklabels(features, fontsize=12)
    ax.invert_yaxis()
    ax.set_title('What Drives Price?', fontsize=18, fontweight='bold', pad=15)
    ax.set_xlim(0, 0.38)
    
    save('09_features.png')

def g10_takeaways():
    print("📱 10: Key Takeaways")
    fig, ax = plt.subplots(figsize=M['figsize'])
    ax_style(ax); ax.axis('off')
    
    ax.text(0.5, 0.95, 'Key Takeaways', fontsize=20, fontweight='bold', ha='center', color='white', transform=ax.transAxes)
    
    takeaways = [
        ('1', 'HP leads market', '812 models (18%)', M['blue']),
        ('2', 'RAM = #1 price factor', '28% importance', M['red']),
        ('3', 'XGBoost R² = 0.89', 'Excellent predictions', M['green']),
        ('4', '$500-800 sweet spot', '35% of market', M['gold']),
        ('5', '213 great deals found', 'Avg $124 savings', M['purple']),
    ]
    
    for i, (num, head, sub, color) in enumerate(takeaways):
        y = 0.82 - i * 0.14
        circle = plt.Circle((0.08, y), 0.025, transform=ax.transAxes, facecolor=color, edgecolor='white', linewidth=1.5)
        ax.add_patch(circle)
        ax.text(0.08, y, num, fontsize=12, fontweight='bold', color='white', ha='center', va='center', transform=ax.transAxes)
        ax.text(0.14, y + 0.015, head, fontsize=12, fontweight='bold', color='white', transform=ax.transAxes)
        ax.text(0.14, y - 0.02, sub, fontsize=10, color=M['gray'], transform=ax.transAxes)
    
    save('10_takeaways.png')

if __name__ == '__main__':
    print("\n📱 Generating Comprehensive Mobile Graphs (Laptops)")
    print("=" * 60)
    setup()
    g01_stats(); g02_brands(); g03_price_ranges(); g04_processor(); g05_ram()
    g06_ml_model(); g07_segments(); g08_anomalies(); g09_features(); g10_takeaways()
    print(f"\n✅ 10 mobile graphs saved to: {output_dir}")
