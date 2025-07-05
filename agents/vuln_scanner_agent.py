from agents.base_agent import BaseAgent
from mcp.context import MemoryContext

import re

class VulnScannerAgent(BaseAgent):
    def __init__(self, context: MemoryContext):
        super().__init__("VulnScannerAgent", context)

    def run(self):
        code = self.read_context("parsed_code") or self.read_context("raw_code")
        if not code:
            raise ValueError("No code found in context to scan.")

        issues = []

        # Rule 1: Check for missing input validation
        if re.search(r"\b(int|float|char|bool|string)\s+\w+\s*\(.*\)", code):
            if not re.search(r"if\s*\(.*\)\s*{", code):
                issues.append("Potential lack of input validation.")

        # Rule 2: Check for use of raw pointers
        if re.search(r"\*\s*\w+", code):
            issues.append("Possible unsafe pointer usage.")

        # Rule 3: Detect hardcoded values or secrets
        if re.search(r"\s*=\s*\".*\"", code):
            issues.append("Hardcoded value or potential secret found.")

        # Rule 4: Detect large functions (complexity risk)
        function_defs = re.findall(r"\bvoid\s+\w+\s*\(.*\)\s*\{.*?\n\}", code, re.DOTALL)
        for f in function_defs:
            if len(f.splitlines()) > 50:
                issues.append("Function too large: consider splitting into smaller functions.")

        # Rule 5: Check for unchecked external calls (e.g., system())
        if "system(" in code:
            issues.append("Use of system() call: potential security risk.")

        self.write_context("vulnerability_issues", issues)
        self.log(f"Issues detected: {issues}")
        return issues
