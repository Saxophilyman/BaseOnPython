# по сути в прошлом примере уже имелась композиция
# class BookStorage:
#     def __init__(self, capacity: int) -> None:
#         self.__capacity = capacity
#         self.__items: list[Book] = []

# чтобы сделать нагляднее можно добавить метод show_all_books
import math


# Первая иерархия
class Book:
    def __init__(self, title: str, author: str, pages: int, price: float) -> None:
        self.__title = title
        self.__author = author
        self.__pages = pages
        self.__price = price

    def info(self) -> str:
        return f"{self.__title} - {self.__author}, {self.__pages} pages, price = {self.__price}"

    def calculate_days_for_reading(self, pages_in_days: int) -> int:
        if pages_in_days <= 0:
            return 0
        return math.ceil(self.__pages / pages_in_days)


# потомок_1
class PaperBook(Book):
    def __init__(self, title: str, author: str, pages: int, price: float, cover: str) -> None:
        super().__init__(title, author, pages, price)
        self.__cover = cover
        self.__destruction = 0  # износ от 0 до 100

    def take_destroying_of_book(self, damage: int) -> None:
        if damage < 0:
            return  # возможно стоило бы использовать исключение, но требуется ли, если соблюдена в логика в данном случае?
        self.__destruction = min(100, self.__destruction + damage)

    def condition(self) -> str:
        if self.__destruction == 0:
            return "new"
        if self.__destruction < 30:
            return "good"
        if self.__destruction < 70:
            return "bad"
        return "very bad"
    # переопределим метод родителя
    def info(self) -> str:
        return f"Paper book: {super().info()}, cover = {self.__cover}"

# потомок 2
class EBook(Book):
    def __init__(self, title: str, author: str, pages: int, price: float, text: str, file_format: str,
                 file_size_mb: float) -> None:
        super().__init__(title, author, pages, price)
        self.__text = text
        self.__file_format = file_format
        self.__file_size_mb = file_size_mb

    def get_file_format(self) -> str:
        return self.__file_format

    def get_file_size_mb(self) -> float:
        return self.__file_size_mb
    # переопределим метод родителя
    def info(self) -> str:
        return f"EBook: {super().info()}, format = {self.__file_format}, size = {self.__file_size_mb} MB"

# Вторая иерархия
class BookStorage:
    def __init__(self, capacity: int) -> None:
        self.__capacity = capacity
        self.__items: list[Book] = []

    def add_book(self, book: Book) -> bool:
        if self.count() >= self.__capacity:
            return False
        self.__items.append(book)
        return True

    def count(self) -> int:
        return len(self.__items)

# новый метод
    def show_all_books(self) -> None:
        for book in self.__items:
            print(book.info())


class Bookshelf(BookStorage):
    def __init__(self, capacity: int) -> None:
        super().__init__(capacity)

    def organize_by_author(self) -> str:
        return "Bookshelf: organized by author"

    def organize_by_themes(self) -> str:
        return "Bookshelf: organized by themes"


class BookBag(BookStorage):
    def __init__(self, capacity: int, weight: float) -> None:
        super().__init__(capacity)
        self.__weight = weight
        self.__is_closed = False

    def close_bag(self) -> None:
        self.__is_closed = True

    def open_bag(self) -> None:
        self.__is_closed = False

    def add_book(self, book: Book) -> bool:
        if self.__is_closed:
            return False
        return super().add_book(book)


def main() -> None:
    paper = PaperBook("Дюна", "Фрэнк Герберт", 700, 1500.0, "твёрдая")
    ebook = EBook("Чистый код", "Роберт Мартин", 464, 900.0, "текст...", "epub", 2.3)

    shelf = Bookshelf(capacity=10)
    bag = BookBag(capacity=2, weight=0.8)

# Формально можно было бы проиллюстрировать так
    print("--- Композиция: шкаф содержит книги ---")
    shelf.add_book(paper)
    shelf.add_book(ebook)
    print("Количество книг в шкафу:", shelf.count())
    shelf.show_all_books()

    print("\n--- Композиция: сумка содержит книги ---")
    bag.open_bag()
    print("Добавляем книгу в открытую сумку:", bag.add_book(paper))
    print("Добавляем электронную книгу в открытую сумку:", bag.add_book(ebook))
    print("Количество книг в сумке:", bag.count())
    bag.show_all_books()
    # но говоря логически это не верно, потому что наша eBook является не носителем, а файлом
    print()

    animals: list[Animal] = []
    fill_animals(animals)

    for animal in animals:
        animal.foo()

# Функция, которая получает на вход список list[Animal]
import random

class Animal:
    def foo(self) -> None:
        pass

class Cat(Animal):
    def foo(self) -> None:
        print("Кошка мурлычет")

class Bird(Animal):
    def foo(self) -> None:
        print("Птица поет")

# учитываем "Не забывайте, что объекты обычным присваиванием не копируются."
def fill_animals(animals: list[Animal]) -> None:
    animals.clear()
    for _ in range(500):
        animal_class = random.choice([Cat, Bird])
        animals.append(animal_class())
# в списке animals лежат объекты двух разных потомков, а сам список является Animals
# работа с ними происходит через родительский тип, когда вызывается .foo()
# смотрится какой объект находится в реальной переменной (Кот или Птица)
# Вывод неупорядочен, потому что объекты потомков по сути перемешаны

if __name__ == "__main__":
    main()

# по примерам сейчас гораздо проще, в общем виде:
# Полиморфизми подтипов: когда у разных классов-потомков имеется общий родитель, а сами эти классы
# при переопределении метода подительского класса ведут себя по другому - в соответствии со своим переопределением.
# А вызов его по имени одинаков foo()
# Про параметрический полиморфизм :
# он работает с разными типами данных и заранее не знает что в неё передадут,
# но реализация для них одна.
# И здесь больше зависит от возможности операций над параметрами, которые будут ей переданы
