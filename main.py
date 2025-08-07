"""
Задание: Исправление ошибок и модернизация первой версии игры
bugfix01-logic. Проверка работоспособности и устранение ошибок
"""

from abc import ABC, abstractmethod
import random

class Weapon(ABC):
    @abstractmethod
    def attack(self):
        pass

    @abstractmethod
    def recharge(self, current_battle_number):
        pass

class Railgun(Weapon):
    def __init__(self):
        self.last_used_battle = 0
        self.recharge_counter = 0
        self.available = True

    def attack(self):
        if self.available:
            damage = random.randint(15, 20)
            return damage
        return 0

    def recharge(self, current_battle_number):
        if self.last_used_battle == 0 or current_battle_number >= self.last_used_battle + 10:
            self.available = True
            self.recharge_counter = 0
        else:
            self.available = False
            self.recharge_counter = (self.last_used_battle + 10) - current_battle_number
        return self.available

class Rocket(Weapon):
    def __init__(self):
        self.last_used_battle = 0
        self.recharge_counter = 0
        self.available = True

    def attack(self):
        if self.available:
            damage = random.randint(20, 30)
            return damage
        return 0

    def recharge(self, current_battle_number):
        if self.last_used_battle == 0 or current_battle_number >= self.last_used_battle + 5:
            self.available = True
            self.recharge_counter = 0
        else:
            self.available = False
            self.recharge_counter = (self.last_used_battle + 5) - current_battle_number
        return self.available

class Grenade(Weapon):
    def __init__(self):
        self.last_used_battle = 0
        self.recharge_counter = 0
        self.available = True

    def attack(self):
        if self.available:
            damage = random.randint(10, 20)
            return damage
        return 0

    def recharge(self, current_battle_number):
        if self.last_used_battle == 0 or current_battle_number >= self.last_used_battle + 4:
            self.available = True
            self.recharge_counter = 0
        else:
            self.available = False
            self.recharge_counter = (self.last_used_battle + 4) - current_battle_number
        return self.available

class MachineGun(Weapon):
    def __init__(self):
        self.last_used_battle = 0
        self.recharge_counter = 0
        self.available = True

    def attack(self):
        if self.available:
            damage = random.randint(0, 10)
            return damage
        return 0

    def recharge(self, current_battle_number):
        if self.last_used_battle == 0 or current_battle_number >= self.last_used_battle + 3:
            self.available = True
            self.recharge_counter = 0
        else:
            self.available = False
            self.recharge_counter = (self.last_used_battle + 3) - current_battle_number
        return self.available

class Knife(Weapon):
    def __init__(self):
        self.available = True
        self.recharge_counter = 0

    def attack(self):
        return random.randint(0, 5)

    def recharge(self, current_battle_number=None):
        self.available = True
        self.recharge_counter = 0
        return True

class Monster:
    def __init__(self):
        self.health = 100
        self.weapons = ['зубы', 'когти', 'рога']

    def attack(self):
        weapon = random.choice(self.weapons)
        damage = random.randint(1, 5)
        return weapon, damage

    def take_damage(self, damage):
        self.health = max(self.health - damage, 0)
        return self.health

class Warrior:
    def __init__(self, weapons):
        self.health = 100
        self.weapons = weapons

    def attack(self, weapon, battle_number):
        if weapon in self.weapons:
            damage = weapon.attack()
            if hasattr(weapon, 'available') and weapon.available:
                weapon.last_used_battle = battle_number
            return weapon, damage
        else:
            raise ValueError('Оружие не найдено в списке!')

    def take_damage(self, damage):
        self.health = max(self.health - damage, 0)
        return self.health

def battle():
    print('--- Начало битвы! ---')
    available_weapons = [Railgun(), Rocket(), Grenade(), MachineGun(), Knife()]
    warrior = Warrior(available_weapons)
    monster = Monster()
    battle_number = 1

    while warrior.health > 0 and monster.health > 0:
        print(f'\nСхватка #{battle_number}')
        print(f'Здоровье Воина: {warrior.health}')
        print(f'Здоровье Монстра: {monster.health}')

        # Обновляем доступность оружия перед боем
        for weapon in warrior.weapons:
            weapon.recharge(battle_number)

        print('Доступное оружие:')
        for idx, weapon in enumerate(warrior.weapons, 1):
            name = weapon.__class__.__name__
            if hasattr(weapon, 'available'):
                status = "Доступно" if weapon.available else f"Недоступно (до готовности {weapon.recharge_counter})"
            else:
                status = "Доступно"
            print(f'{idx}. {name} - {status}')

        # Выбор оружия
        while True:
            try:
                choice = int(input('Выберите оружие по номеру: '))
                if 1 <= choice <= len(warrior.weapons):
                    chosen_weapon = warrior.weapons[choice - 1]
                    if hasattr(chosen_weapon, 'available') and not chosen_weapon.available:
                        print('Оружие недоступно, выберите другое!')
                        continue
                    break
                else:
                    print('Некорректный номер!')
            except ValueError:
                print('Введите номер!')

        weapon_obj, warrior_damage = warrior.attack(chosen_weapon, battle_number)
        print(f'Воин атакует с помощью {weapon_obj.__class__.__name__} и наносит {warrior_damage} урона!')
        monster.take_damage(warrior_damage)

        if monster.health <= 0:
            break

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

