# 🎬 SysMind Grand Prize Demo: The "Titanium" Script

Use this script to record your 3-minute hackathon submission video.

## 🛠️ Preparation
1. **Open 3 Terminal Windows** (Side-by-Side is best).
   - **Terminal 1:** For the Target Container.
   - **Terminal 2:** For SysMind Agent.
   - **Terminal 3:** For Chaos Injector.
2. **Ensure Audio is ON** (for Voice Feedback).
3. **Environment:** Make sure `.env` has your `GEMINI_API_KEY`.

---

## 🎥 Recording Steps

### Scene 1: The Setup (0:00 - 0:30)
*Action:* Show the title screen (README.md on GitHub) briefly.
*Voiceover:* "Hi, I'm [Your Name]. This is SysMind Titanium – an Autonomous SRE Agent powered by Gemini 3. It doesn't just fix servers; it learns, assesses risk, and adheres to strict safety protocols."

### Scene 2: The Infrastructure (0:30 - 0:45)
*Terminal 1:* Start the target container.
```powershell
# In Terminal 1
docker run --rm --name sysmind-target -d --privileged ubuntu:24.04 sleep infinity
docker exec -it sysmind-target bash -c "apt update && apt install -y stress-ng python3 procps net-tools"
```
*Voiceover:* "We have a live Linux production server running in Docker."

### Scene 3: The Attack (0:45 - 1:00)
*Terminal 3:* Inject the fault.
```powershell
# In Terminal 3
python chaos_injector.py cpu
```
*Action:* Show the log output saying "Chaos Injected".
*Voiceover:* "I'm injecting a critical CPU spike that simulates a runaway process crashing the system."

### Scene 4: The AI Response (1:00 - 2:30)
*Terminal 2:* Launch the Agent.
```powershell
# In Terminal 2
python run_agent.py
```
*Visuals to Highlight:*
1. **ASCII Art:** "Titanium Edition".
2. **Connecting:** Agent verifies connectivity.
3. **Reasoning Panels:** Point out the **RED/GREEN panels**.
   - *Voiceover:* "Notice the Risk Assessment panel. SysMind evaluates the 'Blast Radius' before every command. It's not guessing; it's protecting the system."
4. **Google Grounding:** (If it triggers) "It's checking documentation via Google Search."
5. **The Fix:** Agent kills `stress-ng`.
6. **Voice Feedback:** Wait for: *"Mission accomplished. System stabilized."*

### Scene 5: The Knowledge & Audit (2:30 - 3:00)
*Action:* Open `knowledge_base.json` or show the terminal output "[LEARNING] Saved lesson...".
*Voiceover:* "Here's the killer feature. SysMind remembered this fix. Next time, it will be faster. It also generated a full SRE Post-Mortem report."

---

## 🚀 Key Talking Points (Buzzwords for Judges)
- **"Responsible AI"**: Mention the Risk Assessment/Guardrails.
- **"Google Native"**: Mention Gemini 3 & Search Grounding.
- **"ROI"**: "It turns a 30-minute outage into a 30-second fix."
