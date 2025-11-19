# categorizer.py
import json
import os

class Categorizer:

    # Default built-in categories + keywords
    default_keywords = {
        "Politics": ["election", "minister", "government", "policy", "parliament", "vote", "president"],
        "Sports": ["match", "cricket", "football", "tournament", "goal", "team", "score"],
        "Technology": ["ai", "robot", "software", "tech", "device", "coding", "programming", "internet", "machine learning"],
        "Finance": ["stock", "market", "economy", "finance", "investment", "bank", "crypto", "inflation"],
        "Entertainment": ["movie", "film", "bollywood", "actor", "actress", "song", "series", "show"],
        "Education": ["school", "college", "university", "exam", "students", "learning"],
        "Health": ["virus", "covid", "disease", "hospital", "treatment", "doctor", "health"],
        "Science": ["research", "space", "nasa", "experiment", "biology", "physics", "astronomy"],
        "Travel": ["flight", "tourism", "trip", "hotel", "journey", "travel"],
        "Environment": ["climate", "pollution", "earth", "weather", "global warming"],
        "Crime": ["murder", "theft", "police", "arrest", "criminal", "scam"],
        "Business": ["startup", "company", "profit", "loss", "industry", "corporate"]
    }

    def __init__(self, json_file="categories.json"):
        self.json_file = json_file
        self.keywords = self.load_categories()

    # ------------------ Load categories.json + merge default ------------------
    def load_categories(self):
        # If no file, create one
        if not os.path.exists(self.json_file):
            with open(self.json_file, "w") as f:
                json.dump(self.default_keywords, f, indent=4)
            return dict(self.default_keywords)

        # Load file
        try:
            with open(self.json_file, "r") as f:
                saved = json.load(f)
        except:
            saved = {}

        # Merge default + saved (saved overwrites)
        merged = dict(self.default_keywords)
        merged.update(saved)
        return merged

    # ------------------ Save updated categories back to file ------------------
    def save_categories(self):
        with open(self.json_file, "w") as f:
            json.dump(self.keywords, f, indent=4)

    # ------------------ Category Matching (multi-category) -------------------
    def match_category(self, content):
        content = content.lower()
        matched = []

        # Check matches across all categories
        for category, words in self.keywords.items():
            if any(word in content for word in words):
                matched.append(category)

        # MULTIPLE MATCHES → return all
        if matched:
            print("\n✔ Matched categories:", ", ".join(matched))
            return matched

        # NO match → admin must create/select a category
        print("\n⚠ No category matched this article.")
        print("Available categories:")
        for c in self.keywords:
            print("•", c)

        while True:
            print("\n1) Choose existing category")
            print("2) Add NEW category")
            choice = input("Enter choice (1/2): ").strip()

            if choice == "1":
                selected = input("Enter category name: ").strip().title()
                if selected in self.keywords:
                    return [selected]
                print("Invalid category name.")

            elif choice == "2":
                new_cat = input("Enter NEW category name: ").strip().title()
                if new_cat:
                    self.keywords[new_cat] = []
                    self.save_categories()     # SAVE TO JSON
                    print(f"New category '{new_cat}' added & saved permanently!")
                    return [new_cat]
                else:
                    print("Empty name not allowed.")

            else:
                print("Invalid option.")

    # Optional: add keyword to category
    def add_keyword(self, category, keyword):
        keyword = keyword.lower()
        if category in self.keywords:
            self.keywords[category].append(keyword)
            self.save_categories()
            print(f"Keyword '{keyword}' added to '{category}' and saved.")
        else:
            print("Category does not exist.")
