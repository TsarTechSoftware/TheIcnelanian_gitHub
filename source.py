import random
import pickle
import os
import pygame
import numpy
import time
import math

''' [1] = Damage, [2] = Turns to Effect,  [3] = Continuous, [4] Hurts All Opponents,
    [5] = Percentile Factor, [6] attack,defence,health,mgk,luck, [7] Amount,amt,amt,amt,amt
    [8] = Hurt Specific Opponent
    Types of item effect are:
    Frost: The opponent will miss turns according to the attacker's luck. The more powerful
    the weapon, the more turn's lost probability will increase. This uses [2] effect slot.
    
    Drain Soul: The opponent will be poisoned during battle and can use magic, potions, or
    the user must die in order to cure the opponent. This uses the [8] and [3] effect slot.
    
    Blaze: Damages all opponents slightly. Uses [1] and [4].
    
    Lucky: Raises luck. Uses [5].
    
    Greater: Raises [6] by an amount of [7]. [6] is a comma separated list as to allow multiple
    effects to be raised.'''

# This will be initialized with a dtbs
weapons = [("Fists", 1, (), "Hit"), ("Shrokton Dagger", 6, (), "Hit"),
           ("Volshedarr Sword", 10, (), "Hit"), ("Mornatek Sword", 14, (), "Hit"),
           ("Nalshad'aar Sword", 20, (), "Hit"), ("Icnelanian Soldier Sword", 28, (), "Hit"),
           ("Warrior's Sword", 32, (), "Hit"), ("Iron Guard Sword", 35, (), "Hit"),
           ("Magic Sword", 40, (), "Hit"), ("Icnedec's Sword", 50, (), "Hit")]

# This will be initialized with a dtbs
items = [("Shachee Potion", 100, "h"), ("Bomb", 100, "a"), ("Trapped Neshchee Soul", 120, "a"),
         ("Kill Lesser Soul Tome", 150, "a"), ("Greater Shachee Potion", 300, "h")]

main_dir = os.path.split(os.path.abspath(__file__))[0]
danger = .5


def map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


class dummysound:
    def play(self): pass


class entity:

    level = 1
    luck = .99
    gold = 0
    xp = 0
    maxHP = 0
    playerHP = 0
    playerDefense = 0
    maxMP = 0
    playerMP = 0
    playerAP = 0
    name = ""
    weapon = ("NULL", 0)
    inventory = []
    tempAttack = 0

    def __init__(self, lvl=1, newPlayer=1, pName="DEFAULT", weaponThing=weapons[0]):

        playerValue = 100
        npcMultiplier = .6

        if newPlayer == 1:
            npcMultiplier = int(1)

        self.gold = 0
        self.xp = 25*((3*lvl + 1) + 2)*(lvl - 1)
        self.maxHP = int(playerValue * npcMultiplier)
        self.playerHP = self.maxHP
        self.playerDefense = int((playerValue))
        self.maxMP = (playerValue) * npcMultiplier
        self.playerMP = self.maxMP
        self.playerAP = int((playerValue - 95))
        self.name = pName
        self.weapon = weaponThing
        self.inventory = []
        self.levelUp(0)

    def pushInventory(self, tup=("NULL", 0)):
        self.inventory.append(tup)

    def useInventory(self, inCombat=0):
        while True:
            print("Inventory")
            tempNum = 0
            print(tempNum, "::: ", "BACK", sep="")
            tempNum = 1
            for i in self.inventory:
                print(tempNum, "::: ", i[0], ":", i[1], ":", i[2], sep="")
                tempNum = tempNum + 1
            print("What do you want to use?")
            choice = inputI(rangeB=0, rangeE=tempNum-1)
            if choice == 0:
                return
            choice = choice - 1
            if self.inventory[choice][2] == "h":
                self.setHealth(self.playerHP + self.inventory[choice][1])
                print("Recovered", self.inventory[choice][1], "health!")
                self.inventory.remove(self.inventory[choice])
            elif self.inventory[choice][2] == "a" and self.tempAttack == 0:
                if inCombat == 0:
                    print("Cannot use this item right now.")
                    continue
                else:
                    self.tempAttack = self.inventory[choice][1]
                    print(self.name, "used", self.inventory[choice])
                    self.inventory.remove(self.inventory[choice])
                    return -1

    def resetTempAttack(self):
        self.tempAttack = 0

    def printStats(self):
        print("______Stats:______")
        print("Name:", self.name)
        print("Level:", self.level)
        xpNeeded = 25*(3*(int(self.level) + 1) + 2)*int(self.level) - int(self.xp)
        print("XP until next level: ", xpNeeded, "xp", sep="")
        print("HP:", self.maxHP, ":", self.playerHP)
        print("Defense:", self.playerDefense)
        print("Attack Power:", self.playerAP)
        print("MP:", self.maxMP, ":", self.playerMP)
        print("Equipped:", self.weapon[0], ":", self.weapon[1])
        print("XP:", self.xp)
        print("Gold:", self.gold)
        input("Press Enter")

    def setmaxHP(self, num=-1):
        self.maxHP = num
        return

    def setHealth(self, num=-1):
        self.playerHP = num
        if self.playerHP > self.maxHP:
            self.playerHP = self.maxHP
        return

    def setDefense(self, num=-1):
        self.playerDefense = num
        return

    def setMagic(self, num=-1):
        self.playerMP = num
        return

    def setMaxMagic(self, num=-1):
        self.maxMP = num
        return

    def setAttack(self, num=-1):
        self.playerAP = num
        return

    def setWeapon(self,id=0):
        tempAttack = self.playerAP - self.weapon[1]
        self.weapon = weapons[id]
        self.setAttack(tempAttack + self.weapon[1])
        return

    def takeDamage(self, num):
        if num < 1:
            num = 1
        self.setHealth(self.playerHP - num)
        if self.playerHP < 0:
            self.setHealth(0)

    def levelUp(self, prStats = 1):
        while True:
            if self.xp >= 25*(3*(int(self.level) + 1) + 2)*int(self.level):
                self.level = int(self.level) + 1
                if prStats == 1:
                    print(":::::::::::::: You've leveled up to ", self.level, "! ::::::::::::::\n", sep="")
                tempVal = self.playerAP
                self.setAttack(random.randint(self.playerAP + 10, self.playerAP + 15))
                if prStats == 1:
                    print("Attack Leveled Up +", self.playerAP - tempVal, sep="")
                tempVal = self.maxHP
                self.setmaxHP(random.randint(self.maxHP + 10, self.maxHP + 15))
                if prStats == 1:
                    print("HP Leveled Up +", self.maxHP - tempVal, sep="")
                tempVal = self.playerDefense
                self.setDefense(random.randint(self.playerDefense + 10, self.playerDefense + 15))
                if prStats == 1:
                    print("Defense Leveled Up +", self.playerDefense - tempVal, sep="")
                tempVal = self.maxMP
                self.setMaxMagic(random.randint(self.maxMP + 10, self.maxMP + 15))
                if prStats == 1:
                    print("MP Leveled Up +", self.maxMP - tempVal, "\n", sep="")
                self.setHealth(self.maxHP)
                self.setMagic(self.maxMP)
            else:
                break

    def addGold(self, num):
        self.gold = self.gold + num

    def removeGold(self, num):
        self.gold = self.gold - num

    def addXP(self, num):
        self.xp = self.xp + num

    def setLevel(self, num):
        self.addXP((25 * ((3 * num + 1) + 2) * (num - 1)) - self.xp)
        self.levelUp(0)

    def setLuck(self, num):
        self.luck = num


# make shopping better
# make who strikes first in battle
# work in magic
# add extra section to items for optional effects
# add extra section to items for sounds effects
# add armor
# add ways to equip different items
# add miss in combat (this will be a section in weapon attributes)
# add flee probability
# make a load sound function
# enemies have chance of health recovery
# give player ability to choose bonus perk
# Display Enemy's left during battle after stats or inventory usage


sounds = []

currentSong = "NULL"

player = entity()


def generateNpcEnemies(inList=[], curLvl=0, numEnem=0):
    global player
    minLvl = .5 * curLvl
    if numEnem == 0:
        orgv = int(random.randint(int(.5*curLvl), int(1.4*curLvl)))
        if orgv > curLvl:
            inList.append(entity(orgv))
            rand = random.randint(0, 4)
            if rand*player.luck > 2:
                inList.append(entity(orgv))
            return inList
        orgv = int(random.randint(int(.5 * curLvl), int(curLvl)))
        inList.append(entity(orgv))
        inList = generateNpcEnemies(inList, curLvl, numEnem + 1)
        return inList
    mean = 0
    for i in inList:
        mean += i.level
    mean = int(mean/numEnem)
    mew = int(map(mean, minLvl, curLvl, 1, 8))
    mew = abs(mew - 8)
    amountProbability = int(random.gauss(mew, map(mew, 0, 8, 1, 2)))
    if amountProbability > 8:
        amountProbability = 8
    if amountProbability < 0:
        amountProbability = 0
    if amountProbability > numEnem:
        inList.append(entity(int(random.gauss(mean, (.4 / 4) * mean))))
        inList = generateNpcEnemies(inList, curLvl, numEnem + 1)
        return inList
    return inList


def tempEnemyHelper():
    print("Level,Name,Weapon Separated by commas: ")
    tempVal = input()
    thing = tempVal.split(',')
    return thing


def battle():
    global player
    # numEnemies = int(input("How many enemies?"))
    # enemyList = []
    # xpAmount = 0
    # goldAmount = 0
    # for i in range(numEnemies):
    #     helperOutput = tempEnemyHelper()
    #     enemy = entity(int(helperOutput[0]), 0, helperOutput[1], weapons[int(helperOutput[2])])
    #     goldAmount = goldAmount + enemy.playerHP
    #     xpAmount = xpAmount + int(10*(int(enemy.level)/2))
    #     enemyList.append(enemy)
    # goldAmount = random.randint(int(goldAmount/6), int(goldAmount/3))
    #
    xpAmount = 0
    goldAmount = 0
    enemyList = []
    enemyList = generateNpcEnemies(enemyList, player.level)
    numEnemies = 0
    for i in enemyList:
        xpAmount = xpAmount + int(10*(int(i.level)/2)) + int(2000*(1-player.luck)) + 50
        goldAmount = goldAmount + i.playerHP
        numEnemies = numEnemies + 1
    goldAmount = random.randint(int(goldAmount/6), int(goldAmount/3))

    saveFile(0)

    playSong("BattleMusic")
    while True:
        if player.playerHP == 0:
            pygame.mixer.music.stop()
            print("YOU HAVE BEEN DEFEATED")
            pygame.mixer.Sound.play(sounds[3])
            time.sleep(3)
            playSong("Ded")
            print("GAME OVER")
            time.sleep(5)
            input("Press Enter:")
            pygame.mixer.music.fadeout(1000)
            loadFile(player.name)
            return
        if len(enemyList) == 0:
            playSong("FFWin")
            print("You are victorious!")
            player.addGold(2*goldAmount)
            player.addXP(2*xpAmount)
            print(goldAmount, "Gold Added!")
            print(xpAmount, "XP earned!")
            player.levelUp()
            input("Press Enter")
            saveFile(player)
            return
        tempNum = 1
        print("ENEMIES LEFT:")
        for i in enemyList:
            print(tempNum, ":",  i.name, "Lvl:", i.level, "::: HP:", i.playerHP)
            tempNum = tempNum + 1
        print("Your health:::", player.playerHP)
        
        action = menu_combat(numEnemies)
        
        if action == -1:
            '''enemyLevels = 0
            for i in enemyList:
                enemyLevels = enemyLevels + i.level
            x = player.level/(enemyLevels - .8*player.level)
            if x >= 1:
                print("You decided they weren't worth your time...")
            runProbability = (1/(math.exp(1.6*(x+1)-1.6)) - .2)
            canRun = '''
            print("Coward...")
            return
        if action == -3:
            for i in enemyList:
                attack(player, i, player.tempAttack)
            player.resetTempAttack()
        elif action == -2:
            for i in enemyList:
                attack(i, player, -1)
            continue
        else:
            attack(player, enemyList[action-1])
            for i in enemyList:
                if i.playerHP == 0:
                    enemyList.remove(i)
                    print(i.name, "has died...")
                    numEnemies -= 1
            for i in enemyList:
                attack(i, player)


def menu_main():
    global player
    while True:
        playSong("MenuMusic")
        print("_______Choose an action:_______\n:::0 - Quit Game:::\n"
              ":::1 - Enemy:::\n:::2 - Shop:::\n:::3 - Stats:::\n"
              ":::4 - Inventory:::\n:::5 - Save:::\n:::6 - Load:::\n:::"
              "7 - DEBUG add gold:::\n:::8 - DEBUG add level\n:::9 - DEBUG set weapon")
        selection =inputI(rangeB=0, rangeE=9)
        if selection == 0:
            print("Exit?... y/n")
            answer = input()
            if answer == 'y':
                print("Until next time traveller...")
                saveFile(player)
                exit()
        elif selection == 1:
            battle()
        elif selection == 2:
            shop()
        elif selection == 3:
            player.printStats()
        elif selection == 4:
            player.useInventory()
        elif selection == 5:
            saveFile()
        elif selection == 6:
            loadFile()
            if player == -1 or player == -2:
                pass
            else:
                print("Welcome back", player.name)
        elif selection == 7:
            player.addGold(int(input("How much? ::: ")))
            print(player.name, "has", player.gold, "gold.")
        elif selection == 8:
            player.setLevel(inputI("How much?", 0))
        elif selection == 9:
            weaponNum = inputI("Which one?", 0, 9)
            player.setWeapon(weaponNum)
            print(weapons[weaponNum], " equipped to ", player.name, ".", sep="")
        else:
            print("Not a valid selection.")


def menu_combat(numEnem):
    global player
    while True:
        print("[::: 1 - Attack ::: 2 - Defend ::: 3 - stats ::: 4 - Inventory ::: 5 - Run :::]")
        
        menu_combatnum = inputI(rangeB=1, rangeE=5)
        if menu_combatnum == 1:
            select = inputI("Who? ::: ", int(1), int(numEnem))
            return select
        if menu_combatnum == 2:
            return -2
        if menu_combatnum == 3:
            player.printStats()
            continue
        if menu_combatnum == 4:
                usedItem = player.useInventory(1)
                if usedItem == -1:
                    return -3
                continue
        if menu_combatnum == 5:
            return -1


def attack(goodGuys=entity(), badGuys=entity(), damage=0):
    if damage > 0:
        damage = int((damage * damage)/(damage + numpy.random.normal(badGuys.playerDefense*.8,
                                                                     badGuys.playerDefense*.15,
                                                                     1)))
        badGuys.takeDamage(damage)
        print(damage, " Damage on ", badGuys.name, "!")
        input()
        return
    elif damage < 0:
        damage = numpy.random.normal(goodGuys.playerAP*.8,
                                     goodGuys.playerAP*.15,
                                     1)
        damage = int((damage * damage)/(damage + numpy.random.normal(badGuys.playerDefense*.95,
                                                                     badGuys.playerDefense*.15,
                                                                     1)))
        badGuys.takeDamage(damage)
        pygame.mixer.Sound.play(sounds[2])
        print(damage, " Damage on ", badGuys.name, "!")
        input()
        pygame.mixer.Sound.play(sounds[0])
        return
    else:
        damage = numpy.random.normal(goodGuys.playerAP*.8, goodGuys.playerAP*.15,
                                     1)
        damage = int((damage * damage) / (damage + numpy.random.normal(badGuys.playerDefense*.8,
                                                                       badGuys.playerDefense*.15,
                                                                       1)))
        badGuys.takeDamage(damage)
        pygame.mixer.Sound.play(sounds[2])
        print(damage, " Damage on ", badGuys.name, "!")
        input()
        pygame.mixer.Sound.play(sounds[0])
        return


def shop():
    global player
    playSong("ShopMusic")
    print("Welcome traveler! What do you want to buy?")
    while True:
        print("What do you want to buy?")
        while True:
            print("1.) Shachee Potion --- 10\n2.) Bomb --- 50\n3.) Greater Shachee Potion --- 20\n"
                  "4.):::BACK:::")
            print("Your Gold:", player.gold)
            selection = int(input("Make a selection: "))
            if player.gold >= 10 and selection == 1:
                print("Thanks stranger.")
                player.pushInventory(items[0])
                player.removeGold(10)
                continue
            if player.gold >= 50 and selection == 2:
                player.pushInventory(items[1])
                print("Be careful with that.")
                player.removeGold(50)
                continue
            if player.gold >= 20 and selection == 3:
                player.pushInventory(items[4])
                player.removeGold(20)
                continue
            if selection == 4:
                break
            if 0 >= selection > 4:
                print("I don't have anything there stupid...")
            print("You don't have enough for that..")
        print("Is that all? y/n?")
        answer = input()
        if answer == 'y':
            print("Come again there, mate.")
            return


def loadFile(str=""):
    global player
    str = str + "_SAVE_.pkl"
    if str != "_SAVE_.pkl":
        try:
            with open(str, "rb") as file:
                profileWithInventory = pickle.load(file)
                profile = profileWithInventory[0]
                profile.inventory = profileWithInventory[1]
                player = profile
                return 1
        except:
            print("WARNING, the requested file can not be found...")
            return
    filesInHere = os.listdir()
    dotPklFiles = []
    for i in filesInHere:
        if i[len(i) - 10:] == "_SAVE_.pkl":
            dotPklFiles.append(i)

    if len(dotPklFiles) == 0:
        print("Cannot find any saves...")
        return -1
    tempNum = 1
    for i in dotPklFiles:
        print(tempNum, "___", i[:len(i) - 10], "___")
        tempNum = tempNum + 1
    print(tempNum, ":::EXIT:::")
    print("Which file do you want to load?")
    fileChoice = inputI(rangeB=1, rangeE=tempNum)
    if fileChoice == tempNum:
        return -2
    else:
        with open(dotPklFiles[fileChoice - 1], "rb") as tFile:
            profileWithInventory = pickle.load(tFile)
            profile = profileWithInventory[0]
            profile.inventory = profileWithInventory[1]
            player = profile
        return 1


def saveFile(polite=1):
    global player
    selec = 'y'
    if polite == 1:
        print("Save profile ", player.name, "? y/n", sep="")
        selec = input()
    if selec == 'y':
        with open(player.name + "_SAVE_.pkl", 'wb') as output:
            playerWithInventory = [player, player.inventory]
            pickle.dump(playerWithInventory, output, pickle.HIGHEST_PROTOCOL)
        if polite == 1:
            print(player.name, "saved...")
            input("Press Enter:")
    else:
        print("Save Canceled...")


def loadSound(file):
    file = os.path.join(main_dir, 'AudioFiles', file)
    try:
        sound = pygame.mixer.Sound(file)
        return sound
    except pygame.error:
        print('Unable to load file')
    return dummysound()


def audioInitialize(sound):
    for i in sound:
        sounds.append(loadSound(i+".wav"))


def playSong(file):
    global currentSong
    if file == currentSong:
        return
    currentSong = file
    music = os.path.join(main_dir, 'AudioFiles', file+".wav")
    pygame.mixer.music.stop()
    pygame.mixer.music.load(music)
    pygame.mixer.music.play(-1)


def main():
    global player
    pygame.mixer.init()
    soundList = ["Hit", "MenuSelect", "Swing", "DeathJingle"]
    audioInitialize(soundList)

    while True:
        print("1 - Load Profile, 2 - New Game")
        choice = inputI(rangeB=1, rangeE=2)
        if choice == 1:
            loadSuccess = loadFile()
            if loadSuccess == -1:
                print("No saves found...")
                continue
            if loadSuccess == -2:
                continue
            print("Welcome back", player.name)
            break
        elif choice == 2:
            newName = input("Name:")
            player = entity(20, 1, newName, weapons[0])

            print("Nice to meet you", player.name)
            saveFile(0)
            break
        else:
            print("Not a valid selection")
            continue
    menu_main()


def inputI(stri="", rangeB=-255, rangeE=255):
    while True:
        try:
            selection = int(input(stri))
            pygame.mixer.Sound.play(sounds[1])
            if rangeB > selection or selection > rangeE:
                print("Not a valid selection.")
                continue
            return selection
        except:
            print("Not a valid selection.")


if __name__ == "__main__":
    main()