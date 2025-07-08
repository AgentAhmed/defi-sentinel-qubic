# Experimental - for CLI use

import os
import traceback
from agents.code_parser_agent import CodeParserAgent
from agents.vuln_scanner_agent import VulnScannerAgent
from agents.explainability_agent import ExplainabilityAgent
from agents.risk_score_agent import RiskScoreAgent
from agents.report_generator_agent import ReportGeneratorAgent
from mcp.context import MemoryContext

CONTRACTS_DIR = "contracts/"

def scan_contract(filepath):
    """Scan a single smart contract and return analysis results."""
    context = MemoryContext()
    context.write("contract_path", filepath)

    # Initialize agents
    parser = CodeParserAgent(context)
    scanner = VulnScannerAgent(context)
    explainer = ExplainabilityAgent(context)
    scorer = RiskScoreAgent(context)
    reporter = ReportGeneratorAgent(context)

    try:
        parser.run()
        scanner.run()
        explainer.run()
        scorer.run()
        reporter.run()

        assessed = context.read("assessed_vulnerabilities") or []

        result = {
            "vulnerabilities": assessed,
            "risk_score": context.read("overall_risk_score", 0),
            "risk_level": context.read("risk_level", "Unknown"),
            "report_path": context.read("report_path", "")
        }

        print(f"✅ Scanned: {os.path.basename(filepath)}")
        return result

    except Exception as e:
        print(f"❌ Error scanning {filepath}: {str(e)}")
        traceback.print_exc()
        return {"error": str(e)}

def scan_directory(directory_path=CONTRACTS_DIR):
    """Scan all contracts in a directory and return a dict of results."""
    results = {}

    if not os.path.exists(directory_path):
        return {"error": f"Directory '{directory_path}' does not exist."}

    files = [f for f in os.listdir(directory_path) if f.endswith(".cpp")]

    if not files:
        print("⚠️ No .cpp smart contracts found in the directory.")
        return results

    for filename in files:
        filepath = os.path.join(directory_path, filename)
        print(f"\n📄 Scanning {filename}...")
        results[filename] = scan_contract(filepath)

    return results

# CLI usage
if __name__ == "__main__":
    print("🔍 Starting Batch Contract Scanner...")
    scan_directory()
