# Повторенье - мать ученья
# 1.1.  В начале 2000-х мне нравилась игра Majesty, которая была интересна своим непрямым управлением. 
#  - Так если говорить про понятные классы классов персонажей, которые имеют структуру имя, уровень, класс с характеристиками, возможное обмундирование, дающие плюсы к статам, скорость перемещения,
# возможны такие дополнительные поля как расстояние, в которое они готовы пройти за наградой, уровень "жадности", при котором они готовы пойти за наградой. 
# Также имеются классы построек и уровень зданий, с фабриками создания юнитов, уровнем прочности зданий, названия, возможный доход, который они могут приносить или отдельными функциями, которые они дают. 
# Предполагается, что это начальный уровень по ООп, поэтому глубоко не стану закапываться, но на уровне сиситемы уже гораздо больше вариантов сразу приходит в голову. 
# Симуляция своей жизни и уровень приоритетов, поведение, враги, сами задания на каждую миссию, карты и многое другое. Не говоря уже 
# - Также можно взять игру Crusaders King's с её системой генетического наследования. Которая опять же в своей модели, помимо стандартных полей, с именами, характеристиками, способностями, 
# должна иметь классы правил наследования черт родителей и агрегации данных правил в единое целое. Возможно будут два разделения классов и праил, если учитывать "графику", чисто свойства и сама внешность.

# 1.2. Главное не перепутать, что мы пишем на python. Сложно также теперь не учитывать "контракты", но и сразу мыслить ими в реализации на python сложно

from dataclasses import dataclass

#типовой алиас. Сейчас не принципиально, после возможно превращение в класс
type Coord = tuple[float, float]

#Максимальное упрощение
@dataclass
class Hero:
    name: str
    hero_class: str
    level: int
    hp: int
    speed: float
    greed: int
    max_prize_distance: float

@dataclass
class Building:
    name: str
    building_type: str
    level: int
    hp: int
    income_per_day: int
    pos: Coord

@dataclass
class Prize:
    prize_type: str
    reward: int # сумма награды
    pos: Coord

def distance(from_point: Coord, to_point: Coord) -> float:
    dx = from_point[0] - to_point[0]
    dy = from_point[1] - to_point[1]
    return (dx * dx + dy * dy) ** 0.5

def will_hero_take_prize(hero: Hero, hero_point: Coord, prize: Prize) -> bool:
    dist = distance(hero_point, prize.pos)
    return (
            prize.reward >= hero.greed
            and dist <= hero.max_prize_distance
    )

# для побочных эффектов; не должно ничего возвращать, но объект поменяется
def heal_hero(hero: Hero, heal_amount: int) -> None:
        hero.hp += heal_amount

#---------------------
def main() -> None:
    hero_1 = Hero(
        name="Rolf",
        hero_class="Ranger",
        level=2,
        hp=80,
        speed=4.5,
        greed=40,
        max_prize_distance=120.0,
    )

    hero_2 = Hero(
        name="Abram",
        hero_class="Wizard",
        level=3,
        hp=55,
        speed=3.2,
        greed=70,
        max_prize_distance=90.0,
    )

    guild = Building(
        name="Rangers Guild",
        building_type="guild",
        level=1,
        hp=500,
        income_per_day=25,
        pos=(10.0, 10.0),
    )

    prize = Prize(
        prize_type="attack",
        reward=60,
        pos=(70.0, 50.0),
    )

    print(hero_1)
    print(hero_2)
    print(guild)
    print(prize)

    hero_1_pos: Coord = (12.0, 12.0)
    hero_2_pos: Coord = (35.0, 20.0)
    print()
    print(f"{hero_1.name} take prize? {will_hero_take_prize(hero_1, hero_1_pos, prize)}")
    print(f"{hero_2.name} take prize? {will_hero_take_prize(hero_2, hero_2_pos, prize)}")

#1.3. Побочный эффект - функция меняет объект и это видно снаружи
    print()
    print(f"Before healing: {hero_2.name} hp={hero_2.hp}")
    heal_hero(hero_2, heal_amount=30)
    print(f"After healing:  {hero_2.name} hp={hero_2.hp}")


if __name__ == "__main__":
    main()
  
