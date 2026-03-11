import os
from openai import OpenAI

class LLMClient:
    def __init__(self, api_key=None, base_url=None):
        # GitHub Copilot currently does not provide a public REST API for direct usage in scripts 
        # like this. However, you can use the OpenAI API format which is standard.
        # You can use an OpenAI Key, or a local model (like Ollama, LM Studio) that provides
        # an OpenAI-compatible endpoint.
        
        self.client = OpenAI(
            api_key=api_key or os.environ.get("OPENAI_API_KEY"),
            base_url=base_url or os.environ.get("OPENAI_BASE_URL")
        )

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
                model="gpt-4o-mini", # Or any other model available to your API key
                messages=[
                    {"role": "system", "content": "You are a helpful research assistant."},
                    {"role": "user", "content": prompt}
                ]
            )
            content = response.choices[0].message.content
            return {"raw_response": content}
        except Exception as e:
            return {"error": str(e)}
