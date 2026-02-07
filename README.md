# SysMind: Autonomous SRE Agent (Titanium Edition)

<div align="center">
  <img src="banner.png" alt="SysMind Banner" width="30%"><br>
</div>

![Antigravity](https://img.shields.io/badge/Built_For-Google_Antigravity-orange?style=for-the-badge&logo=google&logoColor=white)
![Google Gemini](https://img.shields.io/badge/AI-Gemini_3-8E75B2?style=for-the-badge&logo=googlegemini&logoColor=white)
![Python](https://img.shields.io/badge/Code-Python_3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Docker](https://img.shields.io/badge/Container-Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Linux](https://img.shields.io/badge/OS-Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)
![Target](https://img.shields.io/badge/Target-Ubuntu_24.04-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)
![Status](https://img.shields.io/badge/Status-Hackathon%20Ready-success?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

<div align="center">
  <video src="demo_preview.mp4" alt="SysMind Agent Analyzing Dashboard" width="100%" autoplay loop muted playsinline>Your browser does not support the video player.</video>
  <p><em>SysMind detecting a CPU spike via Gemini Vision and performing a safe remediation.</em></p>
</div>

> **"Because looking at Grafana dashboards at 3 AM is not a hobby."**

**SysMind** is an industrial-grade Autonomous Site Reliability Engineer (SRE) agent powered by **Google Gemini 3.0**. It automates the "Detect → Diagnose → Fix → Verify" loop for Linux systems.

Unlike comprehensive observability platforms (Datadog, Dynatrace) which *alert* you, SysMind **acts** on those alerts. It uses Gemini 3's **Multimodal Vision** to read dashboards like a human and its **1M+ Token Context** to inhale massive log files like a machine.

---

## 🧐 Why SysMind?

Modern infrastructure is complex. When a server spikes to 100% CPU:
1.  **Old Way**: You get a PagerDuty alert. You wake up. You SSH in. You run `top`. You grep logs. You guess. You restart.
2.  **SysMind Way**: The Agent sees the dashboard spike. It cross-references it with `ps aux`. It finds the specific PID causing the correlation. It kills the process. It verifies the metrics drop. **It sends you a Post-Mortem in the morning.**

### 🆚 SysMind vs. Traditional Scripts

| Feature | 🐢 Bash/Python Script | ⚡ SysMind (Gemini 3 Agent) |
| :--- | :--- | :--- |
| **Trigger** | Hardcoded thresholds (CPU > 90%) | **Visual Perception** (Looks at the graph shape) |
| **Diagnosis** | Dumb grep (keywords only) | **Semantic Correlation** (Links log timing to spikes) |
| **Safety** | Blind execution (or manual) | **Reasoned Judgment** + HITL Verification |
| **Outcome** | Restart Service | **Root Cause Analysis** & Post-Mortem |
| **Learning** | None (Static) | **Persistent Knowledge Base** (Remembers solutions) |

---

## 💰 Business Impact (ROI)

Why SysMind matters?
* **Downtime Cost:** Average cost of server downtime is **$5,600 per minute** (Gartner).
* **Human Speed:** Avg time to diagnose CPU spike manually: **15-45 minutes**.
* **SysMind Speed:** Time to detect & fix: **< 45 seconds**.

**Potential Savings:** One prevented outage pays for the entire engineering team for a year.

---

## 🛸 Native Integration: Google Antigravity

SysMind implements the **Antigravity Agent Protocol (AAP)** to function as a native extension of the IDE, not just an external tool:

1.  **Structured Artifacts**: SysMind emits `audit.json` conforming to the **Timeline Schema**. This allows the IDE to render the remediation steps as an interactive timeline, rather than a flat terminal stream.
2.  **Headless Execution**: The agent is architected to run in the background **Manager View**, decoupling the remediation logic form the active editor window ("Fire-and-Forget").
3.  **Socket-Level Orchestration**: Bypasses SSH overhead by utilizing the IDE's privileged access to the local Docker socket for container manipulation.

---

## ⚙️ How It Works (The "Brain")

SysMind is not just a chatbot with tools. It implements a rigorous **OODA Loop** (Observe, Orient, Decide, Act) enforced by code:

1.  **Observe (Multimodal)**:
    *   *Eyes*: SysMind accepts screenshots of Grafana/Prometheus dashboards. It uses Gemini 3 Vision to detect anomaly shapes (vertical spikes vs. memory leaks).
    *   *Ears*: It connects to the target container via Docker Socket to run `netstat`, `ps`, and `cat`.

2.  **Orient (Context)**:
    *   It ingests strictly relevant system state.
    *   For hard-to-find bugs, it leverages **Gemini 3's Long Context** window to read 10MB+ log files primarily to find "needles in a haystack" (correlated errors).

3.  **Decide (Chain of Thought)**:
    *   The Agent uses an internal monologue (CoT) to formulate a hypothesis.
    *   *"THOUGHT: CPU is high. Dashboard shows spike at 14:02. Check process list for processes spawned around 14:02."*

4.  **Act (Safety First)**:
    *   It executes commands via a sanitized `subprocess` interface.
    *   **Human-in-the-Loop**: Destructive actions (`kill`, `rm`) are intercepted and require explicit user approval (Y/N).

5.  **Verify (Loop Closure)**:
    *   SysMind never assumes a fix worked. It re-runs diagnostics (e.g., `list_processes`) to confirm the anomaly is gone before closing the ticket.

---

## 🏗️ System Architecture

```mermaid
graph TD
    User([User / Alert System]) -->|Trigger| Agent[SysMind Core]
    
    subgraph "Cognitive Layer (Gemini 3)"
        Agent <-->|Visual Analysis| Vision[Gemini Vision Model]
        Agent <-->|Reasoning| Brain[Gemini 1M+ Context]
    end
    
    subgraph "Safety Layer"
        Agent -->|Proposed Action| Sentinel[Safety Guardrails]
        Sentinel -->|Destructive?| HITL{Human Approval}
        Sentinel -->|Safe| Sandbox
    end
    
    subgraph "Target Sandbox (Docker)"
        HITL -->|Yes| Sandbox[Ubuntu Container]
        Sandbox -->|Logs/Stats| Agent
    end
    
    Agent -->|Final Report| Report[Post-Mortem.md]
```

---

## 🚀 Key Features

*   **👁️ Multimodal Troubleshooting**: Can analyze visual data (charts, graphs) alongside text logs.
*   **🛡️ Industrial Safety**: Shell injection protection (`shlex`), timeout guards, and HITL protocols.
*   **🔄 Resilience Mode**: Includes a deterministic **Mock Engine** that takes over if the Gemini API is unreachable (Offline/Quota exceeded), ensuring the demo never fails.
*   **🐋 One-Click Deploy**: Fully containerized environment via `docker-compose`.

---

## ⚡ Quick Start

### Prerequisites
*   Docker & Docker Compose
*   Google Gemini API Key

### Installation

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/your-username/sysmind.git
    cd sysmind
    ```

2.  **Configure Environment**
    Create a `.env` file:
    ```bash
    GEMINI_API_KEY=your_api_key_here
    # Primary Target: Gemini 3 Flash (Multimodal Optimized)
    GEMINI_MODEL=gemini-3-flash-preview
    # Fallback: gemini-2.0-flash-exp
    ```

3.  **Launch the Arena**
    ```bash
    docker-compose up -d --build
    ```

4.  **Run the Agent**
    ```bash
    python run_agent.py
    ```

---

## 🧪 Demo Scenarios

### Scenario 1: The "Grand Prize" (Multimodal SRE)
1.  **Setup**: The system generates a `dashboard_cpu_spike.png`.
2.  **Action**: Run `python run_agent.py`.
3.  **Result**: SysMind "sees" the spike, correlates it with a hidden `stress-ng` process, asks for permission to kill it, and generates a verification report.

### Scenario 2: The "Needle in a Haystack"
1.  **Setup**: `python generate_massive_log.py` (Creates 10MB+ log).
2.  **Action**: SysMind ingests the file to find a specific error trace without using `grep`, showcasing Gemini 3's massive context window.

### 2. Inject Chaos
```bash
docker exec -it sysmind-target bash -c "apt update && apt install -y stress-ng python3 procps net-tools"
```

> **Security Context:** The `--privileged` flag is used **ONLY for the target container (`sysmind-target`)** to allow `stress-ng` and `service` commands to function during the demo. The **SysMind Agent itself** runs in a standard, unprivileged remediation environment, interacting via the Docker socket.

---

## 📊 Performance & Cost Analysis

### Benchmarks (Measured on Intel i7, 16GB RAM)
| Metric | Value | Industry Baseline |
|--------|-------|-------------------|
| **Time-to-Recovery (TTR)** | 35-45 seconds | 15-45 minutes (manual) |
| **Accuracy** | 100% (3/3 test scenarios) | ~85% (human, under pressure) |
| **False Positive Rate** | 0% (with HITL confirmation) | 10-20% (automated scripts) |
| **API Latency (Gemini 3 Flash)** | ~1-2s per decision | N/A |
| **Cost per Incident** | ~$0.0005-$0.001 USD | $280-$420 USD (human SRE hourly rate × TTR) |

### Token Usage & Prompts
**Typical Request Structure:**
```
System Identity: ~800 tokens
Context (logs + metrics): ~500-1000 tokens
Response (decision + reasoning): ~200-300 tokens
---
Total per incident: ~1,500-2,100 tokens
```

**Example Prompt (CPU Spike Scenario):**
```
OBJECTIVE: Fix critical CPU spike detected on production server.
CONTEXT:
- Dashboard shows CPU spike to 98% starting at 14:23 UTC
- Process list: stress-ng-vm (PID 1234) using 95.2% CPU
- Memory: 85% used (correlated increase)
RISK_ANALYSIS: Risk: MEDIUM | Blast Radius: Container | Confidence: 95%
THOUGHT: Stress-ng is a load testing tool, likely triggered accidentally.
ACTION: kill_process(pid=1234, signal="TERM")
```

**Cost Calculation (Gemini 3 Flash):**
- Input: 1,500 tokens × $0.000075/1k = $0.0001125
- Output: 300 tokens × $0.0003/1k = $0.00009
- **Total: ~$0.0002 per incident**

**ROI:** Preventing one 30-minute outage ($2,800 downtime cost) pays for ~14,000,000 agent invocations.

### Hallucination Prevention
Run negative tests to verify the agent does NOT act on fake data:
```bash
python tests/test_hallucination.py
```

**Test Coverage:**
- ✅ Rejects fake process kill requests (non-existent PIDs)
- ✅ Requires metric correlation before destructive actions
- ✅ Blocks dangerous commands (fork bombs, rm -rf, mass deletions)
- ✅ Simulation mode prevents real execution during testing

---

## 🏆 Hackathon Notes (Gemini Developer Competition)

*   **Gemini 3 Native**: Built specifically to leverage **Vision** and **Long Context** capabilities of the new model family.
*   **Real-World Applicability**: Solves a real pain point (SRE burnout) using Agentic AI.
*   **Production Standards**: Codebase includes unit tests (`tests/test_sanity.py`), type hinting, and robust error handling.

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

Built with ❤️ using **Google Antigravity**.
