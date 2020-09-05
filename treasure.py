#!/usr/bin/env python3
import argparse
import csv
from random import randint, choices
from typing import NamedTuple, Sequence, Optional, List, Dict
from io import StringIO

class TreasureRow(NamedTuple):
    level: int
    silver: int
    gold: int
    gems: int
    jewels: int
    magic: int

class TreasureTable:
    @classmethod
    def from_csv(cls, treasure_file:str) -> 'TreasureTable':
        with open(treasure_file, 'r', encoding='utf-8') as tf:
            treasure_reader = csv.reader(tf, delimiter=',')
            labels = next(treasure_reader)
            rows = [r for r in treasure_reader]
        treasure = {}
        for row in rows:
            tr = TreasureRow(*(int(x) for x in row))
            treasure[int(tr.level)] = tr
        return cls(treasure)

    def __init__(self, treasure:Dict[int, TreasureRow]) -> None:
        self.treasure = treasure

    def roll(self, dungeon_level:int) -> 'TreasureResult':
        treasure_row = self.treasure[dungeon_level]
        gold = roll_gold(treasure_row.gold)
        silver = roll_silver(treasure_row.silver, dungeon_level)
        gems = roll_gems(treasure_row.gems, dungeon_level)
        jewels = roll_jewels(treasure_row.jewels, dungeon_level)
        magic = roll_magic(treasure_row.magic)
        return TreasureResult(gold, silver, gems, jewels, magic, dungeon_level)

class Gem:
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
    
    def __init__(self) -> None:
        self.value = choices(
            population = self.gem_chances[0], 
            weights = self.gem_chances[1]
            )[0]
        self._upgrade()

    def _upgrade(self) -> None:
        if randint(1, 6) == 1:
            self.value = self.upgrade_map[self.value]
            self._upgrade()

    def __str__(self):
        return f'A {self.value}gp gem'

class Jewel:
    def __init__(self) -> None:
        roll = randint(1,100)
        if roll <= 20:
            self.value = (randint(1,6) + randint(1,6) + randint(1,6)) * 100
        elif roll <= 80:
            self.value = randint(1,6) * 1000
        else:
            self.value = randint(1,10) * 1000
    def __str__(self) -> str:
        return f'{self.value} jewelry'
    
class MagicItem:
    magic_table=(   ('Potion', 'Scroll', 'Ring', 'Wand', 'Misc', 'Armor', 'Weapon'),
                    ( 25,       25,       5,      5,      5,      10,      10, )   )

    def __init__(self) -> None:
        self.type = choices(
            population = self.magic_table[0],
            weights = self.magic_table[1]
            )[0]

    def __str__(self) -> str:
        return f'Magic {self.type}'

class TreasureResult(NamedTuple):
    gold: int
    silver: int
    gems: Sequence[Gem]
    jewels: Sequence[Jewel]
    magic: Optional[MagicItem]
    level: int
    def format_result(self) -> str:
        buff = StringIO()
        buff.write(f'Level {self.level} Treasure:\n')
        def indent() -> None:
            buff.write(' '*4)
        if self.gold:
            indent()
            buff.write(f'- {self.gold}gp\n')
        if self.silver:
            indent()
            buff.write(f'- {self.silver}sp\n')
        if self.gems:
            for g in self.gems:
                indent()
                buff.write(f'- {g}\n')
        if self.jewels:
            for j in self.jewels:
                indent()
                buff.write(f'- {j}\n')
        if self.magic:
            indent()
            buff.write(f'- A {self.magic}\n')
        result = buff.getvalue()
        buff.close()
        return result

def roll_gold(gold_constant:int) -> int:
    gold = randint(0, 1) * gold_constant * randint(1, 6)
    return gold

def roll_silver(silver_constant:int, level:int)-> int:
    if level < 3:
        silver = silver_constant * randint(1, 12)
    else:
        silver = silver_constant * randint(1, 6)
    return silver

def roll_gems(gem_probability:int, level:int):
    if level > 7:
        gem_chances = 12
    else:
        gem_chances = 6
    gems = [ Gem() for _ in range(gem_chances) if randint(1, 100) <= gem_probability ]
    return gems

def roll_jewels(jewel_probability:int, level:int) -> List[Jewel]:
    if level > 7:
        jewel_chances = 12
    else:
        jewel_chances = 6
    jewels = [ Jewel() for _ in range(jewel_chances) if randint(1, 100) <= jewel_probability ]
    return jewels

def roll_magic(magic_probability:int) -> Optional[MagicItem]:
    if randint(1, 100) <= magic_probability:
        return MagicItem()
    else:
        return None

default_treasure_table = TreasureTable.from_csv('odndtreasure.csv')          

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--level', '-l', type=int, default=1)
    parser.add_argument('--count', '-c', type=int, default=1)
    args = parser.parse_args()
    run(**vars(args))

def run(level:int, count:int) -> None:
    for _ in range(count):
        treasure_result = default_treasure_table.roll(level)
        print(treasure_result.format_result(), end='')

if __name__ == '__main__':
    main()
