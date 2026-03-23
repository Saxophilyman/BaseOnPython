# После долгого перерыва, моя задача "Вспомнить всё"
# Всё также присутствуют сложности с синтаксисом языка, что отнимает значительную часть времени
# 5.1. Разделите видимость полей (сделайте все поля приватными) и методов во всех классах вашей программы.
# Казалось бы здесь всё достаточно просто и понятно, но пришлось разобраться с нюансами handling и инициализацией через конструктор
# добавил небольшие инварианты

from dataclasses import dataclass

type Coord = tuple[float, float]


# Максимальное упрощение
class Hero:
    __name: str
    __hero_class: str
    __level: int
    __hp: int
    __speed: float
    __greed: int
    __max_prize_distance: float
    __pos_hero_coord: Coord

    # контруктор
    def __init__(self, name: str, hero_class: str, level: int, hp: int, speed: float, greed: int,
                 max_prize_distance: float, pos_hero_coord: Coord) -> None:
        self.__name = name
        self.__hero_class = hero_class
        self.__level = level
        self.__hp = hp
        self.__speed = speed
        self.__greed = greed
        self.__max_prize_distance = max_prize_distance
        self.__pos_hero_coord = pos_hero_coord

    #   геттер
    def get_hp(self) -> int:
        return self.__hp

    # три метода
    def is_alive(self) -> bool:
        return self.__hp > 0

    def take_damage(self, damage: int) -> None:
        if damage < 0:
            raise ValueError("damage must be >= 0")
        self.__hp = max(0, self.__hp - damage)

    def heal(self, heal_count: int) -> None:
        if heal_count < 0:
            raise ValueError("heal_count must be >= 0")
        self.__hp += heal_count


class Building:
    # узнал, что без полей, можно сразу, через инициализацию создавать атрибуты
    # контруктор
    def __init__(self, name: str, building_type: str, level: int, hp: int, income_per_day: int, last_day_by_income: int,
                 pos_building_coord: Coord) -> None:
        self.__name = name
        self.__building_type = building_type
        self.__level = level
        self.__hp = hp
        self.__income_per_day = income_per_day
        self.__last_day_by_income = last_day_by_income
        self.__pos_building_coord = pos_building_coord
        self.__destroyed = False

    # три метода
    def building_upgrade(self) -> None:
        if self.__destroyed:
            return
        self.__level += 1
        self.__income_per_day += 10

    def collect_income(self, current_day: int) -> int:
        if self.__destroyed:
            return 0
        days_for_income = current_day - self.__last_day_by_income
        if days_for_income <= 0:
            return 0
        self.__last_day_by_income = current_day
        return self.__income_per_day * days_for_income

    def destroy(self) -> None:
        self.__destroyed = True
        self.__hp = 0
        self.__income_per_day = 0


# Постройте две небольшие и косвенно логически связанные иерархии классов в вашей программе
# У родительского класса в каждой иерархии должно быть не менее двух наследников.
# В каждом дочернем классе должно быть не менее двух оригинальных методов, характеризующих уникальность этих классов, их отличие от родительского.

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


# Вторая иерархия, т.к. они должны быть косвенно связаны можно подумать о таком:

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

    print("Книги")
    print(paper.info())
    print("Сколько займёт дней (50 страниц в день):", paper.calculate_days_for_reading(50))
    paper.take_destroying_of_book(35)
    print("Состояние книги:", paper.condition())

    print(ebook.info())
    print("Формат электронной книги:", ebook.get_file_format())
    print("Сколько весит электронная книга:", ebook.get_file_size_mb(), "MB")

    print("\n")
    print("Добавить книгу в шкаф:", shelf.add_book(paper))
    print("Количество книг в шкафу:", shelf.count())
    print(shelf.organize_by_author())


    print("\n")
    bag.close_bag()
    print("Добавляем книгу в закрытую сумку:", bag.add_book(paper))  # должно быть False
    bag.open_bag()
    print("Добавляем книгу в открытую сумку:", bag.add_book(paper))
    print("Количество книг в сумке:", bag.count())


if __name__ == "__main__":
    main()

