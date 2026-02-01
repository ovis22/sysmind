# SysMind: Autonomous SRE Agent (Gemini 3 Hackathon)

[![Gemini 3 Native](https://img.shields.io/badge/Gemini--3_Native-blue?logo=google-gemini)](https://ai.google.dev/)
[![EIT Digital Ready](https://img.shields.io/badge/EIT_Digital-Aalto_%7C_KTH-orange)](https://www.eitdigital.eu/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**SysMind** is a "Platinum" grade autonomous Site Reliability Engineering (SRE) agent powered by **Gemini 3 Flash**. It goes beyond simple chatbot logic by implementing native **Function Calling** to manage, diagnose, and remediate Linux infrastructure in real-time.

---

## 🧠 Platinum Cognitive Architecture

SysMind implements a sophisticated **OODA Loop** (Observe-Orient-Decide-Act) with native Gemini 3 capabilities:

1.  **Observe**: Native exploration via `list_directory` (The Eyes) and `list_processes`.
2.  **Orient**: Uses **Native System Instructions** to maintain a persistent SRE expert persona.
3.  **Decide**: Generates high-precision **Function Calls** (no Regex parsing required).
4.  **Act**: Executes commands via `docker-exec` with a **10-second safety fuse (Timeout)**.

### Native Reasoning Trace
Instead of predicting text, Gemini 3 outputs structured data that SysMind executes immediately:

```python
# Agent Insight: OOM error detected in syslog.
# Action: Identify process using 'list_processes' 
# Result: Native Function Call list_processes() triggered.
```

---

## 🛡️ Industrial Resilience & Academic alignment

SysMind is built for the **Gemini 3 Hackathon** while adhering to **EIT Digital (Aalto/KTH)** engineering standards:

-   **Visibility (The Eyes)**: Ability to explore `/var/log` or `/etc` autonomously to locate root causes.
-   **Execution Safety**: Every system call is protected by a **timeout** to prevent agent freezing in hanging environments.
-   **Terminal Stability**: Purged of non-ASCII characters to ensure 100% stable logs on all terminal encodings (inc. Windows).
-   **Contextual Security**: Case-insensitive guardrails prevent destructive actions (e.g., `rm` restricted to temp/logs).

---

## 🚀 Getting Started (Hollywood Demo)

Experience the full power of SysMind in a simulated "Chaos Engineering" scenario:

1.  **Build & Run Environment**:
    ```bash
    docker build -t sysmind-target ./target-node
    docker run -d --name sysmind-target sysmind-target
    ```
2.  **Inject Chaos**:
    ```bash
    python chaos_injector.py  # Injects a rogue process & fake OOM error
    ```
3.  **Activate SysMind**:
    ```bash
    python run_agent.py  # Watch the Agent diagnose and kill the villain
    ```

---
*Created for the Gemini 3 Hackathon. Bridging the gap between Advanced AI Reasoning and Linux System Stability.*
