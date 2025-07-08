# DeFi Sentinel – Qubic C++ Smart Contract Auditor

## 🌐 Overview
**DeFi Sentinel** is an AI-powered agentic tool designed to audit and verify C++ smart contracts deployed on the Qubic Network. By combining static code analysis with multi-agent intelligence via Model Context Protocol (MCP), the platform detects vulnerabilities, scores risk, and generates human-readable audit reports—accelerating secure development in decentralized finance (DeFi).

## 🎯 Purpose
To demonstrate a real-world application of decentralized computation using Qubic's smart contract architecture, while showcasing how AI and agentic tools can empower developers with secure-by-design workflows.

🔹 Short Description (≤255 characters):
AI-powered C++ smart contract auditor for the Qubic Network. Uses modular agents and Groq’s LLaMA to detect vulnerabilities, assess risk, and generate audit reports in PDF/JSON.

🔹 Long Description (≥100 words):
DeFi Sentinel is an autonomous auditing platform designed to ensure the security of smart contracts on the Qubic Network. It uses a multi-agent architecture built with the Model Context Protocol (MCP) to analyze C++ code, detect vulnerabilities, score risks, and generate readable reports. Enhanced by Groq's LLaMA3 model, the system explains potential exploits, recommends fixes, and supports both single and batch scanning. A Streamlit-based dashboard allows real-time analysis, PDF/JSON downloads, and an optional chatbot assistant. This project solves the critical problem of smart contract insecurity and helps developers ship safer DeFi apps faster.

🔹 Technology & Category Tags (choose from Lablab options):
AI Agent, Cybersecurity, DeFi, Smart Contracts, Blockchain, Groq, Python, C++, Qubic, Streamlit

---

## 🧠 Core Features
- ✅ AI-powered code parsing and vulnerability detection
- ✅ Agent-based architecture powered by MCP (Model Context Protocol)
- ✅ C++ static analysis and pattern matching
- ✅ Risk severity scoring for vulnerabilities
- ✅ Audit report generation in JSON & PDF formats
- ✅ Ready for deployment on the Qubic Testnet

---

## 🏗 Architecture
```
User Input → CodeParserAgent → VulnScannerAgent → RiskAssessorAgent → ReportGeneratorAgent
```
Each agent communicates through shared memory/context layers using MCP, forming a dynamic and modular pipeline.

---

## ⚙️ Tech Stack
- **Python** (agent system, MCP, UI)
- **C++** (Qubic contracts)
- **Streamlit** (UI dashboard)
- **Groq API** (LLaMA 3 LLM)
- **FPDF** (Unicode PDF generation)
- **Qubic CLI** (testnet deployment)
- **dotenv** (API config management)

---

## 🚀 How to Run
1. Clone the repo:
```bash
git clone https://github.com/your-username/defi-sentinel-qubic.git
cd defi-sentinel-qubic
```
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Run audit interface locally:
```bash
streamlit run frontend/audit_editor.py
```
4. Test vulnerability scanner:
```bash
python test/test_vuln_scanner.py
```

---

## 📦 Folder Structure
```
defi-sentinel-qubic/
├── agents/                # Modular AI agents (parser, scanner, risk, report, insights)
├── contracts/             # Sample C++ smart contracts for auditing
├── frontend/              # Streamlit-based UI interface
├── mcp/                   # Model Context Protocol implementation (shared memory)
├── scripts/               # Testnet deploy, verify, compile, batch audit
├── fonts/                 # DejaVuSans.ttf for Unicode PDF support
├── reports/               # Auto-generated audit reports (PDF & JSON)
├── test/                  # Unit and agent tests
├── .env                   # Add GROQ_API_KEY here
├── requirements.txt       
├── setup.py               # Editable package installer
└── README.md

```

---

## 🧭 Roadmap
- [x] Project scaffold + agent architecture
- [x] Sample contract + AST parser
- [x] Vulnerability scanner (beta)
- [ ] MCP integration between agents
- [ ] Streamlit-based frontend UI
- [ ] Audit report exporter (PDF + JSON)
- [ ] Live Qubic testnet deployment
- [ ] Video walkthrough demo

---

## ✅ Hackathon Submission Checklist
- [x] Clear setup & run instructions
- [x] System architecture
- [x] Project roadmap
- [x] Public GitHub repo
- [ ] Qubic testnet deployment
- [ ] Demo video

---

🧩 Challenge Alignment
This project addresses the Qubic Track’s official challenge:
“C++ Smart Contract Audit Tool – Develop an AI toolchain or analyzer that can help audit and verify smart contracts written in C++ on Qubic.”

DeFi Sentinel delivers this via a modular, multi-agent auditing system built with Python, MCP, and deployed on the Qubic testnet—making smart contract security more accessible, scalable, and developer-friendly.

## 🔗 Useful Links
- [Qubic Docs](https://docs.qubic.org)
- [Model Context Protocol (MCP)](https://github.com/microsoft/mcp-for-beginners)
- [Hackathon Event Page](https://lablab.ai/event/raise-your-hack)

---

**Team Name**: Andromeda – Qubic Track  
