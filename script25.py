import json
import os
from datetime import datetime

BOOKS_FILE = "books.json"


def load_books():
    if not os.path.exists(BOOKS_FILE):
        return []
    with open(BOOKS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_books(books):
    with open(BOOKS_FILE, "w", encoding="utf-8") as f:
        json.dump(books, f, ensure_ascii=False, indent=2)


def add_book():
    books = load_books()

    print("\n--- Добавление книги ---")
    author = input("Автор: ").strip()
    title = input("Название: ").strip()

    # Проверка на дубликаты (ИСПРАВЛЕНО)
    for book in books:
        if book["author"].lower() == author.lower() and book["title"].lower() == title.lower():
            print(" Такая книга уже есть!")
            return

    while True:
        try:
            rating = int(input("Оценка (1-5): "))
            if 1 <= rating <= 5:
                break
            print("Оценка должна быть от 1 до 5")
        except ValueError:
            print("Введите целое число")

    date = input("Дата прочтения (ГГГГ-ММ-ДД): ").strip()
    if not date:
        date = datetime.now().strftime("%Y-%m-%d")

    books.append({
        "author": author,
        "title": title,
        "rating": rating,
        "date": date
    })

    save_books(books)
    print(" Книга добавлена!")


def show_all_books():
    books = load_books()

    if not books:
        print("\n Нет добавленных книг")
        return

    print("\n--- Все книги ---")
    for i, book in enumerate(books, 1):
        print(f"{i}. {book['author']} — «{book['title']}»")
        print(f"   Оценка: {book['rating']}/5, Дата: {book['date']}\n")


def show_avg_rating():
    books = load_books()

    if not books:
        print("\n Нет книг для подсчёта")
        return

    total = sum(book["rating"] for book in books)
    avg = total / len(books)
    print(f"\n Средняя оценка: {avg:.2f} (на основе {len(books)} книг)")


def show_author_stats():
    books = load_books()

    if not books:
        print("\n📭 Нет книг для статистики")
        return

    stats = {}
    for book in books:
        author = book["author"]
        stats[author] = stats.get(author, 0) + 1

    print("\n--- Статистика по авторам ---")
    for author, count in sorted(stats.items()):
        print(f"{author}: {count} книг(и)")


def delete_book():
    books = load_books()

    if not books:
        print("\n Нет книг для удаления")
        return

    show_all_books()

    try:
        num = int(input("\nВведите номер книги для удаления: "))
        if 1 <= num <= len(books):
            removed = books.pop(num - 1)
            save_books(books)
            print(f"Удалена: {removed['author']} — «{removed['title']}»")
        else:
            print("Неверный номер")
    except ValueError:
        print("Введите число")


def main():
    while True:
        print("\n" + "=" * 40)
        print("ТРЕКЕР ПРОЧИТАННЫХ КНИГ")
        print("=" * 40)
        print("1. Добавить книгу")
        print("2. Показать все книги")
        print("3. Показать среднюю оценку")
        print("4. Статистика по авторам")
        print("5. Удалить книгу")
        print("6. Выход")

        choice = input("\nВыберите пункт: ").strip()

        if choice == "1":
            add_book()
        elif choice == "2":
            show_all_books()
        elif choice == "3":
            show_avg_rating()
        elif choice == "4":
            show_author_stats()
        elif choice == "5":
            delete_book()
        elif choice == "6":
            print("До свидания! ")
            break
        else:
            print("Неверный пункт, попробуйте снова")


if __name__ == "__main__":
    main()