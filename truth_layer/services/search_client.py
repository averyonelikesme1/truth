from duckduckgo_search import DDGS


class SearchClient:

    def search(self, query: str):

        results = []

        with DDGS() as ddgs:

            search_results = ddgs.text(
                query,
                max_results=5
            )

            for item in search_results:

                results.append(
                    {
                        "title": item.get("title"),
                        "url": item.get("href"),
                        "content": item.get("body")
                    }
                )

        return results