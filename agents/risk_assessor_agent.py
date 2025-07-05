from agents.base_agent import BaseAgent
from mcp.context import MemoryContext

class RiskAssessorAgent(BaseAgent):
    def __init__(self, context: MemoryContext):
        super().__init__("RiskAssessorAgent", context)

    def calculate_risk_score(self, vuln_type, confidence, lines_affected):
        base_score = {
            "Critical": 9,
            "High": 7,
            "Medium": 5,
            "Low": 3
        }.get(confidence, 5)

        # Extra points for large code spans
        range_penalty = 0
        if lines_affected > 20:
            range_penalty = 2
        elif lines_affected > 10:
            range_penalty = 1

        return min(10, base_score + range_penalty)

    def run(self):
        vulnerabilities = self.read_context("vulnerabilities") or []
        assessed = []

        for vuln in vulnerabilities:
            score = self.calculate_risk_score(
                vuln.get("type"),
                vuln.get("confidence", "Medium"),
                vuln.get("lines_affected", 1)
            )

            severity_label = (
                "Critical" if score >= 9 else
                "High" if score >= 7 else
                "Medium" if score >= 5 else
                "Low"
            )

            vuln["risk_score"] = score
            vuln["severity"] = severity_label
            assessed.append(vuln)

        self.write_context("assessed_vulnerabilities", assessed)
        self.log(f"Assessed {len(assessed)} vulnerabilities.")
