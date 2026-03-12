import sys
import os
import datetime
# Add the src directory to the python path so imports work when running from root
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
from arxiv_client import ArxivClient
from llm_client import LLMClient
from openai import OpenAI
import arxiv # Import arxiv explicitly for SortCriterion

# Load environment variables
load_dotenv()

def generate_report(papers, filename="accepted_papers.md"):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"# Paper Search Report\n\n")
        f.write(f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"---\n\n")
        
        for i, paper in enumerate(papers, 1):
            title = paper['title']
            authors = ', '.join(paper['authors'])
            published = paper['published']
            link = paper['pdf_url']
            summary = paper['summary'].replace('\n', ' ')
            
            f.write(f"## {i}. {title}\n\n")
            f.write(f"**Authors:** {authors}\n\n")
            f.write(f"**Published:** {published}\n\n")
            f.write(f"**Link:** [PDF]({link})\n\n")
            f.write(f"**Summary:**\n> {summary}\n\n")
            
            # Extract reasoning/decision from raw response if not parsed
            # For simplicity, assuming 'llm_reasoning' contains the raw text
            if 'llm_reasoning' in paper:
                f.write(f"**AI Evaluation:**\n{paper['llm_reasoning']}\n\n")
            
            f.write(f"---\n\n")

def main():
    # 1. Configuration - Interactive Input
    print("Welcome to PaperSearch!")
    
    # Get keywords
    default_query = "large language models survey"
    query = input(f"Enter search keywords (default: '{default_query}'): ").strip()
    if not query:
        query = default_query
        
    # Get criteria
    default_criteria = "Select detailed and comprehensive survey papers."
    criteria = input(f"Enter screening criteria (default: '{default_criteria}'): ").strip()
    if not criteria:
        criteria = default_criteria

    # Get search settings
    sort_option = input("Sort by (1) Relevance or (2) Submission Date? (default: 1): ").strip()
    year_filter = None
    
    if sort_option == "2":
        sort_by = arxiv.SortCriterion.SubmittedDate
        sort_name = "SubmittedDate"
    else:
        sort_by = arxiv.SortCriterion.Relevance
        sort_name = "Relevance"
        
        # Ask for year filter only when sorting by relevance
        use_year_filter = input("Do you want to filter out older papers? (y/n, default: n): ").lower().strip()
        if use_year_filter == 'y':
            try:
                year_input = input("Enter the starting year (e.g. 2023): ").strip()
                if year_input:
                    year_filter = int(year_input)
            except ValueError:
                print("Invalid year. Skipping time filter.")
        
    # Get counts
    try:
        max_search_candidates = int(input("How many papers to scan from Arxiv initially? (default: 50): ").strip() or "50")
    except ValueError:
        max_search_candidates = 50
        
    try:
        target_papers = int(input("How many approved papers do you want? (default: 10): ").strip() or "10")
    except ValueError:
        target_papers = 10

    # 2. Search Arxiv
    print(f"\nSearching Arxiv for '{query}' (fetching up to {max_search_candidates} candidates, sorted by {sort_name})...")
    arxiv_client = ArxivClient()
    # Note: Arxiv search sorts by relevance now
    candidates = arxiv_client.search_papers(query, max_results=max_search_candidates, sort_by=sort_by)
    print(f"Found {len(candidates)} candidates.")

    # 3. Screen with LLM
    print(f"\nStarting screening process...")
    
    # Initialize unified LLM client - it will use config from .env
    llm_client = LLMClient()
    
    screened_positive = []
    
    for i, paper in enumerate(candidates):
        # Stop if we have enough approved papers
        if len(screened_positive) >= target_papers:
            break
            
        # Time filtering logic
        if year_filter:
            try:
                # published format is usually "YYYY-MM-DD"
                pub_year = int(paper['published'].split('-')[0])
                if pub_year < year_filter:
                    # Skip silently or with minimal log if desired
                    # print(f"  Skipping {paper['title'][:30]}... (Published {pub_year} < {year_filter})")
                    continue
            except Exception:
                pass # If date parsing fails, we include it to be safe
            
        print(f"[{i+1}/{len(candidates)}] Screening: {paper['title'][:60]}...")
        
        # Call LLM
        result = llm_client.screen_paper(paper['title'], paper['summary'], criteria)
        
        if "error" in result:
            print(f"  > Error: {result['error']}")
            continue
            
        response_text = result['raw_response']
        
        # Simple Logic to check if ACCEPTED
        # We look for "Decision: ACCEPT" (case insensitive usually good, but prompt asks for uppercase)
        is_accepted = "Decision: ACCEPT" in response_text
        
        if is_accepted:
            print(f"  > ACCEPTED!")
            paper['llm_decision'] = "ACCEPT"
            paper['llm_reasoning'] = response_text
            screened_positive.append(paper)
        else:
            print(f"  > REJECTED.")
    
    # 4. Generate Markdown Report
    if screened_positive:
        output_file = "accepted_papers.md"
        generate_report(screened_positive, output_file)
        print(f"\nSuccess! Report generated: {output_file}")
        print(f"Contains {len(screened_positive)} papers.")
    else:
        print("\nNo papers matched your criteria.")

if __name__ == "__main__":
    main()
