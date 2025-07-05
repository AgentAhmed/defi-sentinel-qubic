import os
import json
from datetime import datetime
from fpdf import FPDF

from agents.base_agent import BaseAgent
from mcp.context import MemoryContext

class ReportGeneratorAgent(BaseAgent):
    def __init__(self, context: MemoryContext, output_dir="reports"):
        super().__init__("ReportGeneratorAgent", context)
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def generate_json_report(self, data, filename):
        path = os.path.join(self.output_dir, filename)
        with open(path, "w") as f:
            json.dump(data, f, indent=4)
        self.log(f"JSON report saved to: {path}")

    def generate_pdf_report(self, data, filename):
        path = os.path.join(self.output_dir, filename)
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="DeFi Sentinel – Smart Contract Audit Report", ln=True, align="C")
        pdf.ln(10)

        for idx, vuln in enumerate(data, 1):
            pdf.set_font("Arial", style='B', size=12)
            pdf.cell(0, 10, f"Finding {idx}:", ln=True)
            pdf.set_font("Arial", size=11)
            pdf.multi_cell(0, 10, f"""
Type: {vuln['type']}
Severity: {vuln['severity']} (Risk Score: {vuln['risk_score']})
Details: {vuln.get('details', 'N/A')}
Lines Affected: {vuln.get('lines_affected')}
            """)
            pdf.ln(5)

        pdf.output(path)
        self.log(f"PDF report saved to: {path}")

    def run(self):
        assessed = self.read_context("assessed_vulnerabilities") or []
        if not assessed:
            self.log("No assessed vulnerabilities found.")
            return

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.generate_json_report(assessed, f"audit_report_{timestamp}.json")
        self.generate_pdf_report(assessed, f"audit_report_{timestamp}.pdf")
