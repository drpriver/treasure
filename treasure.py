#!/usr/local/bin/python3
import sys
import random
import itempick
def d(N):
    return random.randint(1,N)

class treasure():
    def mktreasuretable(self,treasuretable):
        try:
            treasure=open(treasuretable,'r')
        except:
            print("Treasure file is missing!!!\n", file=sys.stderr)
            sys.exit(1)
        table=[row.rstrip() for row in treasure]
        labels=table.pop(0).split(',')
        treasuretable={}
        for row in table:
            treasuretable[int(row.split(',')[0])]=dict(zip(labels,row.split(',')))
        self.tt=treasuretable
    def mksilver(self):
        self.silver=0
        if 1 < self.dl < 3:
            self.silver=int(self.tt[self.dl]['Silver'])*d(12)
        else:
            self.silver=int(self.tt[self.dl]['Silver'])*d(6)
    def mkgold(self):
        self.gold=0
        self.gold=(d(2)-1)*int(self.tt[self.dl]['Gold'])*d(6)

    g=itempick.gem_picker()
    def mkgems(self):
        self.gems=''
        gprob= int(self.tt[self.dl]['Gems'])
        diesize=6
        if self.dl>=8:
            diesize=12
        self.gems=[self.g() for each in range(d(diesize)) if d(100)<=gprob]

    j=itempick.jewel_picker()
    def mkjewels(self):
        self.jewels=''
        jprob=int(self.tt[self.dl]['Jewels'])
        diesize=6
        if self.dl >= 8:
            diesize=12
        self.jewels=[self.j() for each in range(d(diesize)) if d(100) <=jprob]

    m=itempick.magic()
    def mkmagic(self):
        self.magic=''
        mprob=int(self.tt[self.dl]['Jewels'])
        self.magic=[self.m() for each in range(1) if d(100) <= mprob]
    def __str__(self):
        retrnstr='Treasure:\n'
        indent='\t'+'- '
        if self.silver:
            retrnstr+=indent+str(self.silver)+'sp\n'
        if self.gold:
            retrnstr+=indent+str(self.gold)+'gp\n'
        if self.gems:
            for gem in self.gems:
                retrnstr+=indent+str(gem)+'\n'
        if self.jewels:
            for jewel in self.jewels:
                retrnstr+=indent+str(jewel)+'\n'
        if self.magic:
            for magic in self.magic:
                retrnstr+=indent+str(magic)+'\n'
        return retrnstr
    def __call__(self,dl=1):
        self.dl=dl
        self.mksilver()
        self.mkgold()
        self.mkgems()
        self.mkjewels()
        self.mkmagic()
        return str(self)
    def __init__(self, treasuretable='./tables/odndtreasure.txt', dl=1):
        self.mktreasuretable(treasuretable)
        self(dl)
t=treasure()
dungeonlevel=1
loops=range(1)
if __name__ == "__main__":
    try: dungeonlevel=int(sys.argv[1])
    except: pass
    try: loops=range(int(sys.argv[2]))
    except: pass
    if dungeonlevel > 10:
        dungeonlevel=10
    for x in loops:
        print(f"Level {dungeonlevel} treasure")
        print(t(dungeonlevel))
