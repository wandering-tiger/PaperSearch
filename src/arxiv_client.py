import arxiv
from typing import List, Dict

class ArxivClient:
    def __init__(self):
        self.client = arxiv.Client()

    def search_papers(self, query: str, max_results: int = 50, sort_by=arxiv.SortCriterion.Relevance) -> List[Dict]:
        """
        Search for papers on Arxiv.
        """
        search = arxiv.Search(
            query=query,
            max_results=max_results,
            sort_by=sort_by
        )

        results = []
        for result in self.client.results(search):
            results.append({
                "title": result.title,
                "authors": [author.name for author in result.authors],
                "summary": result.summary,
                "pdf_url": result.pdf_url,
                "published": result.published.strftime("%Y-%m-%d"),
                "entry_id": result.entry_id
            })
        return results
