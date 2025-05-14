import json
import logging
import os
from tavily import TavilyClient
from .tool import Tool

MAX_RESULTS = 2
TAVILY_API_KEY = "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"

logger = logging.getLogger(__name__)


client = TavilyClient(TAVILY_API_KEY)


class TavilySearchTool(Tool):
    def __init__(self):
        super().__init__("search", "Useful for searching the web for information.")
        self.client = TavilyClient(TAVILY_API_KEY)

    def clean_results(self, response):
        results = response["results"]
        clean_results = []
        for result in results:
            clean_result = {}
            clean_result["title"] = result["title"]
            clean_result["url"] = result["url"]
            clean_result["content"] = result["content"]
            clean_result["score"] = result["score"]
            if result["raw_content"]:
                clean_result["raw_content"] = result["raw_content"]
            clean_results.append(clean_result)
        return clean_results

    def __call__(self, query: str) -> str:
        print(f"Searching for:\n {query}")
        response = self.client.search(query=query, max_results=MAX_RESULTS)
        print(f"Search Response:\n {response}")
        clean_results = self.clean_results(response)
        return ";".join(str(result) for result in clean_results)


if __name__ == "__main__":
    tavily_search_tool = TavilySearchTool()
    results = tavily_search_tool("current height of the Eiffel Tower in 2025")
    print(type(results))
    print(results)
