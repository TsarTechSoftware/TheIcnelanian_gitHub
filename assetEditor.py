import source
import pickle
import os

statusEffects = {"Frost": (2,), "Drain Soul": (8, 3), "Blaze": (1, 4), "Lucky": (5,), "Greater": (6,)}
statusModifiers = {0: "AP", 1: "Damage", 2: "Turns to Effect", 3: "Continuous", 4: "Hurts All",
                   5: "Percent Factor", 6: "attack,defence,health,mgk,luck",
                   7: "amout,amt,amt,amt,amt", 8: "Hurt Specific", 9: "Effect Name"}

def mainMenu():
    print("Welcome to the asset editor")
    print("1 - Weapon Editor")
    ans = int(input())
    if ans == 1:
        editWeapons()

'''def characterBuilder():
    level = 1
    gold = 0
    xp = 0
    maxHealth = 0
    playerHealth = 0
    defense_player = 0
    mp_player_max = 0
    mp_player = 0
    attackPower_player = 0
    name = ""
    weapon = ("NULL", 0)
    inventory = []
    tempAttack = 0
    lvl = input("Level:")
    character = source.entity()'''

# creator for specific shop owners

def editWeapons():
    ''' [0] = It's base damae amount, [1] = Damage, [2] = Turns to Effect,
        [3] = Continuous, [4] Hurts All Opponents,
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
    weaponList = []
    try:
        with open("weapon_assets_AST_.pkl", "rb") as weapons:
            weaponList = pickle.load(weapons)
    except Exception:
        print("Creating new directory")
        weaponsTemp = [()]
        saveWeaponList(weaponsTemp)
    for i in weaponList:
        print("###", i, "###")
    while True:
        print("0 - BACK, 1 - Create New Weapon, 2 - Edit Weapon, 3 - Move Order, 4 - Print Readable List")
        choice = inputI("", 0, 4)
        if choice == 0:
            return
        elif choice == 1:
            weapon = createNewWeapon()
            weaponList.append(weapon)
            saveWeaponList(weaponList)
        elif choice == 2:
            editSpecificWeapon(weaponList)
        elif choice == 4:
            for i in weaponList:
                print("###", i, "###")


def saveWeaponList(wl=[]):
    with open("weapon_assets_AST_.pkl", "wb") as weapons:
        pickle.dump(wl, weapons, pickle.HIGHEST_PROTOCOL)


def createNewWeapon():
    while True:
        weapon = []
        weapon.append(input("Name:"))
        statusEffect = input("Special status Effects? Enter \'None\' for none:")
        if statusEffect == "None":
            weapon.append((int(input("AP:")), 0, 0, 0, 0, "", "", 0, ""))
        else:
            effectTuple = [0, 0, 0, 0, 0, "", "", 0, statusEffect]
            for i in statusEffects[statusEffect]:
                print(statusModifiers[i])
                effectTuple[i] = input("How much?:")
            effectTuple[0] = input("AP:")
            weapon.append(tuple(effectTuple))
        weapon.append(input("What sound?:"))
        weapon[0] = statusEffect + " " + weapon[0]
        print(weapon)
        print("Does this look correct? 0 - BACK, 1 - yes, 2 - no")
        ans = inputI("", 0, 2)
        if ans == 0:
            return
        if ans == 1:
            return tuple(weapon)


def editSpecificWeapon(weaponList):
    while True:
        indxr = 1
        for i in weaponList:
            print("###", indxr, i, "###")
            indxr += 1
        print("Which do you want to edit?, 0 - BACK")
        ans = inputI("", 0, len(weaponList))
        if ans == 0:
            return
        while True:
            print(weaponList[ans - 1])
            print("0 - BACK, 1 - Edit, 2 - Delete")
            otherAns = inputI("", 0, 2)
            if otherAns == 0:
                break
            if otherAns == 1:
                while True:
                    originalWep = weaponList[ans - 1]
                    wep = []
                    for i in originalWep:
                        wep.append(i)
                    print("What do you want to edit?")
                    print("0 - BACK:\n", "1 - Name: ", wep[0], "\n", "2 - AP: ",
                          wep[1][0], "\n", "3 - Modifier: ", wep[1][8], "\n", wep[1][1:7],
                          "\n", "4 - Sound: ", wep[2], sep="")
                    editChoice = inputI("", 0, 4)
                    if editChoice == 0:
                        break
                    elif editChoice == 1:
                        print(wep[0])
                        wep[0] = input("New Name:")
                    elif editChoice == 2:
                        tempTup = []
                        for i in wep[1]:
                            tempTup.append(i)
                        tempTup[0] = input("AP:")
                        wep[1] = tuple(tempTup)
                    elif editChoice == 3: # TODO Need to remove name of status effect
                        if wep[1][8] != "None":
                            tempName = wep[0].split(" ")
                            tempName.remove(tempName[0])
                            for i in tempName:
                                wep[0] += i
                        thingTuple = [wep[1][0], 0, 0, 0, 0, "", "", 0, ""]
                        # Asking for a new status effect and adding the values accordingly
                        thingTuple[8] = input("New Effect:")
                        for i in statusEffects[thingTuple[8]]:
                            print(statusModifiers[i])
                            thingTuple[i] = input("New Value:")
                        # Adding it back in to the weapon
                        wep[1] = tuple(thingTuple)
                        wep[0] = thingTuple[8] + " " + wep[0]
                    print("Does this look correct? y/n\n", "1 - Name: ", wep[0], "\n", "2 - AP: ",
                          wep[1][0], "\n", "3 - Modifier: ", wep[1][8], "\n", wep[1][1:7],
                          "\n", "4 - Sound: ", wep[2], sep="")
                    if input() == "y":
                        weaponList.remove(weaponList[ans - 1])
                        weaponList.insert(ans - 1, tuple(wep))
                        saveWeaponList(weaponList)
                        continue
            else:
                weaponList.remove(weaponList[ans - 1])
                saveWeaponList(weaponList)

# armor data editor

# potion data editor

# spell editor

# name database editor

# level randomness threshold editor (Nalshad'aar lvl 20 has typicial max healh of x)

# name assignment data editor with randomness seed (lvl 20 people are usually nalshad'arr)


def inputI(stri="", rangeB=-255, rangeE=255):
    while True:
        try:
            selection = int(input(stri))
            if rangeB > selection or selection > rangeE:
                print("Not a valid selection.")
                continue
            return selection
        except:
            print("Not a valid selection.")


def main():
    mainMenu()


if __name__ == "__main__":
    main()