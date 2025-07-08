import re
from agents.base_agent import BaseAgent

class VulnScannerAgent(BaseAgent):
    def __init__(self, context):
        super().__init__("VulnScannerAgent", context)

    def run(self):
        code = self.read_context("contract_code")
        if not code:
            self.log("No contract code found.")
            return

        vulnerabilities = []

        # === 1. Unsafe system call ===
        if "system(" in code:
            vulnerabilities.append({
                "type": "Use of system() call",
                "description": "Use of system() allows arbitrary command execution. Avoid using it in smart contracts.",
                "confidence": "High",
                "location": "system()",
                "lines_affected": self._count_lines(code, "system(")
            })

        # === 2. Hardcoded secrets or keys ===
        if re.search(r'(\".*(key|password|secret).*\"|\'.*(key|password|secret).*\')', code, re.IGNORECASE):
            vulnerabilities.append({
                "type": "Hardcoded secret or key",
                "description": "Sensitive data like secrets or API keys should not be hardcoded.",
                "confidence": "High",
                "location": "string literals",
                "lines_affected": self._count_lines(code, "key")
            })

        # === 3. Integer overflow/underflow (no checks) ===
        arithmetic_ops = re.findall(r'(\w+\s*[\+\-\*\/]=?\s*\w+)', code)
        for op in arithmetic_ops:
            if not re.search(r'(assert|require|if\s*\()', op):  # naive check for guards
                vulnerabilities.append({
                    "type": "Unchecked arithmetic operation",
                    "description": f"Operation '{op.strip()}' might cause overflow/underflow. Consider using safe math checks.",
                    "confidence": "Medium",
                    "location": op.strip(),
                    "lines_affected": self._count_lines(code, op.strip())
                })

        # === 4. Large function blocks ===
        functions = re.findall(r'[\w\s]+[\*&]*\s+\w+\s*\([^\)]*\)\s*\{[^{}]*\}', code, re.DOTALL)
        for func in functions:
            lines = func.count("\n")
            if lines > 25:
                vulnerabilities.append({
                    "type": "Function too large",
                    "description": "Functions longer than 25 lines are harder to audit and more error-prone.",
                    "confidence": "Low",
                    "location": func.split("\n")[0].strip(),
                    "lines_affected": lines
                })

        # === 5. Dangerous casting ===
        if re.search(r'\(char\*\)\s*\w+', code):
            vulnerabilities.append({
                "type": "Dangerous casting",
                "description": "Casting to raw pointers like (char*) can lead to memory corruption.",
                "confidence": "Medium",
                "location": "(char*)",
                "lines_affected": self._count_lines(code, "(char*)")
            })

        # === 6. No validation for transfer handler ===
        if "onTransfer" in code and not re.search(r'(require|assert|if\s*\()', code):
            vulnerabilities.append({
                "type": "Missing validation in onTransfer",
                "description": "onTransfer() should validate sender and amount to prevent exploit.",
                "confidence": "High",
                "location": "onTransfer",
                "lines_affected": self._count_lines(code, "onTransfer")
            })

        self.write_context("vulnerabilities", vulnerabilities)
        self.log(f"Issues detected: {[v['type'] for v in vulnerabilities]}")

    def _count_lines(self, code, keyword):
        """Return number of lines containing the keyword (naive but fast)"""
        return sum(1 for line in code.splitlines() if keyword in line)
