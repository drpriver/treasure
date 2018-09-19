#!/usr/bin/env python3
from random import randint, choices
import csv
from collections import namedtuple

treasure_row = namedtuple('treasure_row', ['Level', 'Silver','Gold','Gems','Jewels','Magic'])

class treasure_table:
    def __init__(self, treasure_file):
        with open(treasure_file, 'r', encoding='utf-8') as tf:
            treasure_reader = csv.reader(tf, delimiter=',')
            labels = next(treasure_reader)
            rows = [r for r in treasure_reader]
        treasure = {}
        for row in rows:
            tr = treasure_row(*(int(x) for x in row))
            treasure[int(tr.Level)] = tr
        self.treasure = treasure
    def __call__(self, dungeon_level):
        treasure_row = self.treasure[dungeon_level]
        gold = roll_gold(treasure_row.Gold)
        silver = roll_silver(treasure_row.Silver, dungeon_level)
        gems = roll_gems(treasure_row.Gems, dungeon_level)
        jewels = roll_jewels(treasure_row.Jewels, dungeon_level)
        magic = roll_magic(treasure_row.Magic)
        return gold, silver, gems, jewels, magic, dungeon_level

def roll_gold(Gold_constant):
    gold = randint(0,1) * Gold_constant * randint(1,6)
    return gold

def roll_silver(Silver_constant, level):
    if level < 3:
        silver = Silver_constant * randint(1,12)
    else:
        silver = Silver_constant * randint(1,6)
    return silver

def roll_gems(gem_probability, level):
    if level > 7:
        gem_chances = 12
    else:
        gem_chances = 6
    gems = [ gem() for _ in range(gem_chances) if randint(1,100) <= gem_probability ]
    return gems
def roll_jewels(jewel_probability, level):
    if level > 7:
        jewel_chances = 12
    else:
        jewel_chances = 6
    jewels = [ jewel() for _ in range(jewel_chances) if randint(1,100) <= jewel_probability ]
    return jewels

def roll_magic(magic_probability):
    if randint(1,100) <= magic_probability:
        return magic_item()
    else:
        return None

def format_treasure_result(gold, silver, gems, jewels, magic, level):
    result = f"""
Level {level} Treasure:"""
    if gold:
        result+=f"""
    - {gold}gp"""
    result += f"""
    - {silver}sp"""
    if gems:
        result+='\n'+'\n'.join(f"    - {g}" for g in gems)
    if jewels:
        result+='\n'+'\n'.join(f"    - {j}" for j in jewels)
    if magic:
        result+=f"""
    - A {magic}"""
    return result

class gem:
    gem_chances = [ (10, 50, 100, 500, 100),
                    (10, 15, 50,  15,  10 ) ]
    upgrade_map = {     10 :      50,
                        50 :     100,
                       100 :     500,
                       500 :   1_000,
                     1_000 :   5_000,
                     5_000 :  10_000,
                    10_000 :  25_000,
                    25_000 :  50_000,
                    50_000 : 100_000,
                   100_000 : 500_000  }
    
    def __init__(self):
        self.value = choices(
            population = self.gem_chances[0], 
            weights = self.gem_chances[1]
            )[0]
        self.upgrade()
    def upgrade(self):
        if randint(1, 6) == 1:
            self.value = self.upgrade_map[self.value]
            self.upgrade()
    def __str__(self):
        return f"A {self.value}gp gem"
class jewel:
    def __init__(self):
        roll = randint(1,100)
        if roll <= 20:
            self.value = (randint(1,6) + randint(1,6) + randint(1,6)) * 100
        elif roll <= 80:
            self.value = randint(1,6) * 1000
        else:
            self.value = randint(1,10) * 1000
    def __str__(self):
        return f"{self.value} jewelry"
class magic_item:
    magic_table=[   ("Potion", "Scroll", "Ring", "Wand", "Misc", "Armor", "Weapon"),
                    ( 25,       25,       5,      5,      5,      10,      10, )   ]
    def __init__(self):
        self.type = choices(
            population = self.magic_table[0],
            weights = self.magic_table[1]
            )[0]
    def __str__(self):
        return f"Magic {self.type}"
default_treasure_table = treasure_table("odndtreasure.txt")          
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-level", "-l", type = int, default = 1)
    parser.add_argument("-count", "-c", type = int, default = 1)
    args = parser.parse_args()
    for _ in range(args.count):
        treasure_result = default_treasure_table(args.level)
        print(format_treasure_result(*treasure_result))
