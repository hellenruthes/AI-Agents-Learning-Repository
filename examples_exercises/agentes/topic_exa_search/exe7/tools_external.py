import os
from dotenv import load_dotenv
from exa_py import Exa

load_dotenv()

EXA_API_KEY = os.getenv("EXA_API_KEY")


def get_exa_client():
    if not EXA_API_KEY:
        raise ValueError("EXA_API_KEY not defined in environment")
    return Exa(EXA_API_KEY)


def search_external(query: str, num_results: int = 5) -> list[dict]:
    """
    Search external data using Exa AI
    """
    exa = get_exa_client()

    response = exa.search_and_contents(
        query,
        num_results=num_results,
        text=True
    )

    results = []

    for item in response.results:
        results.append({
            "source": "external",
            "title": item.title,
            "text": item.text[:500] if item.text else "",  # limit size
            "url": item.url,
        })

    return results


def filter_external_results(results: list[dict], keyword: str) -> list[dict]:
    keyword_lower = keyword.lower()

    return [
        item for item in results
        if keyword_lower in item["title"].lower()
        or keyword_lower in item["text"].lower()
    ]


def summarize_external_results(results: list[dict]) -> str:
    """
    Create a summary of external results
    """
    if not results:
        return "No results found"
    
    summary_lines = [f"Total results: {len(results)}\n"]
    
    for i, item in enumerate(results, 1):
        summary_lines.append(f"{i}. {item['title']}")
        summary_lines.append(f"   URL: {item['url']}")
        summary_lines.append(f"   Preview: {item['text'][:100]}...")
        summary_lines.append("")
    
    return "\n".join(summary_lines)