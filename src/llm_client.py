import os
from openai import OpenAI

class LLMClient:
    def __init__(self, api_key=None, base_url=None, model=None):
        # Initialize OpenAI client with environment variables or provided arguments
        # This works for OpenAI, DeepSeek, GitHub Models (Copilot), and local LLMs (Ollama)
        
        self.client = OpenAI(
            api_key=api_key or os.environ.get("OPENAI_API_KEY"),
            base_url=base_url or os.environ.get("OPENAI_BASE_URL")
        )
        # Default to gpt-5.4 if not specified in env or args
        self.model = model or os.environ.get("MODEL_NAME") or "gpt-5.4"
        print(f"Initialized LLMClient with model: {self.model} at {self.client.base_url}")

    def screen_paper(self, paper_title: str, paper_summary: str, criteria: str) -> dict:
        """
        Uses an LLM to screen a paper based on criteria.
        """
        prompt = f"""
        You are a research assistant. Please evaluate the following paper based on the selection criteria.
        
        Title: {paper_title}
        Summary: {paper_summary}
         
        Selection Criteria: {criteria}
        
        Please respond in the following format:
        Decision: [ACCEPT/REJECT]
        Reasoning: [Brief explanation]
        """

        try:
            response = self.client.chat.completions.create(
                model=self.model, 
                messages=[
                    {"role": "system", "content": "You are a helpful research assistant."},
                    {"role": "user", "content": prompt}
                ]
            )
            content = response.choices[0].message.content
            return {"raw_response": content}
        except Exception as e:
            return {"error": str(e)}
