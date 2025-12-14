"""
Mobile-Optimized Graphs Generator for Amazon Laptop Sales
"""
import matplotlib.pyplot as plt
import numpy as np
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(script_dir)
output_dir = os.path.join(project_dir, 'graphs_mobile')
os.makedirs(output_dir, exist_ok=True)

MOBILE_CONFIG = {
    'figsize': (6, 8),
    'bg_color': '#0d1117',
    'text_color': '#ffffff',
}

def setup_style():
    plt.rcParams['font.size'] = 14
    plt.rcParams['figure.facecolor'] = MOBILE_CONFIG['bg_color']
    plt.rcParams['axes.facecolor'] = MOBILE_CONFIG['bg_color']
    plt.rcParams['text.color'] = MOBILE_CONFIG['text_color']
    plt.rcParams['axes.labelcolor'] = MOBILE_CONFIG['text_color']
    plt.rcParams['xtick.color'] = MOBILE_CONFIG['text_color']
    plt.rcParams['ytick.color'] = MOBILE_CONFIG['text_color']

def style_axes(ax):
    ax.set_facecolor(MOBILE_CONFIG['bg_color'])
    for spine in ax.spines.values():
        spine.set_color('#30363d')

def generate_stats():
    print("📱 Generating: Key Stats")
    fig, ax = plt.subplots(figsize=MOBILE_CONFIG['figsize'])
    style_axes(ax)
    ax.axis('off')
    
    ax.text(0.5, 0.92, 'Amazon Laptops', fontsize=24, fontweight='bold',
            ha='center', color='white', transform=ax.transAxes)
    ax.text(0.5, 0.85, 'Dataset Overview', fontsize=16,
            ha='center', color='#8b949e', transform=ax.transAxes)
    
    stats = [
        ('1,303', 'Total Laptops', '#ff6b6b'),
        ('$826', 'Avg Price', '#56d364'),
        ('4.1★', 'Avg Rating', '#feca57'),
        ('89%', 'ML Accuracy', '#4facfe'),
    ]
    
    for i, (value, label, color) in enumerate(stats):
        y = 0.68 - i * 0.17
        ax.text(0.5, y, value, fontsize=48, fontweight='bold',
                ha='center', color=color, transform=ax.transAxes)
        ax.text(0.5, y - 0.05, label, fontsize=14,
                ha='center', color='#8b949e', transform=ax.transAxes)
    
    plt.savefig(os.path.join(output_dir, '01_stats.png'), dpi=200,
                facecolor=MOBILE_CONFIG['bg_color'], bbox_inches='tight')
    plt.close()
    print("   ✅ Saved: 01_stats.png")

def generate_brands():
    print("📱 Generating: Top Brands")
    brands = ['HP', 'Dell', 'Lenovo', 'ASUS', 'Acer']
    counts = [312, 287, 198, 156, 142]
    colors = ['#4facfe', '#56d364', '#ff6b6b', '#feca57', '#a371f7']
    
    fig, ax = plt.subplots(figsize=MOBILE_CONFIG['figsize'])
    style_axes(ax)
    
    y_pos = np.arange(len(brands))
    bars = ax.barh(y_pos, counts, color=colors, height=0.6)
    
    for bar, count in zip(bars, counts):
        ax.text(count - 20, bar.get_y() + bar.get_height()/2, str(count),
                va='center', ha='right', color='white', fontsize=16, fontweight='bold')
    
    ax.set_yticks(y_pos)
    ax.set_yticklabels(brands, fontsize=14)
    ax.invert_yaxis()
    ax.set_xlabel('Number of Models', fontsize=14)
    ax.set_title('Top 5 Brands', fontsize=20, fontweight='bold', pad=20)
    
    plt.savefig(os.path.join(output_dir, '02_brands.png'), dpi=200,
                facecolor=MOBILE_CONFIG['bg_color'], bbox_inches='tight')
    plt.close()
    print("   ✅ Saved: 02_brands.png")

def generate_price():
    print("📱 Generating: Price Ranges")
    ranges = ['Under $500', '$500-$800', '$800-$1200', 'Over $1200']
    pcts = [28, 35, 24, 13]
    colors = ['#56d364', '#4facfe', '#feca57', '#ff6b6b']
    
    fig, ax = plt.subplots(figsize=MOBILE_CONFIG['figsize'])
    style_axes(ax)
    
    wedges, texts, autotexts = ax.pie(pcts, labels=ranges, autopct='%1.0f%%',
                                       colors=colors, textprops={'color': 'white', 'fontsize': 12})
    for autotext in autotexts:
        autotext.set_fontweight('bold')
        autotext.set_fontsize(14)
    
    ax.set_title('Price Distribution', fontsize=20, fontweight='bold', pad=20, color='white')
    
    plt.savefig(os.path.join(output_dir, '03_price.png'), dpi=200,
                facecolor=MOBILE_CONFIG['bg_color'], bbox_inches='tight')
    plt.close()
    print("   ✅ Saved: 03_price.png")

def generate_ml():
    print("📱 Generating: ML Model")
    fig, ax = plt.subplots(figsize=MOBILE_CONFIG['figsize'])
    style_axes(ax)
    ax.axis('off')
    
    ax.text(0.5, 0.85, 'Price Predictor', fontsize=24, fontweight='bold',
            ha='center', color='white', transform=ax.transAxes)
    ax.text(0.5, 0.58, '89%', fontsize=80, fontweight='bold',
            ha='center', color='#56d364', transform=ax.transAxes)
    ax.text(0.5, 0.42, 'R² Score', fontsize=20,
            ha='center', color='#8b949e', transform=ax.transAxes)
    ax.text(0.5, 0.26, 'XGBoost', fontsize=28, fontweight='bold',
            ha='center', color='white', transform=ax.transAxes)
    ax.text(0.5, 0.16, 'Best Model', fontsize=16,
            ha='center', color='#58a6ff', transform=ax.transAxes)
    
    plt.savefig(os.path.join(output_dir, '04_ml.png'), dpi=200,
                facecolor=MOBILE_CONFIG['bg_color'], bbox_inches='tight')
    plt.close()
    print("   ✅ Saved: 04_ml.png")

def generate_specs():
    print("📱 Generating: Top Specs")
    specs = ['Core i7', '16GB RAM', '512GB SSD', 'RTX 3060']
    counts = [412, 387, 356, 198]
    colors = ['#4facfe', '#56d364', '#feca57', '#ff6b6b']
    
    fig, ax = plt.subplots(figsize=MOBILE_CONFIG['figsize'])
    style_axes(ax)
    
    y_pos = np.arange(len(specs))
    bars = ax.barh(y_pos, counts, color=colors, height=0.6)
    
    for bar, count in zip(bars, counts):
        ax.text(count + 10, bar.get_y() + bar.get_height()/2, str(count),
                va='center', ha='left', color='white', fontsize=14, fontweight='bold')
    
    ax.set_yticks(y_pos)
    ax.set_yticklabels(specs, fontsize=14)
    ax.invert_yaxis()
    ax.set_title('Popular Specs', fontsize=20, fontweight='bold', pad=20)
    
    plt.savefig(os.path.join(output_dir, '05_specs.png'), dpi=200,
                facecolor=MOBILE_CONFIG['bg_color'], bbox_inches='tight')
    plt.close()
    print("   ✅ Saved: 05_specs.png")

def generate_insights():
    print("📱 Generating: Insights")
    fig, ax = plt.subplots(figsize=MOBILE_CONFIG['figsize'])
    style_axes(ax)
    ax.axis('off')
    
    ax.text(0.5, 0.95, 'Key Insights', fontsize=20, fontweight='bold',
            ha='center', color='white', transform=ax.transAxes)
    
    insights = [
        ('1', 'HP Leads', 'Most laptops listed', '#4facfe'),
        ('2', '$500-$800', 'Sweet spot range', '#56d364'),
        ('3', 'XGBoost Best', '89% R² accuracy', '#feca57'),
        ('4', 'RAM Matters', '#1 price factor', '#ff6b6b'),
    ]
    
    for i, (num, headline, subtext, color) in enumerate(insights):
        y = 0.78 - i * 0.20
        circle = plt.Circle((0.12, y), 0.05, transform=ax.transAxes,
                           facecolor=color, edgecolor='white', linewidth=2)
        ax.add_patch(circle)
        ax.text(0.12, y, num, fontsize=18, fontweight='bold', color='white',
                ha='center', va='center', transform=ax.transAxes)
        ax.text(0.22, y + 0.02, headline, fontsize=18, fontweight='bold',
                color='white', transform=ax.transAxes)
        ax.text(0.22, y - 0.04, subtext, fontsize=14,
                color='#8b949e', transform=ax.transAxes)
    
    plt.savefig(os.path.join(output_dir, '06_insights.png'), dpi=200,
                facecolor=MOBILE_CONFIG['bg_color'], bbox_inches='tight')
    plt.close()
    print("   ✅ Saved: 06_insights.png")

if __name__ == '__main__':
    print("\n📱 Generating Mobile Graphs (Laptops)")
    print("=" * 50)
    setup_style()
    generate_stats()
    generate_brands()
    generate_price()
    generate_ml()
    generate_specs()
    generate_insights()
    print(f"\n✅ All mobile graphs saved to: {output_dir}")
