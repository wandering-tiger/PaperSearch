import sys
import os

# Add the src directory to the python path so imports work when running from root
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
from arxiv_client import ArxivClient
from llm_client import LLMClient

# Load environment variables
load_dotenv()

def main():
    # 1. Configuration
    query = "large language models survey"
    criteria = "Must focus on survey or review of Large Language Models, specifically covering architecture or reasoning capabilities."
    max_results = 5

    print(f"Searching for papers with query: '{query}'...")
    
    # 2. Search Arxiv
    arxiv_client = ArxivClient()
    papers = arxiv_client.search_papers(query, max_results=max_results)
    print(f"Found {len(papers)} papers.")

    # 3. Screen with LLM
    # Note: Requires OPENAI_API_KEY environment variable set in .env file
    llm_client = LLMClient()
    
    print("\nStarting screening process...\n")
    
    for paper in papers:
        print(f"--- Screening: {paper['title']} ---")
        result = llm_client.screen_paper(paper['title'], paper['summary'], criteria)
        
        if "error" in result:
            print(f"Error calling LLM: {result['error']}")
        else:
            print(f"LLM Response:\n{result['raw_response']}\n")

if __name__ == "__main__":
    main()
