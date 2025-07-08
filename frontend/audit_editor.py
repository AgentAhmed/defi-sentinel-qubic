import os
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
import tempfile
import streamlit as st
from dotenv import load_dotenv
from mcp.context import MemoryContext
from agents import (
    CodeParserAgent,
    VulnScannerAgent,
    ExplainabilityAgent,
    RiskScoreAgent,
    ReportGeneratorAgent,
    AIInsightsAgent,
)
from your_llm.groq import GroqLLM

load_dotenv()

QUBIC_TEMPLATE = """#include <qubic.h>

CONTRACT {contract_name} : public Contract {{
public:
    {contract_name}() {{}}
    ACTION void init() {{}}
    ACTION uint64_t calculate(uint64_t a, uint64_t b) {{
        return a + b;
    }}
    ON_TRANSFER void onTransfer(Address from, uint64_t amount) {{
    }}
}};
"""

def run_audit(contract_path: str, contract_name: str = "contract"):
    context = MemoryContext()
    context.write("contract_path", contract_path)
    context.write("contract_name", contract_name)

    llm = GroqLLM(api_key=os.getenv("GROQ_API_KEY"))
    agents = [
        CodeParserAgent(context),
        VulnScannerAgent(context),
        ExplainabilityAgent(context),
        RiskScoreAgent(context),
        AIInsightsAgent(context, llm=llm),
        ReportGeneratorAgent(context)
    ]

    try:
        for agent in agents:
            try:
                agent.run()
            except Exception as e:
                print(f"[WARN] Agent {agent.name} failed: {e}")
        return {
            "vulnerabilities": context.read("vulnerabilities", []),
            "risk_score": context.read("overall_risk_score", 0),
            "risk_level": context.read("overall_risk_level", "Unknown"),
            "pdf_path": context.read("pdf_report_path", ""),
            "json_path": context.read("json_report_path", ""),
            "ai_analysis": context.read("ai_analysis", "")
        }
    except Exception as e:
        return {"error": str(e)}

def run_audit_from_code(code: str, contract_name: str):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".cpp", mode="w", encoding="utf-8") as tmp:
        tmp.write(code)
        tmp_path = tmp.name
    result = run_audit(tmp_path, contract_name)
    os.remove(tmp_path)
    return result

def run_audit_from_upload(uploaded_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".cpp", mode="wb") as tmp:
        tmp.write(uploaded_file.getvalue())
        tmp_path = tmp.name
    result = run_audit(tmp_path, uploaded_file.name.split('.')[0])
    os.remove(tmp_path)
    return result

st.set_page_config(page_title="Qubic c++ Smart Contract Auditor", layout="wide")
if "last_mode" not in st.session_state:
    st.session_state.last_mode = None

st.title("🛡️ Qubic C++ Smart Contract Auditor")

if "contract_code" not in st.session_state:
    st.session_state.contract_code = QUBIC_TEMPLATE.format(contract_name="MyContract")
if "contract_name" not in st.session_state:
    st.session_state.contract_name = "MyContract"
if "audit_results" not in st.session_state:
    st.session_state.audit_results = None

mode = st.sidebar.radio("Select Mode", ["Editor", "Upload", "Batch Scan"])

# Detect mode change
if st.session_state.last_mode != mode:
    st.session_state.audit_results = None
    st.session_state.last_mode = mode


if mode == "Editor":
    st.subheader("📝 Contract Editor")
    st.session_state.contract_name = st.text_input("Contract Name", st.session_state.contract_name)
    st.session_state.contract_code = st.text_area("Edit your contract code:", st.session_state.contract_code, height=400)

    if st.button("Run Audit"):
        if st.session_state.contract_code.strip():
            with st.spinner("Auditing contract..."):
                st.session_state.audit_results = run_audit_from_code(
                    st.session_state.contract_code,
                    st.session_state.contract_name
                )
        else:
            st.warning("Please enter contract code")

elif mode == "Upload":
    st.subheader("📤 Upload Contract")
    uploaded_file = st.file_uploader("Choose a .cpp file", type=["cpp"])
    if uploaded_file and st.button("Audit Uploaded File"):
        with st.spinner("Analyzing contract..."):
            st.session_state.audit_results = run_audit_from_upload(uploaded_file)
            st.session_state.contract_name = uploaded_file.name.split('.')[0]

elif mode == "Batch Scan":
    st.subheader("📁 Batch Audit")
    uploaded_files = st.file_uploader("Upload multiple .cpp files", type=["cpp"], accept_multiple_files=True)
    if uploaded_files and st.button("Run Batch Audit"):
        for uploaded_file in uploaded_files:
            with st.spinner(f"Auditing {uploaded_file.name}..."):
                result = run_audit_from_upload(uploaded_file)
                st.markdown(f"### 📄 {uploaded_file.name}")
                st.metric("Risk Score", f"{result['risk_score']}/100")
                st.metric("Vulnerabilities", len(result['vulnerabilities']))
                if result.get("ai_analysis"):
                    st.markdown("**🤖 AI Insights**")
                    st.markdown(result["ai_analysis"])
                for vuln in result.get("vulnerabilities", []):
                    with st.expander(f"{vuln['type']} - {vuln.get('severity', 'Unknown')}"):
                        st.write(f"**Location:** {vuln.get('location', 'Unknown')}")
                        st.write(vuln.get("description", ""))

if st.session_state.get("audit_results"):
    results = st.session_state.audit_results
    if "error" in results:
        st.error(f"Audit failed: {results['error']}")
    else:
        st.subheader("🔍 Audit Results")
        col1, col2 = st.columns(2)
        col1.metric("Risk Score", f"{results['risk_score']}/100")
        col2.metric("Vulnerabilities", len(results['vulnerabilities']))

        st.subheader("📊 Download Reports")
        col_pdf, col_json = st.columns(2)
        if results.get("pdf_path") and os.path.exists(results["pdf_path"]):
            with open(results["pdf_path"], "rb") as f:
                pdf_bytes = f.read()
                col_pdf.download_button(
                    label="📄 Download PDF Report",
                    data=pdf_bytes,
                    file_name=os.path.basename(results["pdf_path"]),
                    mime="application/pdf"
                )


        if results.get("json_path") and os.path.exists(results["json_path"]):
            with open(results["json_path"], "rb") as f:
                json_bytes = f.read()
                col_json.download_button(
                    label="🧾 Download JSON Report",
                    data=json_bytes,
                    file_name=os.path.basename(results["json_path"]),
                    mime="application/json"
                )



        st.subheader("⚠️ Detected Vulnerabilities")
        for vuln in results.get("vulnerabilities", []):
            with st.expander(f"{vuln['type']} - {vuln.get('severity', 'Unknown')}"):
                st.write(f"**Location:** {vuln.get('location', 'Unknown')}")
                st.write(vuln.get("description", ""))
                if vuln.get("recommendation"):
                    st.write("**Recommendation:**")
                    st.write(vuln["recommendation"])

        if results.get("ai_analysis"):
            st.subheader("🤖 AI Insights")
            st.markdown(results["ai_analysis"])
