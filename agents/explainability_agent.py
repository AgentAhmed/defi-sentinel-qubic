from agents.base_agent import BaseAgent

class ExplainabilityAgent(BaseAgent):
    def __init__(self, context):
        super().__init__("ExplainabilityAgent", context)

    def get_explanation(self, vuln_type):
        explanations = {
            "Hardcoded Credentials": (
                "Hardcoded credentials (e.g., API keys, passwords) present a severe security risk. "
                "They can be extracted from compiled binaries or open-source repositories."
            ),
            "Unchecked External Call": (
                "Calls to external systems (e.g., using `system()` or raw IO) without proper validation "
                "may allow arbitrary command execution or logic hijacking."
            ),
            "Unrestricted Access": (
                "Functions or variables without proper access controls can be abused, allowing unauthorized use."
            ),
            "Reentrancy": (
                "Reentrancy occurs when a function makes an external call before updating its state, "
                "allowing attackers to exploit the contract’s logic."
            ),
            "Overflow/Underflow": (
                "Unsigned integer operations can wrap around, causing unexpected behavior. "
                "Use safe math libraries or add boundary checks."
            ),
            "Use of system()": (
                "`system()` allows execution of shell commands. It is highly dangerous and should be avoided "
                "unless strictly sandboxed."
            ),
            "Function too large": (
                "Large functions are harder to understand, test, and secure. Split into smaller modules for better auditability."
            ),
            "Magic Numbers": (
                "Magic numbers make code hard to understand and maintain. Use named constants instead."
            ),
        }
        return explanations.get(vuln_type, f"No detailed explanation available for '{vuln_type}'.")

    def run(self):
        vulnerabilities = self.read_context("vulnerabilities", [])
        if not vulnerabilities:
            self.log("No vulnerabilities to explain.")
            return

        for vuln in vulnerabilities:
            vuln_type = vuln.get("type", "Unknown")
            if "details" not in vuln or not vuln["details"]:
                vuln["details"] = self.get_explanation(vuln_type)

        self.write_context("vulnerabilities", vulnerabilities)
        self.log(f"Added explanations to {len(vulnerabilities)} vulnerabilities.")
