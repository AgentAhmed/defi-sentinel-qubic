from agents.base_agent import BaseAgent
import re

class CodeParserAgent(BaseAgent):
    def __init__(self, context):
        super().__init__("CodeParserAgent", context)

    def extract_functions(self, code):
        pattern = re.compile(r"(?:[\w:<>]+\s+)+(\w+)\s*\([^;]*\)\s*\{?")
        lines = code.splitlines()
        function_defs = []
        for idx, line in enumerate(lines):
            match = pattern.search(line)
            if match:
                function_defs.append({
                    "name": match.group(1),
                    "line": idx + 1,
                    "code": line.strip()
                })
        return function_defs

    def extract_contracts(self, code):
        contract_pattern = re.compile(r"CONTRACT\s+(\w+)")
        return contract_pattern.findall(code)

    def extract_comments(self, code):
        comments = []
        lines = code.splitlines()
        for i, line in enumerate(lines):
            if "//" in line or "/*" in line:
                comments.append({"line": i + 1, "comment": line.strip()})
        return comments

    def run(self):
        path = self.read_context("contract_path")
        with open(path, "r", encoding="utf-8") as f:
            code = f.read()

        function_defs = self.extract_functions(code)
        comments = self.extract_comments(code)
        contracts = self.extract_contracts(code)

        parsed_info = {
            "functions": function_defs,
            "comments": comments,
            "loc": len(code.splitlines()),
            "contracts": contracts
        }

        self.write_context("parsed_info", parsed_info)
        self.write_context("contract_code", code)
        self.log(f"Parsed {len(function_defs)} functions, {len(comments)} comments, "
                 f"{len(code.splitlines())} lines of code.")
