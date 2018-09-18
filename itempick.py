#!/usr/local/bin/python
# Well this shit needs to be rewritten! lol! wtf was I doing
import random
import yaml
def parse_item_table(itemfile):
    """item files are now yaml!"""
    with open(itemfile,'r') as fp:
        item_dict=yaml.load(fp)
    for each in item_dict: item_dict[each]['name']=each
    return item_dict

def random_item(item_dict,weights=False):
    if weights:
        keys=[]
        weights=[]
        for each in item_dict:
            keys.append(each)
            weights.append(item_dict[each][weight])
            return item_dict[random.choices(keys,weights)[0]]
    else:
        return item_dict[random.choice(list(item_dict))]

class item:
    def __init__(self,item_dict):
        self.name=item_dict.get('name')
        self.description=item_dict.get('description')
        self.appearance=item_dict.get('appearance')
    def __str__(self):
        itemstring=str(self.name)
        if self.description:
           itemstring+='\n\t'+str(self.description)
        if self.appearance:
            itemstring+='\n\t'+str(self.appearance)
        return itemstring
class item_picker:
    itemtype=item
    def __init__(self,file_to_parse=None):
        if not file_to_parse:
            file_to_parse=self.default_file
        self.parse(file_to_parse)
    def parse(self,itemfile):
        self.item_dict=parse_item_table(itemfile)
    def pick(self):
        return random_item(self.item_dict)
    def __call__(self):
        return self.itemtype(self.pick())


class potion(item):
    def __str__(self):
        potstring="Potion of "+self.name
        potstring+="\n\tEffect: "+self.description
        potstring+="\n\tAppearance: "+self.appearance
        return potstring
class potion_picker(item_picker):
    itemtype=potion
    default_file='./tables/potions.yaml'

class gem(item):
    def __str__(self):
        retrnstr=str(self.description)+"gp gem"
        return retrnstr
def gemupgrade(rawgem):
    "note that gem_upgrade will take a gem and upgrade it in-place"
    upgrade_dict = {    10 :      50,
                        50 :     100,
                       100 :     500,
                       500 :   1_000,
                     1_000 :   5_000,
                     5_000 :  10_000,
                    10_000 :  25_000,
                    25_000 :  50_000,
                    50_000 : 100_000,
                   100_000 : 500_000  }
    if random.randint(1,6)<=1:
        rawgem.description=upgrade_dict[rawgem.description]
        gemupgrade(rawgem)
    else:
        rawgem.description*=(random.randint(1,6)+random.randint(1,6)+3)/10
        rawgem.description=int(rawgem.description)
class gem_picker(item_picker):
    itemtype=gem
    default_file='./tables/gem.yaml'
    def __call__(self):
        rawgem=self.itemtype(self.pick())
        gemupgrade(rawgem)
        return rawgem
class jewel(item):
    def __str__(self):
        return str(self.description)+"gp jewelry"
class jewel_picker(item_picker):
    itemtype=jewel
    default_file='./tables/jewel.yaml'
    def pick(self):
        #TODO
        return {'description': 1000}
    def __call__(self):
        raw_jewel=self.itemtype(self.pick())
        raw_jewel.description*=(random.randint(1,6)+random.randint(1,6)+3)/10
        raw_jewel.description=int(raw_jewel.description)
        return raw_jewel
class scroll(item):
    def __str__(self):
        scrollstring="Scroll of "+self.description
        return scrollstring
class scroll_picker(item_picker):
    default_file='./tables/scroll.yaml'
    itemtype=scroll
    def __call__(self):
        tempscroll=scroll({})
        tempscroll.description=', '.join(map(lambda x: self.pick()['name'],range(min(random.randint(3,7),random.randint(3,7)))))
        return tempscroll
class weapon_picker():
    def __init__(self):
        self.mweapon=item_picker('./tables/meleeweapon.yaml')
        self.mproperties=item_picker('./tables/meleeproperties.yaml')
        self.rweapon=item_picker('./tables/rangedweapon.yaml')
        self.rproperties=item_picker('./tables/rangedproperties.yaml')
        self.tweapon=item_picker('./tables/thrownweapon.yaml')
        self.tproperties=item_picker('./tables/thrownproperties.yaml')
    def __call__(self):
        weptype=random.choices(['Melee','Ranged','Thrown'],weights=[3,2,1])[0]
        if weptype=='Melee':
            wep=self.mweapon()
            prop=self.mproperties
        elif weptype=='Ranged':
            wep=self.rweapon()
            prop=self.rproperties
        elif weptype=='Thrown':
            wep=self.tweapon()
            prop=self.tproperties
        enchant_weapon(wep,prop)
        return magic_weapon(wep)
def enchant_weapon(weapon,properties):
    plusses=0
    if random.randint(1,6)<=4:
        plusses+=1
        if random.randint(1,6)<=3:
            plusses+=1
    num_properties=min(random.choice([0,1,2]),random.choice([0,1,2,]))
    if not plusses and not num_properties:
        plusses+=1
    weapon_properties=[]
    while len(weapon_properties)<num_properties:
        temp=properties()
        if temp in weapon_properties:
            continue
        else:
            weapon_properties.append(temp)
    weapon.plusses=plusses
    weapon.properties=weapon_properties

class magic_weapon:
    def __init__(self,enchanted_weapon):
        self.plusses=enchanted_weapon.plusses
        self.properties=enchanted_weapon.properties
        self.name=enchanted_weapon.name
    def __str__(self):
        retrnstr=''
        if self.plusses:
            retrnstr+="+"+str(self.plusses)+" "
        retrnstr+=self.name
        if len(self.properties)>0:
            retrnstr+=" of "+self.properties[0].name
        if len(self.properties)>1:
            retrnstr+=" and "+self.properties[1].name
        return retrnstr

class armor(item):
    def __str__(self):
        armor_string=''
        if self.plusses:
            armor_string+='+'+str(self.plusses)+' '
        armor_string+=self.name
        if self.properties:
            armor_string+=' of ' +str(self.properties.name)
        return armor_string
class armor_picker(item_picker):
    default_file='./tables/armor.yaml'
    itemtype=armor
    def __call__(self):
        raw_armor=armor(self.pick())
        enchant_armor(raw_armor)
        return raw_armor

ap=item_picker('./tables/armorproperties.yaml')
def enchant_armor(armor):
    plusses=0
    if random.randint(1,6)<=3:
        plusses+=1
        if random.randint(1,6)<=2:
            plusses+=1
    if plusses and random.randint(0,1):
        properties=ap()
    elif not plusses:
        properties=ap()
    else:
        properties=None
    armor.plusses=plusses
    armor.properties=properties

class misc_picker(item_picker):
    default_file='./tables/miscellaneousmagic.yaml'
class wand_picker(item_picker):
    default_file='./tables/wand.yaml'
class ring(item):
    def __str__(self):
        return "Ring of "+self.name
class ring_picker(item_picker):
    default_file='./tables/ring.yaml'
    itemtype=ring

class magic(item_picker):
    item_picker_dict=dict(
                            Potion=potion_picker(),
                            Scroll=scroll_picker(),
                            Armor=armor_picker(),
                            Weapon=weapon_picker(),
                            Ring=ring_picker(),
                            Wand=wand_picker(),
                            Misc=misc_picker()          )
    default_file='./tables/addmagic.yaml'
    def __call__(self):
        return self.item_picker_dict[self.pick()['name']]()

if __name__=='__main__':
    magicmaker=magic()
    for i in range(100): print(magicmaker(),'\n')
