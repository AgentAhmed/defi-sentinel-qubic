from agents.base_agent import BaseAgent
from mcp.context import MemoryContext
import os
import json
import requests

from dotenv import load_dotenv

load_dotenv()

class ChatbotAgent(BaseAgent):
    def __init__(self, context: MemoryContext):
        super().__init__("ChatbotAgent", context)
        self.groq_api_key = os.getenv("GROQ_API_KEY")  # Add to .env or OS

    def _query_context(self, question: str) -> str:
        # Quick local knowledge from context
        raw_code = self.context.get("raw_code") or ""
        issues = self.context.get("explainable_vulnerabilities", [])
        loc = len(raw_code.strip().splitlines())

        if "issue" in question.lower():
            return f"There are {len(issues)} explainable vulnerabilities detected in this contract."
        if "line" in question.lower() or "code" in question.lower():
            return f"The contract has {loc} lines of C++ code."
        if "functions" in question.lower():
            funcs = self.context.get("functions", [])
            return f"{len(funcs)} functions detected. Example: {funcs[0] if funcs else 'N/A'}"
        return None  # Fallback to Groq

    def _query_groq(self, question: str) -> str:
        if not self.groq_api_key:
            return "Groq API key not configured. Please set GROQ_API_KEY."

        headers = {
            "Authorization": f"Bearer {self.groq_api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "llama3-70b-8192",
            "messages": [
                {"role": "system", "content": "You are an AI assistant helping analyze C++ smart contracts on the Qubic blockchain."},
                {"role": "user", "content": question}
            ]
        }

        response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload)

        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return f"[Groq Error] {response.status_code}: {response.text}"

    def run(self, question: str):
        local_reply = self._query_context(question)
        if local_reply:
            return local_reply
        else:
            print("[ChatbotAgent] Falling back to Groq...")
            return self._query_groq(question)
