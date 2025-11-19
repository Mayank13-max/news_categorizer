# display_manager.py
import os
import time
import textwrap

class DisplayManager:

    def clear_screen(self):
        os.system("cls" if os.name == "nt" else "clear")

    def type_text(self, text: str, speed: float = 0.002):
        for ch in text:
            print(ch, end="", flush=True)
            time.sleep(speed)
        print()

    # ============ USER MENU ===============
    def show_user_menu(self):
        self.clear_screen()
        menu = """
┌──────────────────────────────────────────────┐
│                 USER MENU                    │
├──────────────────────────────────────────────┤
│ 1. Search Articles                           │
│ 2. Browse by Category                        │
│ 3. Paginate Articles                         │
│ 4. View Full Article by ID                   │
│ 5. Trending Articles (Sort by Views)         │
│ 6. Latest Articles (Sort by Date)            │
│ 7. Exit                                      │
└──────────────────────────────────────────────┘
"""
        self.type_text(menu)

    # ============ ADMIN MENU ===============
    def show_admin_menu(self):
        self.clear_screen()
        menu = """
┌──────────────────────────────────────────────┐
│                 ADMIN MENU                   │
├──────────────────────────────────────────────┤
│ 1. Add Article                               │
│ 2. Delete Article                            │
│ 3. View All Articles                         │
│ 4. Exit                                      │
│ 5. Change Admin Password                     │
└──────────────────────────────────────────────┘
"""
        self.type_text(menu)

    # ============ WRAPPED ARTICLE LIST ===============
    def display_article_list(self, article_list):
        if not article_list:
            print("📭 No articles.\n")
            return

        max_width = 50

        for a in article_list:
            cats = ", ".join(a["category"])

            title_lines = textwrap.wrap(a["title"], max_width)
            cat_lines = textwrap.wrap(cats, max_width)

            box_width = max_width + 2

            print("┌" + "─" * box_width + "┐")
            print(f"│ ID: {a['id']}".ljust(box_width + 1) + "│")

            print("│ Title:".ljust(box_width + 1) + "│")
            for line in title_lines:
                print(f"│ {line}".ljust(box_width + 1) + "│")

            print("│ Categories:".ljust(box_width + 1) + "│")
            for line in cat_lines:
                print(f"│ {line}".ljust(box_width + 1) + "│")

            print(f"│ Date: {a['date']}".ljust(box_width + 1) + "│")
            print(f"│ Views: {a['views']}".ljust(box_width + 1) + "│")
            print("└" + "─" * box_width + "┘\n")

    # ============ NUMBERED ARTICLE LIST ===============
    def display_article_list_numbered(self, article_list):
        if not article_list:
            print("📭 No articles.\n")
            return

        for i, a in enumerate(article_list, 1):
            cats = ", ".join(a["category"])
            print(f"{i}. {a['title']} ({cats})")

    # ============ FULL ARTICLE VIEW ===============
    def show_full_article(self, article):
        cats = ", ".join(article["category"])
        max_width = 70

        content_lines = textwrap.wrap(article["content"], max_width)
        title_lines = textwrap.wrap(article["title"], max_width)
        cat_lines = textwrap.wrap(cats, max_width)

        print("=" * 80)
        print("FULL ARTICLE".center(80))
        print("=" * 80)

        print("\nID:", article["id"])
        print("Title:")
        for line in title_lines:
            print(" ", line)

        print("\nCategories:")
        for line in cat_lines:
            print(" ", line)

        print("\nDate:", article["date"])
        print("Views:", article["views"])

        print("\nCONTENT:\n")
        for line in content_lines:
            print(line)

        print("\n" + "=" * 80 + "\n")

    # ============ PAGINATION ===============
    def paginate_results(self, articles, per_page=3):
        total = len(articles)
        if total == 0:
            print("📭 No articles.")
            return

        pages = (total + per_page - 1) // per_page

        for p in range(1, pages + 1):
            self.clear_screen()
            print(f"--- Page {p}/{pages} ---\n")

            start = (p - 1) * per_page
            end = start + per_page
            self.display_article_list(articles[start:end])

            if p < pages:
                nxt = input("Next page? (y/n): ").lower()
                if nxt != "y":
                    break

        input("\nPress Enter to continue...")
