from mcp.base_agent import Context
from agents.code_parser_agent import CodeParserAgent
from agents.vuln_scanner_agent import VulnerabilityScannerAgent
from agents.risk_assessor_agent import RiskAssessorAgent
from agents.report_generator_agent import ReportGeneratorAgent

def main():
    code = "# Sample C++ smart contract code..."
    context = Context()

    parser = CodeParserAgent(context)
    parser.parse(code)

    scanner = VulnerabilityScannerAgent(context)
    scanner.scan()

    assessor = RiskAssessorAgent(context)
    assessor.assess()

    reporter = ReportGeneratorAgent(context)
    report = reporter.generate()

    print("Audit Report:", report)

if __name__ == "__main__":
    main()