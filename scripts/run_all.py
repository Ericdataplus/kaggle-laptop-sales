"""
Run all static graph generation scripts
"""
import subprocess
import sys
import os

# Get script directory
script_dir = os.path.dirname(os.path.abspath(__file__))

# List of scripts to run (in order)
scripts = [
    '01_brand_distribution.py',
    '02_price_analysis.py',
    '03_ram_analysis.py',
    '04_os_analysis.py',
    '05_screen_size_analysis.py',
    '06_graphics_analysis.py',
    '07_top_sellers.py',
    '08_rating_analysis.py',
    '10_summary_dashboard.py',
]

print("🚀 Running all graph generation scripts...")
print("=" * 50)

for script in scripts:
    script_path = os.path.join(script_dir, script)
    if os.path.exists(script_path):
        print(f"\n▶ Running: {script}")
        result = subprocess.run([sys.executable, script_path], 
                               capture_output=True, text=True, cwd=script_dir)
        if result.returncode == 0:
            print(result.stdout.strip())
        else:
            print(f"❌ Error in {script}:")
            print(result.stderr)
    else:
        print(f"⚠️ Script not found: {script}")

print("\n" + "=" * 50)
print("✅ All scripts completed!")
