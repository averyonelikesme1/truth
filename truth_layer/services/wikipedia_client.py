import wikipedia


class WikipediaClient:

    def search_claim(self, claim: str):

        try:

            results = wikipedia.search(
                claim,
                results=5
            )

            evidence = []

            for result in results:

                try:

                    page = wikipedia.page(
                        result,
                        auto_suggest=False
                    )

                    evidence.append(
                        {
                            "title": page.title,
                            "url": page.url,
                            "content": page.summary
                        }
                    )

                except Exception:
                    continue

            return evidence

        except Exception:
            return []