import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta

def generate_spike_image():
    # 1. Create simulated data (Time Points: last 60 minutes)
    now = datetime.now()
    # Create 100 timestamps for the last hour
    timestamps = [now - timedelta(minutes=60 - (i * 0.6)) for i in range(100)]
    time_labels = [t.strftime("%H:%M") for t in timestamps]
    x = np.linspace(0, 60, 100)
    
    # Healthy baseline (20-30% CPU)
    y = 20 + np.random.normal(0, 2, 100)
    
    # Injection point at t=40 (approx 20 mins ago)
    spike_start = 66  # Index approx 2/3rds in
    y[spike_start:] = 98 + np.random.normal(0, 1, 100 - spike_start) # Sudden spike to 98%
    
    # 2. Plotting (Dark Mode / SRE Style)
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Plot line
    ax.plot(x, y, color='#ff6b6b', linewidth=2, label='CPU Usage (%)')
    
    # Highlight spike area
    ax.axvspan(40, 60, color='#ff0000', alpha=0.1, label='Critical Alert Area')
    
    # Styling
    ax.set_title(f"Server Telemetry: sysmind-target [PROD]", fontsize=14, color='white', pad=20)
    ax.set_xlabel('Time (Minutes ago)', fontsize=10)
    ax.set_ylabel('CPU Load (%)', fontsize=10)
    ax.set_ylim(0, 110)
    ax.grid(True, linestyle='--', alpha=0.3)
    ax.legend(loc='upper left')
    
    # Dynamic Anomaly Annotation
    # Calculate time of spike start (~20 mins ago)
    spike_time = (now - timedelta(minutes=20)).strftime("%H:%M")
    
    plt.text(42, 50, f"ANOMALY DETECTED\nTime: {spike_time} UTC", color='red', fontsize=12, fontweight='bold')
    
    # Custom X-axis labels (show only every 10th label to avoid clutter)
    # We map 0..60 scale to real time
    x_positions = np.linspace(0, 60, 6) # 0, 12, 24, 36, 48, 60
    # Corresponding times
    x_labels = [(now - timedelta(minutes=60 - val)).strftime("%H:%M") for val in x_positions]
    ax.set_xticks(x_positions)
    ax.set_xticklabels(x_labels)
    
    # Save
    filename = "dashboard_cpu_spike.png"
    plt.savefig(filename, dpi=100, bbox_inches='tight')
    print(f"[OK] Generated dynamic dashboard artifact: {filename} (Anomaly at: {spike_time})")

if __name__ == "__main__":
    try:
        generate_spike_image()
    except ImportError:
        print("[ERROR] matplotlib missing. Run: pip install matplotlib")
