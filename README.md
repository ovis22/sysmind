# SysMind: Autonomous SRE Agent (Gemini 3 Hackathon)

[![Gemini 3 Native](https://img.shields.io/badge/Gemini-3_Native-blue?logo=google-gemini)](https://ai.google.dev/)
[![EIT Digital Ready](https://img.shields.io/badge/EIT_Digital-Aalto_%7C_KTH-orange)](https://www.eitdigital.eu/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**SysMind** is an autonomous Site Reliability Engineering (SRE) agent powered by **Gemini 2.0 Flash**. It doesn't just answer questions; it actively manages, diagnoses, and remediates Linux infrastructure in real-time using an intelligent **OODA Loop**.

---

## 🧠 The Agentic Heart: OODA Loop Reasoning

SysMind operates on the **Observe-Orient-Decide-Act (OODA)** cycle:

1.  **Observe**: Captures raw system telemetry.
2.  **Orient**: Uses Gemini 2.0 Flash to contextualize anomalies.
3.  **Decide**: Formulates a remediation plan.
4.  **Act**: Executes commands via secure transport.

### Example Reasoning Path
```json
{
  "thought": "I see high memory usage in syslog. Checking process list to identify the consumer.",
  "tool": "list_processes",
  "args": {}
}
```

---

## 🛡️ Industry-Standard Alignment (Academic Grade)

This project bridges the gap between **Google's Gemini 3 Hackathon** and the **EIT Digital Master School** curricula:

-   **Operating Systems (Aalto)**: Low-level `/proc` and signal management.
-   **Network Service Provisioning (Aalto)**: Auto-remediation of network daemons.
-   **Distributed AI (KTH)**: Multi-step reasoning loops and agentic autonomy.
-   **Resilience Engineering**: Implementation of **Exponential Backoff** and **Bulletproof Regex Parsing** for distributed stability.

---

## � Engineering Excellence

### Transport Layer
By leveraging `subprocess` and `docker exec` hooks, SysMind maintains zero-trust connectivity even when Port 22/SSH is restricted.

### Safety Guardrails
Includes a **Human-in-the-Loop** confirmation for dangerous operations:
- Case-insensitive protection against `rm -rf`, `kill -9`, `reboot`, `iptables`, etc.

> **Scalability Note:** SysMind's stateless and modular architecture allows for seamless deployment as a Kubernetes Sidecar, enabling proactive pod self-healing and autonomous remediation across massive distributed clusters.

---

## � Getting Started

1.  **Build Target Node**:
    ```bash
    docker build -t sysmind-target ./target-node
    ```
2.  **Run Environment**:
    ```bash
    docker run -d --name sysmind-target sysmind-target
    ```
3.  **Configure**:
    Add your `GEMINI_API_KEY` to the `.env` file.
4.  **Activate**:
    ```bash
    python run_agent.py
    ```

---
*Created for the Gemini 3 Hackathon. Bridging the gap between LLMs and Linux Kernels.*
