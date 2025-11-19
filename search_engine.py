# search_engine.py
class SearchEngine:

    def linear_search(self, articles, keyword: str):
        keyword = keyword.lower()
        return [
            a for a in articles
            if keyword in a["title"].lower() or keyword in a["content"].lower()
        ]

    def levenshtein(self, a: str, b: str) -> int:
        dp = [[i + j if i * j == 0 else 0 for j in range(len(b) + 1)] for i in range(len(a) + 1)]
        for i in range(1, len(a) + 1):
            for j in range(1, len(b) + 1):
                dp[i][j] = min(
                    dp[i-1][j] + 1,
                    dp[i][j-1] + 1,
                    dp[i-1][j-1] + (0 if a[i-1] == b[j-1] else 1)
                )
        return dp[-1][-1]

    def suggest_similar_titles(self, articles, wrong_title: str, threshold: int = 3):
        wrong_title = wrong_title.lower()
        suggestions = []
        for a in articles:
            dist = self.levenshtein(wrong_title, a["title"].lower())
            if dist <= threshold:
                suggestions.append((a["title"], dist))
        suggestions.sort(key=lambda x: x[1])
        return [s[0] for s in suggestions]

    def suggest_similar_categories(self, category_names, wrong_category: str, threshold: int = 3):
        wrong_category = wrong_category.lower()
        suggestions = []
        for c in category_names:
            dist = self.levenshtein(wrong_category, c.lower())
            if dist <= threshold:
                suggestions.append((c, dist))
        suggestions.sort(key=lambda x: x[1])
        return [s[0] for s in suggestions]
