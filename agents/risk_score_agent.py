from agents.base_agent import BaseAgent

class RiskScoreAgent(BaseAgent):
    def __init__(self, context):
        super().__init__("RiskScoreAgent", context)

    def run(self):
        vulnerabilities = self.read_context("vulnerabilities", [])

        severity_weights = {
            "Low": 10,
            "Medium": 25,
            "High": 50,
            "Critical": 100
        }

        score = 0
        for vuln in vulnerabilities:
            severity = vuln.get("severity", "Low")
            score += severity_weights.get(severity, 10)

        score = min(score, 100)

        if score >= 75:
            level = "Critical"
        elif score >= 50:
            level = "High"
        elif score >= 25:
            level = "Medium"
        elif score > 0:
            level = "Low"
        else:
            level = "None"

        self.write_context("overall_risk_score", score)
        self.write_context("overall_risk_level", level)
