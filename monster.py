import os
import random

import updater

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

class Monster:
    # TO ADD: variability in drops, additional monster types(?) (such as bosses?)
    # AI type, is that necessary?
    def __init__(self, name, level, room):
        self.name = name
        self.room = room
        self.level = level
        self.gold = level * 20 # determines how much gold enemies drop
        self.health = 20 + (level-1) * 10 
        self.mhp = self.health
        self.atk = 3 + (level-1)
        self.defe = 2 + (level-1)
        self.acc = 90 # accuracy of enemies attacks
        room.add_monster(self)
        updater.register(self)
    def update(self):
        if random.random() < .5:
            self.move_to(self.room.random_neighbor())
    def move_to(self, room):
        self.room.remove_monster(self)
        self.room = room
        room.add_monster(self)
    def die(self):
        self.room.remove_monster(self)
        updater.deregister(self)
    def show_status(self):
        clear()
        print(f"{self.name} status:")
        print()
        print(f"Level: {self.level}")
        print(f"HP: {self.health}/{self.mhp}")
        print(f"Attack: {self.atk}")
        print(f"Defense: {self.defe}")
        print()
        input("Press enter to continue...")