# main.py
import os
from datetime import datetime

from article_manager import ArticleManager
from search_engine import SearchEngine
from display_manager import DisplayManager
from preprocessor import Preprocessor
from categorizer import Categorizer
from file_handler import FileHandler

# ---------------- PASSWORD SYSTEM ----------------
PASS_FILE = "admin_pass.txt"

def load_admin_password():
    if not os.path.exists(PASS_FILE):
        with open(PASS_FILE, "w") as f:
            f.write("admin123")  
        return "admin123"
    with open(PASS_FILE, "r") as f:
        return f.read().strip()

def save_admin_password(new_pass):
    with open(PASS_FILE, "w") as f:
        f.write(new_pass)


# ---------------- INITIALIZATION ----------------
manager = ArticleManager()
search = SearchEngine()
display = DisplayManager()
pre = Preprocessor()
cat = Categorizer("categories.json")
file = FileHandler()

manager.articles = file.load_from_file()
manager.restore_next_id()

display.type_text("📰 Welcome to the News Categorizer System!\n", speed=0.004)

mode = input("Login as (admin/user): ").strip().lower()
admin_password = load_admin_password()

# ---------------- ADMIN LOGIN ----------------
if mode == "admin":
    for attempt in range(3):
        pwd = input("Enter admin password: ").strip()
        if pwd == admin_password:
            print("Login Successful!")
            break
        else:
            print(f"Incorrect password ({2 - attempt} attempts left)")
    else:
        print("Too many failed attempts. Exiting.")
        exit()


# ---------------- USER PANEL ----------------
if mode == "user":
    while True:
        display.show_user_menu()
        ch = input("Enter choice: ").strip()

        # ---------- SEARCH ----------
        if ch == "1":
            key = input("Enter search keyword: ").strip()
            results = search.linear_search(manager.get_articles(), key)

            if not results:
                suggestions = search.suggest_similar_titles(manager.get_articles(), key)
                if suggestions:
                    print("\nDid you mean:")
                    for i, s in enumerate(suggestions, 1):
                        print(f"{i}. {s}")
                else:
                    print("No results.")
            else:
                display.display_article_list_numbered(results)
                try:
                    idx = int(input("\nEnter article number for full content (0 = skip): "))
                    if idx != 0:
                        article = results[idx - 1]
                        manager.increase_views(article)
                        file.save_to_file(manager.get_articles())
                        display.show_full_article(article)
                except:
                    print("Invalid selection.")

            input("\nPress Enter to continue...")

        # ---------- BROWSE CATEGORY ----------
        elif ch == "2":
            user_in = input("Enter categories (comma-separated): ")
            requested = [c.strip().title() for c in user_in.split(",")]

            all_cats = list(cat.keywords.keys())
            valid_cats = []

            for r in requested:
                if r in all_cats:
                    valid_cats.append(r)
                else:
                    sug = search.suggest_similar_categories(all_cats, r)
                    if sug:
                        print(f"Did you mean '{sug[0]}'?")
                        if input("Replace? (y/n): ").lower() == "y":
                            valid_cats.append(sug[0])
                    else:
                        print(f"⚠ Unknown category '{r}' ignored.")

            if not valid_cats:
                print("No valid categories.")
                input("\nPress Enter...")
                continue

            print("\nFilter Mode:")
            print("1) AND (match ALL)")
            print("2) OR (match ANY)")
            mode_choice = input("Choice: ")

            results = []
            if mode_choice == "1":
                results = [a for a in manager.get_articles() if all(c in a["category"] for c in valid_cats)]
            else:
                results = [a for a in manager.get_articles() if any(c in a["category"] for c in valid_cats)]

            display.display_article_list_numbered(results)

            if results:
                try:
                    idx = int(input("\nEnter article number (0 = skip): "))
                    if idx != 0:
                        article = results[idx - 1]
                        manager.increase_views(article)
                        file.save_to_file(manager.get_articles())
                        display.show_full_article(article)
                except:
                    print("Invalid selection.")

            input("\nPress Enter...")

        # ---------- PAGINATION ----------
        elif ch == "3":
            display.paginate_results(manager.get_articles())
            input("\nPress Enter...")

        # ---------- VIEW BY ID ----------
        elif ch == "4":
            try:
                aid = int(input("Enter Article ID: "))
            except:
                print("Invalid ID.")
                continue

            article = manager.get_by_id(aid)
            if not article:
                print("Article not found.")
            else:
                manager.increase_views(article)
                file.save_to_file(manager.get_articles())
                display.show_full_article(article)

            input("\nPress Enter...")

        # ---------- TRENDING ----------
        elif ch == "5":
            trending = manager.sort_by_views()
            print("\nTRENDING ARTICLES\n")
            display.display_article_list_numbered(trending)

            try:
                idx = int(input("\nEnter article number (0 = skip): "))
                if idx != 0:
                    article = trending[idx - 1]
                    manager.increase_views(article)
                    file.save_to_file(manager.get_articles())
                    display.show_full_article(article)
            except:
                print("Invalid choice.")

            input("\nPress Enter...")

        # ---------- LATEST ----------
        elif ch == "6":
            latest = manager.sort_by_date()
            print("\nLATEST ARTICLES\n")
            display.display_article_list_numbered(latest)

            try:
                idx = int(input("\nEnter article number (0 = skip): "))
                if idx != 0:
                    article = latest[idx - 1]
                    manager.increase_views(article)
                    file.save_to_file(manager.get_articles())
                    display.show_full_article(article)
            except:
                print("Invalid choice.")

            input("\nPress Enter...")

        # ---------- EXIT ----------
        elif ch == "7":
            print("Bye User!")
            break

        else:
            print("Invalid choice.")


# ---------------- ADMIN PANEL ----------------
elif mode == "admin":
    while True:
        display.show_admin_menu()
        ch = input("Enter choice: ").strip()

        # ---------- ADD ARTICLE ----------
        if ch == "1":
            title = input("Title: ")
            content = input("Content: ")
            date = datetime.now().strftime("%Y-%m-%d")

            print(f"Auto Date: {date}")

            try:
                views = int(input("Initial Views: "))
            except:
                views = 0

            processed = pre.clean_text(content)
            processed = pre.remove_stopwords(processed)
            categories = cat.match_category(processed)

            article = {
                "title": title,
                "content": content,
                "category": categories,
                "date": date,
                "views": views
            }

            manager.add_article(article)
            file.save_to_file(manager.get_articles())

        # ---------- DELETE ARTICLE ----------
        elif ch == "2":
            print("\nDelete by:")
            print("1) ID")
            print("2) Title")
            opt = input("Choice: ").strip()

            # -------- DELETE BY ID --------
            if opt == "1":
                try:
                    aid = int(input("Enter ID: "))
                except:
                    print("Invalid ID.")
                    continue

                article = manager.get_by_id(aid)
                if not article:
                    print("Article not found.")
                    continue

                print("\nFound Article:")
                display.show_full_article(article)

                confirm = input("⚠ Delete this article? (y/n): ")
                if confirm.lower() == "y":
                    manager.delete_by_id(aid)
                    file.save_to_file(manager.get_articles())
                    print("Deleted successfully!")
                else:
                    print("Cancelled.")

            # -------- DELETE BY TITLE --------
            elif opt == "2":
                name = input("Enter title: ").strip()

                exact = manager.find_exact_title(name)

                # ---- EXACT MATCH ----
                if len(exact) == 1:
                    article = exact[0]
                    display.show_full_article(article)

                    confirm = input("⚠ Delete this article? (y/n): ")
                    if confirm.lower() == "y":
                        manager.delete_by_id(article["id"])
                        file.save_to_file(manager.get_articles())
                        print("🗑 Deleted.")
                    else:
                        print("Cancelled.")

                # ---- MULTIPLE MATCHES ----
                elif len(exact) > 1:
                    print("\nMultiple articles found:")
                    display.display_title_choices(exact)

                    try:
                        aid = int(input("Enter ID: "))
                    except:
                        print("Invalid ID.")
                        continue

                    article = manager.get_by_id(aid)
                    display.show_full_article(article)

                    confirm = input("⚠ Delete this article? (y/n): ")
                    if confirm.lower() == "y":
                        manager.delete_by_id(aid)
                        file.save_to_file(manager.get_articles())
                        print("Deleted.")
                    else:
                        print("Cancelled.")

                # ---- NO EXACT MATCH → TRY FUZZY ----
                else:
                    suggestions = search.suggest_similar_titles(manager.get_articles(), name)
                    if not suggestions:
                        print("No similar titles found.")
                        continue

                    print("\nDid you mean:")
                    for i, s in enumerate(suggestions, 1):
                        print(f"{i}. {s}")

                    try:
                        sel = int(input("Select number (0 = cancel): "))
                    except:
                        print("Invalid choice.")
                        continue

                    if sel == 0:
                        print("Cancelled.")
                        continue

                    corrected_title = suggestions[sel - 1]
                    matches = manager.find_exact_title(corrected_title)

                    display.display_title_choices(matches)

                    try:
                        aid = int(input("Enter ID: "))
                    except:
                        print("Invalid ID.")
                        continue

                    article = manager.get_by_id(aid)
                    display.show_full_article(article)

                    confirm = input("⚠ Delete this article? (y/n): ")
                    if confirm.lower() == "y":
                        manager.delete_by_id(aid)
                        file.save_to_file(manager.get_articles())
                        print("Deleted!")
                    else:
                        print("Cancelled.")

        # ---------- VIEW ALL ----------
        elif ch == "3":
            display.display_article_list(manager.get_articles())
            input("\nPress Enter...")

        # ---------- EXIT ----------
        elif ch == "4":
            print("Logging out admin...")
            break

        # ---------- CHANGE PASSWORD ----------
        elif ch == "5":
            old = input("Enter OLD password: ").strip()
            if old != admin_password:
                print("Wrong password.")
                input("\nPress Enter...")
                continue

            new = input("Enter NEW password: ").strip()
            confirm = input("Confirm NEW password: ").strip()

            if new != confirm:
                print("Passwords do not match.")
                input("\nPress Enter...")
                continue

            save_admin_password(new)
            admin_password = new

            print("Password updated!")
            input("\nPress Enter...")

        else:
            print("Invalid option.")
