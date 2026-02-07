# Очень сложно с непривычки не ошибиться в синтаксисе, не говоря о другом.
# Классы и методы хочется прописать с предусловиями, а с другой стороны не хватает системы проектирования
# поэтому получается небольшой такой разрозненный разброд

from dataclasses import dataclass

type Coord = tuple[float, float]


# Максимальное упрощение
class Hero:
    name: str
    hero_class: str
    level: int
    hp: int
    speed: float
    greed: int
    max_prize_distance: float
    pos_hero_coord: Coord

    # контруктор
    def __init__(self, name: str, hero_class: str, level: int, hp: int, speed: float, greed: int,
                 max_prize_distance: float, pos_hero_coord: Coord) -> None:
        self.name = name
        self.hero_class = hero_class
        self.level = level
        self.hp = hp
        self.speed = speed
        self.greed = greed
        self.max_prize_distance = max_prize_distance
        self.pos_hero_coord = pos_hero_coord

    # три метода
    def is_alive(self) -> bool:
        return self.hp > 0

    def take_damage(self, damage: int) -> None:
        self.hp = max(0, self.hp - damage)

    def heal(self, heal_count: int) -> None:
        self.hp += heal_count


class Building:
    name: str
    building_type: str
    level: int
    hp: int
    income_per_day: int
    last_day_by_income: int
    destroyed: bool
    pos_building_coord: Coord

    # контруктор
    def __init__(self, name: str, building_type: str, level: int, hp: int, income_per_day: int, last_day_by_income: int,
                 pos_building_coord: Coord) -> None:
        self.name = name
        self.building_type = building_type
        self.level = level
        self.hp = hp
        self.income_per_day = income_per_day
        self.last_day_by_income = last_day_by_income
        self.pos_building_coord = pos_building_coord
        self.destroyed = False

    # три метода
    def building_upgrade(self) -> None:
        if self.destroyed:
            return
        self.level += 1
        self.income_per_day += 10

    def collect_income(self, current_day: int) -> int:
        if self.destroyed:
            return 0
        days_for_income = current_day - self.last_day_by_income
        self.last_day_by_income = current_day
        return self.income_per_day * days_for_income

    def destroy(self) -> None:
        self.destroyed = True
        self.hp = 0
        self.income_per_day = 0


# контруктор

@dataclass
class Prize:
    prize_type: str
    reward: int  # сумма награды
    pos: Coord


def main() -> None:
    # Объекты
    hero_1 = Hero("Rolf", "Ranger", 2, 80, 4.5, 70, 120.0, (12.0, 12.0))
    hero_2 = Hero("Abram", "Wizard", 3, 55, 3.2, 40, 90.0, (17.0, 17.0))

    ranger_guild = Building(
        name="Rangers Guild",
        building_type="guild",
        level=1,
        hp=500,
        income_per_day=25,
        last_day_by_income=1,
        pos_building_coord=(10.0, 10.0),
    )

    wizard_guild = Building(
        name="Wizard Guild",
        building_type="guild",
        level=1,
        hp=500,
        income_per_day=25,
        last_day_by_income=1,
        pos_building_coord=(15.0, 15.0),
    )

    # Вызываем их методы и выводим на экран
    print("____HERO____")
    print()
    print("hero_1 alive:", hero_1.is_alive())
    hero_1.take_damage(30)
    print("hero_1 hp after damage:", hero_1.hp)
    hero_1.heal(10)
    print("hero_1 hp after heal:", hero_1.hp)

    print()
    print("hero_2 alive:", hero_2.is_alive())
    hero_2.take_damage(100)
    print("hero_2 hp after damage:", hero_2.hp)
    print("hero_2 alive after damage:", hero_2.is_alive())

    print()
    print()
    print("____BUILDINGS____")
    print()
    print("ranger_guild income:", ranger_guild.collect_income(current_day=4))
    ranger_guild.building_upgrade()
    print("ranger_guild level after upgrade:", ranger_guild.level)
    print("ranger_guild income_per_day after upgrade:", ranger_guild.income_per_day)

    print()
    print("wizard_guild income:", wizard_guild.collect_income(current_day=3))
    wizard_guild.destroy()
    print("wizard_guild destroyed:", wizard_guild.destroyed)
    print("wizard_guild income after destroy:", wizard_guild.collect_income(current_day=10))
    print("wizard_guild hp after destroy:", wizard_guild.hp)
if __name__ == "__main__":
    main()

