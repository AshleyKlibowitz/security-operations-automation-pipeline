# Threat-Bot: Cybersecurity Automation & Forensics Pipeline

### Enterprise-grade SecOps automation for Detection, Response, and Verification.

**Threat-Bot** is a modular DevSecOps pipeline designed to automate the lifecycle of a security incident. From detecting network anomalies to orchestrating remediation in Jira and performing deep-packet forensics, this project demonstrates a "Closed-Loop" security architecture. It integrates Threat Intelligence (AbuseIPDB) and leverages Browser Automation (Playwright) to self-verify the success of its own incident response workflows.

---

### 🚀 Technical Highlights

This project displays proficiency across distinct phases of the Security Engineering lifecycle:

#### Phase 1: Automated Detection & Threat Intelligence
* **Network Scanning:** Built a custom port scanner in Python (`socket` library) to identify exposed services (e.g., Port 8080) on target infrastructure.
* **Context-Aware Enrichment:** Integrated the **AbuseIPDB API** to automatically query the reputation of detected IP addresses, distinguishing between harmless traffic and known malicious actors.

#### Phase 2: Orchestrated Incident Response (SOAR)
* **Jira Cloud Integration:** Engineered an automated response mechanism using the **Atlassian Jira REST API**.
* **Workflow Automation:** When a high-risk anomaly is detected, the system autonomously provisions a Jira ticket (e.g., `KAN-6`), assigning severity levels and descriptions without human intervention.

#### Phase 3: Forensic Analysis
* **Packet-Level Inspection:** Developed a forensics module using **Scapy** to parse raw PCAP files (`traffic.pcap`).
* **Anomaly Hunting:** Implemented logic to hunt for specific network signatures, such as **TCP Reset (RST)** floods, identifying potential "connection killing" attacks or scanning evasion attempts.

#### Phase 4: Reliability Engineering (Automated QA)
* **End-to-End Verification:** Integrated **Microsoft Playwright** to act as a "Robot Auditor."
* **Visual Proof:** The robot autonomously logs into the Jira dashboard, navigates complex UI elements, and captures photographic proof (`qa_success.png`) that the security alerts were successfully delivered to the SOC board.

---

### 📊 Threat Logic & Metrics

The table below illustrates how raw telemetry is transformed into actionable intelligence:

| Event Input | Context / Logic | Risk Classification | Automated Action |
| :--- | :--- | :--- | :--- |
| **Port 8080 Open** | AbuseIPDB Score > 0 | 🔴 **High Risk** | **Create Ticket:** `Security Alert: Port 8080 Open` |
| **Port 443 Open** | AbuseIPDB Score = 0 | 🟢 **Trusted** | **Log Only:** No alert generated. |
| **TCP Flag: RST** | Packet Analysis (Scapy) | 🟠 **Suspicious** | **Forensics Log:** `[!] Suspicious Activity Detected` |

---

### 🛠 Technology Stack

* **Core Engine:** Python 3.10+
* **Network & Forensics:** Scapy, Socket, PCAP Analysis
* **Orchestration & API:** Jira Cloud REST API, AbuseIPDB API, Requests
* **Automation & QA:** Microsoft Playwright (Headless Browser Testing)
* **Environment:** Dotenv (`.env`) for credential security

---

### 📂 File Structure

The repository is organized to facilitate modular execution of the security pipeline:

* `scanner.py` - The "Watchdog." Scans ports, checks AbuseIPDB reputation, and triggers Jira tickets.
* `forensics.py` - The "Investigator." Analyzes binary PCAP files to find TCP Reset attacks.
* `qa_test.py` - The "Auditor." A Playwright robot that logs into Jira to verify tickets exist.
* `generate_pcap.py` - Utility to generate synthetic malicious traffic for testing forensics logic.
* `logs/` - Stores automated audit trails (`scanner_logs.json`) and visual proofs (`qa_success.png`).

---

### ⚡ Installation & Usage

**1. Clone the Repository**
```bash
git clone [https://github.com/yourusername/threat-bot.git](https://github.com/yourusername/threat-bot.git)
cd threat-bot
```

**2. Configure Environment Create a .env file in the root directory with your credentials:**
```bash
JIRA_USER=your_email@example.com
JIRA_API_TOKEN=your_atlassian_api_token
JIRA_SERVER=[https://your-domain.atlassian.net](https://your-domain.atlassian.net)
JIRA_PROJECT_KEY=KAN
ABUSEIPDB_API_KEY=your_abuseipdb_key
```

**3. Install Dependencies**
```bash
pip install -r requirements.txt
playwright install chromium
```

## 🧪 Test Scenarios

### Scenario A: The "Red Team" Attack (Detection)

**Run the scanner:**
```bash
python scanner.py
```
Result:
The script detects an open port, queries AbuseIPDB, and pushes a ticket to Jira.

### Scenario B: The Forensic Deep-Dive

1.**Generate traffic:**
```bash
python generate_pcap.py
```
2.**Analyze it:**
```bash
python forensics.py
```
3. **Result:** The script parses the binary file and alerts on: [!] Suspicious Activity Detected: TCP Reset (RST).

### Scenario C: The "Robot" Audit

1. **Run the QA bot:**
```bash
python qa_test.py
```
2. **Result:** A Chromium browser launches, logs into your Jira instance, verifies the alert exists, and saves a screenshot to logs/qa_success.png.
