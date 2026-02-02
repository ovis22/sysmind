# SysMind: Autonomous SRE Agent (Gemini 3 Hackathon)

[![Gemini 3 Native](https://img.shields.io/badge/Gemini--3_Native-blue?logo=google-gemini)](https://ai.google.dev/)
[![EIT Digital Ready](https://img.shields.io/badge/EIT_Digital-Aalto_%7C_KTH-orange)](https://www.eitdigital.eu/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**SysMind** is a "Grand Prize" grade autonomous Site Reliability Engineering (SRE) agent. Powered by **Gemini 3 Flash**, it implements a full **Human-in-the-Loop** safety architecture to diagnose and remediate real-world infrastructure failures.

---

## 🧠 Cognitive Architecture: Visible Reasoning

SysMind doesn't just execute; it thinks. By leveraging Gemini 3's **Native Function Calling** and **Chain-of-Thought (CoT)** enforcement:

1.  **Observe**: Active exploration via `list_directory` (The Eyes) and `get_net_stats`.
2.  **Orient**: Analyzes technical telemetry through a persistent **SRE Persona**.
3.  **Decide**: Formulates a detailed **THOUGHT** reasoning trace before every action.
4.  **Act**: Executes native tools with a **10-second safety fuse**.

### Visible Chain-of-Thought
During operation, the agent provides full transparency into its decision-making:
```text
[BRAIN] Reasoning: High CPU detected in stress-ng-vm process. Investigating if this is the target villain.
[ACTION] kill_process {'pid': 1234, 'force': True}
```

---

## 🛡️ Industrial Grade Safety & Resilience

-   **Human-in-the-Loop (HITL)**: Crucial for production safety. Every destructive action (`kill`, `rm`, `restart`) requires **Interactive Human Approval**.
-   **Execution Verification**: All system calls are protected by timeouts to prevent "freezing" in erratic Docker environments.
-   **Terminal Stability**: Purged of non-ASCII characters for 100% stable logs on all terminal encodings.
-   **Surgical Diagnosis**: Utilizes `grep` with context and `systemctl` status checks for a professional, non-destructive approach.

---

## 🚀 The Grand Prize Demo (Real Stress)

SysMind is tested against **real resource pressure**, not just script simulations:

1.  **Prepare**:
    ```bash
    docker build -t sysmind-target ./target-node
    docker run -d --name sysmind-target sysmind-target
    ```
2.  **Chaos Injection (Real Load)**:
    ```bash
    python chaos_injector.py  # Launches real stress-ng load (80% Memory)
    ```
3.  **Autonomous Remediation**:
    ```bash
    python run_agent.py  # Watch the Agent diagnose and wait for your approval to repair
    ```

---

## ⚙️ Technical Specifications

### System Requirements
*   **Operating System**: Linux (for Target), Windows/Linux/macOS (for Agent).
*   **Memory**: Minimum **2GB RAM** recommended for the target container (to safely handle `stress-ng` chaos scenarios).
*   **API**: Valid `GEMINI_API_KEY` with access to Gemini 3 Flash.

### Security Architecture (Enterprise Grade)
*   **Shell Injection Immunity**: Every diagnostic tool (`grep`, `tail`, `ls`, `printf`) uses `shlex.quote` on all user-controlled inputs. This prevents the Agent (or a malicious prompt) from hijacking the system shell.
*   **Human-in-the-Loop (HITL)**: Destructive actions are gated by interactive human approval.
*   **Privilege Disclosure**: While the demo agent uses `sudo` for service management within the isolated Docker container, a production deployment should follow the **Principle of Least Privilege (PoLP)** by granting specific CAP_SYS_PTRACE or tailored sudoers permissions.

---
*Created for the Gemini 3 Hackathon. Bridging the gap between Advanced AI Autonomy and Production-Grade Safety.*
