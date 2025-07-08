# Experimental , use for CLI 

# # main.py - 

# from agents.code_parser_agent import CodeParserAgent
# from agents.vuln_scanner_agent import VulnScannerAgent
# from agents.risk_assessor_agent import RiskAssessorAgent
# from agents.report_generator_agent import ReportGeneratorAgent
# from mcp.context import MemoryContext

# import sys

# def main(contract_path: str):
#     # Initialize shared context
#     context = MemoryContext()
#     context.write("contract_path", contract_path)

#     # Step 1: Parse code
#     parser = CodeParserAgent(context)
#     parser.run()

#     # Step 2: Scan vulnerabilities
#     scanner = VulnScannerAgent(context)
#     scanner.run()

#     # Step 3: Assess risk
#     assessor = RiskAssessorAgent(context)
#     assessor.run()

#     # Step 4: Generate report
#     reporter = ReportGeneratorAgent(context)
#     reporter.run()

#     print("\n✅ Audit completed. Check the /reports folder for output files.\n")

# if __name__ == "__main__":
#     if len(sys.argv) < 2:
#         print("Usage: python main.py contracts/sample_contract.cpp")
#     else:
#         contract_path = sys.argv[1]
#         main(contract_path)
