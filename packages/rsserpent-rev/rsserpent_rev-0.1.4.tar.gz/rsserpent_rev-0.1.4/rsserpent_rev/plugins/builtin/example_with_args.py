from typing import Any, Dict


path = "/_/example/{n:int}"


async def provider(n: int) -> Dict[str, Any]:
    """Define a example data provider function with arguments."""
    return {
        "title": "Example",
        "link": "https://example.com",
        "description": "An example rsserpent plugin.",
        "items": [
            {"title": f"Example Title {i}", "description": f"Example Description {i}"}
            for i in range(1, n + 1)
        ],
    }
