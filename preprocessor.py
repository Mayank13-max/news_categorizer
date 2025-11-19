class Preprocessor:
    stopwords = {"the", "is", "and", "a", "an", "in", "on", "of", "to", "for", "with", "by"}

    def clean_text(self, text: str) -> str:
        text = text.lower()
        text = "".join(c for c in text if c.isalnum() or c.isspace())
        return text

    def remove_stopwords(self, text: str) -> str:
        return " ".join(word for word in text.split() if word not in self.stopwords)

    def tokenize(self, text: str):
        return text.split()
