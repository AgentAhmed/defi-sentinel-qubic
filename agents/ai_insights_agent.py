from agents.base_agent import BaseAgent

class AIInsightsAgent(BaseAgent):
    def __init__(self, context, llm=None):
        super().__init__("AIInsightsAgent", context)
        self.llm = llm

    def run(self):
        vulnerabilities = self.read_context("vulnerabilities", [])
        contract_name = self.read_context("contract_name", "Unknown")

        if not self.llm:
            self.write_context("ai_analysis", "⚠️ AI assistant is not connected.")
            return

        if not vulnerabilities:
            self.write_context("ai_analysis", "✅ No vulnerabilities found. No AI analysis required.")
            return

        prompt = (
            f"You are a smart contract security expert.\n\n"
            f"Contract Name: {contract_name}\n"
            f"Detected Vulnerabilities:\n{vulnerabilities}\n\n"
            f"Provide a professional audit summary explaining severity, impact, potential exploit paths, "
            f"and mitigation strategies for each vulnerability. Include advice suitable for a developer."
        )

        try:
            response = self.llm(prompt)
            if not response.strip():
                self.write_context("ai_analysis", "⚠️ AI did not return a response.")
            else:
                self.write_context("ai_analysis", response.strip())
        except Exception as e:
            self.write_context("ai_analysis", f"⚠️ AI analysis unavailable due to error: {str(e)}")
