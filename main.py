"""
Задание: Исправление ошибок и модернизация первой версии игры
bugfix02-balance. ⚖️ Сбалансировать урон монстра и игрока
"""

from abc import ABC, abstractmethod
import random

class Weapon(ABC):
    @abstractmethod
    def attack(self):
        pass

    @abstractmethod
    def recharge(self):
        pass

class Railgun(Weapon):
    def __init__(self):
        self.last_used_battle = 0
        self.recharge_counter = 0
        self.available = True

    def attack(self):
        if self.available:
            damage = random.randint(25, 40)
            return damage
        else:
            return 0  # Оружие недоступно

    def recharge(self, current_battle_number):
        # Если оружие не использовалось или прошло 10 схваток с последнего использования
        if self.last_used_battle == 0 or current_battle_number >= self.last_used_battle + 10:
            self.available = True
            self.recharge_counter = 0
        else:
            self.available = False
            self.recharge_counter = (self.last_used_battle + 10) - current_battle_number
        # Обновляем номер схватки, если оружие используется
        if self.available and self.last_used_battle != current_battle_number:
            self.last_used_battle = current_battle_number
        return self.available

class Rocket(Weapon):
    def __init__(self):
        self.last_used_battle = 0
        self.recharge_counter = 0
        self.available = True

    def attack(self):
        if self.available:
            damage = random.randint(15, 25)
            return damage
        else:
            return 0  # Оружие недоступно

    def recharge(self, current_battle_number):
        # Если оружие не использовалось или прошло 5 схваток с последнего использования
        if self.last_used_battle == 0 or current_battle_number >= self.last_used_battle + 5:
            self.available = True
            self.recharge_counter = 0
        else:
            self.available = False
            self.recharge_counter = (self.last_used_battle + 5) - current_battle_number
        # Обновляем номер схватки, если оружие используется
        if self.available and self.last_used_battle != current_battle_number:
            self.last_used_battle = current_battle_number
        return self.available

class Grenade(Weapon):
    def __init__(self):
        self.last_used_battle = 0
        self.recharge_counter = 0
        self.available = True

    def attack(self):
        if self.available:
            damage = random.randint(10, 18)
            return damage
        else:
            return 0  # Оружие недоступно

    def recharge(self, current_battle_number):
        # Если оружие не использовалось или прошло 4 схватки с последнего использования
        if self.last_used_battle == 0 or current_battle_number >= self.last_used_battle + 4:
            self.available = True
            self.recharge_counter = 0
        else:
            self.available = False
            self.recharge_counter = (self.last_used_battle + 4) - current_battle_number
        # Обновляем номер схватки, если оружие используется
        if self.available and self.last_used_battle != current_battle_number:
            self.last_used_battle = current_battle_number
        return self.available

class MachineGun(Weapon):
    def __init__(self):
        self.last_used_battle = 0
        self.recharge_counter = 0
        self.available = True

    def attack(self):
        if self.available:
            damage = random.randint(3, 8)
            return damage
        else:
            return 0  # Оружие недоступно

    def recharge(self, current_battle_number):
        # Если оружие не использовалось или прошло 3 схватки с последнего использования
        if self.last_used_battle == 0 or current_battle_number >= self.last_used_battle + 3:
            self.available = True
            self.recharge_counter = 0
        else:
            self.available = False
            self.recharge_counter = (self.last_used_battle + 3) - current_battle_number
        # Обновляем номер схватки, если оружие используется
        if self.available and self.last_used_battle != current_battle_number:
            self.last_used_battle = current_battle_number
        return self.available

class Knife(Weapon):
    def __init__(self):
        self.available = True

    def attack(self):
        damage = random.randint(1, 6)
        return damage

    def recharge(self, current_battle_number=None):
        self.available = True
        return True

class Monster:
    def __init__(self):
        self.health = 100
        self.weapons = ['зубы', 'когти', 'рога']

    def attack(self):
        weapon = random.choice(self.weapons)
        damage = random.randint(3, 10)
        return weapon, damage

    def take_damage(self, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0
        return self.health

class Warrior:
    def __init__(self, weapons):
        self.health = 100
        self.weapons = weapons  # список экземпляров оружия

    def attack(self, weapon):
        if weapon in self.weapons:
            damage = weapon.attack()
            return weapon, damage
        else:
            raise ValueError('Оружие не найдено в списке доступных!')

    def take_damage(self, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0
        return self.health

def battle():
    print('--- Начало битвы! ---')
    # Создаём оружие
    available_weapons = [
        Railgun(),
        Rocket(),
        Grenade(),
        MachineGun(),
        Knife()
    ]
    # Создаём воина и монстра
    warrior = Warrior(available_weapons)
    monster = Monster()
    battle_number = 1
    while warrior.health > 0 and monster.health > 0:
        print(f'\nСхватка #{battle_number}')
        print(f'Здоровье Воина: {warrior.health}')
        print(f'Здоровье Монстра: {monster.health}')
        print('Доступное оружие:')
        for idx, weapon in enumerate(warrior.weapons, 1):
            weapon_name = weapon.__class__.__name__
            if hasattr(weapon, "available"):
                available = "Доступно" if weapon.available else f"Недоступно (до готовности {getattr(weapon, 'recharge_counter', 0)})"
            else:
                available = "Доступно"
            print(f'{idx}. {weapon_name} - {available}')
        # Выбор оружия
        while True:
            try:
                choice = int(input('Выберите оружие по номеру: '))
                if 1 <= choice <= len(warrior.weapons):
                    chosen_weapon = warrior.weapons[choice-1]
                    # Проверка доступности
                    if hasattr(chosen_weapon, "available") and not chosen_weapon.available:
                        print('Оружие недоступно, выберите другое!')
                        continue
                    break
                else:
                    print('Некорректный номер!')
            except ValueError:
                print('Введите номер!')
        # Атака воина
        weapon_obj, warrior_damage = warrior.attack(chosen_weapon)
        print(f'Воин атакует с помощью {weapon_obj.__class__.__name__} и наносит {warrior_damage} урона!')
        monster.take_damage(warrior_damage)
        # Перезарядка оружия
        for w in warrior.weapons:
            if hasattr(w, 'recharge'):
                w.recharge(battle_number)
        # Атака монстра
        monster_weapon, monster_damage = monster.attack()
        print(f'Монстр атакует с помощью {monster_weapon} и наносит {monster_damage} урона!')
        warrior.take_damage(monster_damage)
        battle_number += 1
    print('\n--- Битва окончена! ---')
    if warrior.health <= 0 and monster.health <= 0:
        print('Ничья! Оба пали в бою.')
    elif warrior.health <= 0:
        print('Монстр победил!')
    else:
        print('Воин победил!')

if __name__ == "__main__":
    battle()
