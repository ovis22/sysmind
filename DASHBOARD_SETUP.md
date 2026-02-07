# Dashboard Analysis - Setup Guide

SysMind can analyze monitoring dashboards using Gemini 3's multimodal vision capabilities.

## Option A: Generated Dashboard (Recommended for Demo)

Use the included dashboard generator:

```bash
python generate_dashboard.py
```

This creates `dashboard_cpu_spike.png` - a realistic Grafana-style dashboard with:
- CPU spike at 14:23 (92% usage)
- Correlated memory increase (85%)
- Professional dark theme styling

**Pros:** Fast, controlled, reproducible for demos.

## Option B: Real Grafana Screenshot

1. Visit https://play.grafana.org/ (free Grafana demo environment)
2. Navigate to any dashboard (e.g., "Node Exporter Full")
3. Take a screenshot (Windows: Win+Shift+S, Mac: Cmd+Shift+4)
4. Save as `dashboard_real.png`

**Pros:** Shows real Grafana UI, more "authentic" feel.

## Usage

Once you have a dashboard image:

```python
# Agent will call:
analyze_dashboard({'image_path': 'dashboard_cpu_spike.png'})

# Or with real screenshot:
analyze_dashboard({'image_path': 'dashboard_real.png'})
```

## Demo Script

**For video/presentation:**

> "SysMind leverages Gemini 3's multimodal vision to analyze monitoring dashboards. 
> Here's a production incident scenario - a critical CPU spike. Watch how the agent 
> reads the dashboard visually, identifies the anomaly, and correlates it with memory usage."

**Note:** The dashboard analysis capability is real (Gemini 3 vision), the specific 
dashboard shown is a simulated production scenario for demonstration purposes.
