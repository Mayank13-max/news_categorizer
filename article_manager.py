# article_manager.py

class ArticleManager:

    def __init__(self):
        self.articles = []
        self.next_id = 1

    def restore_next_id(self):
        if not self.articles:
            self.next_id = 1
        else:
            self.next_id = max(a["id"] for a in self.articles) + 1

    def add_article(self, article):
        article["id"] = self.next_id
        self.next_id += 1
        self.articles.append(article)
        print("Article added!")

    def get_articles(self):
        return self.articles

    def get_by_id(self, aid):
        for a in self.articles:
            if a["id"] == aid:
                return a
        return None

    def delete_by_id(self, aid):
        for a in self.articles:
            if a["id"] == aid:
                self.articles.remove(a)
                print("🗑 Article removed.")
                return True
        print("Article not found.")
        return False

    def find_exact_title(self, title):
        return [a for a in self.articles if a["title"].lower() == title.lower()]

    # -------- VIEWS INCREMENT --------
    def increase_views(self, article):
        article["views"] += 1

    # -------- SORT BY VIEWS --------
    def sort_by_views(self):
        return sorted(self.articles, key=lambda x: x["views"], reverse=True)

    # -------- SORT BY DATE --------
    def sort_by_date(self):
        from datetime import datetime
        return sorted(
            self.articles,
            key=lambda x: datetime.strptime(x["date"], "%Y-%m-%d"),
            reverse=True
        )
