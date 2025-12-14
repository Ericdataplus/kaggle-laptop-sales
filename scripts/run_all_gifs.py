"""
Run all GIF generation scripts
"""
import subprocess
import sys
import os

script_dir = os.path.dirname(os.path.abspath(__file__))

scripts = [
    'gif_01_brand_race.py',
    'gif_02_price_scatter.py',
    'gif_03_stats_counter.py',
    'gif_04_segment_pie.py',
]

print("🎬 Generating GIF animations...")
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
            print(f"❌ Error: {result.stderr[:200]}")
    else:
        print(f"⚠️ Not found: {script}")

print("\n" + "=" * 50)
print("✅ All GIFs generated!")
