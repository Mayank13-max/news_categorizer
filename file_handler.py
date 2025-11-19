# file_handler.py
import os

class FileHandler:
    def __init__(self, filename="articles.txt"):
        self.filename = filename

    def save_to_file(self, articles):
        with open(self.filename, "w", encoding="utf-8") as f:
            for a in articles:
                cats = ",".join(a.get("category", [])) if isinstance(a.get("category"), (list,tuple)) else str(a.get("category"))
                # replace newlines to keep one-line-per-article
                content = a.get("content","").replace("\n"," ")
                f.write(f"{a['id']}|{a['title']}|{content}|{cats}|{a['date']}|{a['views']}\n")

    def load_from_file(self):
        if not os.path.exists(self.filename):
            return []
        articles = []
        with open(self.filename, "r", encoding="utf-8") as f:
            for line in f:
                d = line.strip().split("|")
                if len(d) == 6:
                    cats = d[3].split(",") if d[3] else []
                    articles.append({
                        "id": int(d[0]),
                        "title": d[1],
                        "content": d[2],
                        "category": cats,
                        "date": d[4],
                        "views": int(d[5])
                    })
        return articles
