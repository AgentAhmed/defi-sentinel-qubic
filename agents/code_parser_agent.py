from agents.base_agent import BaseAgent
from mcp.context import MemoryContext

import re
import os

class CodeParserAgent(BaseAgent):
    def __init__(self, context: MemoryContext):
        super().__init__("CodeParserAgent", context)

    def run(self):
        contract_path = self.read_context("contract_path")
        if not contract_path or not os.path.isfile(contract_path):
            raise FileNotFoundError("Smart contract path not found or invalid.")

        with open(contract_path, "r") as file:
            code = file.read()

        # Basic C++ function extraction
        functions = re.findall(r'(?:\w+\s+)+\w+\s*\([^)]*\)\s*\{', code)
        comments = re.findall(r'\/\/.*|\/\*[\s\S]*?\*\/', code)
        loc = len(code.strip().splitlines())

        self.write_context("functions", functions)
        self.write_context("comments", comments)
        self.write_context("lines_of_code", loc)
        self.write_context("raw_code", code)

        self.log("Parsed functions, comments, and LOC.")
