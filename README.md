# 💻 Amazon Laptop Sales Analysis Dashboard

> 📊 **Inspired by:** [Laptop Sales by Amazon](https://www.kaggle.com/datasets/kamali2727/laptop-sales-by-amazon)
>
> Deep data analysis and visualization of 4,400+ laptop listings from Amazon, uncovering pricing trends, brand performance, and hidden value deals.

🔗 **[View Live Dashboard](https://ericdataplus.github.io/kaggle-laptop-sales/)**

![Dashboard Preview](graphs/10_summary_dashboard.png)

## 📊 Key Statistics

| Metric | Value |
|--------|-------|
| Total Laptops | 4,447 |
| Brands Analyzed | 34 |
| Median Price | $992 |
| Total Revenue | $87M+ |
| Avg Rating | 4.2 ⭐ |

## 🔍 Key Findings

1. **🎯 Best Value: Dell Leads** — Dell offers the highest specs-to-price ratio across all brands
2. **💰 The $992 Sweet Spot** — Most successful laptops cluster around this median price point
3. **🎮 Gaming Premium: +40%** — Dedicated GPUs add 40% to average laptop prices
4. **📊 Market Segmentation** — 35% Standard, 26% Mid-Range, 14% Budget, 20% Gaming, 4% Business Premium
5. **🔍 680 Hidden Deals** — ML analysis found 680 laptops priced 30%+ below expected value
6. **⭐ Price ≠ Satisfaction** — Higher prices don't correlate with better customer ratings

## 🔬 Advanced Analysis Features

This project goes **beyond basic charts** with:

- **Value Score Algorithm** — Custom metric combining RAM, CPU, GPU, rating relative to price
- **Price Anomaly Detection** — Machine learning identifies overpriced and underpriced laptops
- **Market Segmentation** — Automated categorization into Gaming, Business, Budget segments
- **Brand Positioning Map** — Strategic quadrant analysis of all brands

## 📁 Project Structure

```
kaggle-laptop-sales/
├── index.html              # Interactive Dashboard
├── graphs/                 # 13 static visualizations (PNG)
│   ├── 01_brand_distribution.png
│   ├── 02_price_analysis.png
│   ├── 03_ram_analysis.png
│   ├── 04_os_analysis.png
│   ├── 05_screen_size_analysis.png
│   ├── 06_graphics_analysis.png
│   ├── 07_top_sellers.png
│   ├── 08_rating_analysis.png
│   ├── 09a_brand_positioning.png
│   ├── 09b_spec_heatmap.png
│   ├── 09c_market_segments.png
│   ├── 09d_value_analysis.png
│   └── 10_summary_dashboard.png
├── gifs/                   # 4 animated visualizations (GIF)
│   ├── 01_brand_race.gif
│   ├── 02_price_scatter.gif
│   ├── 03_stats_counter.gif
│   └── 04_segment_pie.gif
├── scripts/                # Python analysis scripts
│   ├── 01-08_*.py         # Basic analysis
│   ├── 09_advanced_viz.py # Advanced visualizations
│   ├── deep_analysis.py   # ML-based analysis
│   ├── gif_*.py           # Animation generators
│   └── run_all*.py        # Batch runners
└── laptops.csv             # Dataset
```

## 🖼️ Visualizations

### Static Charts
- Brand Distribution
- Price Analysis (histogram + boxplot)
- RAM Distribution & Pricing
- OS Market Share
- Screen Size Trends
- Graphics Card Analysis
- Top Selling Laptops
- Rating Analysis
- Brand Positioning Map (quadrant analysis)
- Price-RAM Heatmap
- Market Segmentation
- Value Score Analysis

### Animated GIFs
- Brand Revenue Race
- Price-Rating Scatter Buildup
- Stats Counter
- Market Segment Pie

## 🛠️ Tech Stack

- **Python** - Data analysis & visualization
- **Pandas** - Data manipulation
- **Matplotlib/Seaborn** - Static visualizations
- **Scikit-learn** - Price prediction & anomaly detection  
- **Pillow** - GIF generation
- **HTML/CSS/JS** - Interactive dashboard

## 📦 Data Source

Dataset from Kaggle: [Laptop Sales by Amazon](https://www.kaggle.com/datasets/kamali2727/laptop-sales-by-amazon)

- 4,447 laptop listings
- 17 features including price, specs, ratings, sales

## 🚀 Quick Start

```bash
# Clone the repo
git clone https://github.com/Ericdataplus/kaggle-laptop-sales.git
cd kaggle-laptop-sales

# Install dependencies
pip install pandas matplotlib seaborn scikit-learn pillow kagglehub

# Generate all visualizations
python scripts/run_all.py        # Static charts
python scripts/run_all_gifs.py   # Animations
python scripts/deep_analysis.py  # Advanced analysis

# Open dashboard
start index.html  # Windows
open index.html   # Mac
```

## 📄 License

MIT License - Feel free to use and modify!

---

Made with 📊 and Python by [Ericdataplus](https://github.com/Ericdataplus) | December 2024
