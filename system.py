import os
import system
import random

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def attack_enemy(player, enemy):
    clear()
    print()
    print(enemy.name + " draws near!")
    print()
    print("Your health is " + str(player.health) + ".")
    print(enemy.name + "'s health is " + str(enemy.health) + ".")
    print()
    while ((player.health >= 0) and (enemy.health >= 0)):
        player_phase = True
        while player_phase:
            player_phase = False
            command = input("What action would you like to take? ")
            if len(command) == 0:
                continue
            command_words = command.split()
            if len(command_words) == 0:
                continue
            match command_words[0].lower():
                case "inventory":
                    player.show_inventory()
                    player_phase = True
                case "use":  #can handle multi-word objects
                    target_name = command[4:] # everything after "use "
                    target = player.is_in_inventory(target_name)
                    if target != False:
                        target.consume(player)
                    else:
                        print("Item does not exist within inventory.")
                        player_phase = True
                case "me":
                    player.show_status()
                    player_phase = True
                case "enemy":
                    enemy.show_status()
                    player_phase = True
                case "attack":
                    clear()
                    print()
                    print("Player attacks!")
                    print()
                    chance = random.randint(1,100)
                    if (chance <= player.weapon.acc):
                        dmg_dealt = player.atk + player.weapon.atk - enemy.defe
                        if (dmg_dealt < 0):
                            dmg_dealt = 0
                        print(f"{enemy.name} takes {dmg_dealt} damage!")
                        enemy.health -= dmg_dealt
                    else:
                        print(f"Player misses!")                        
                case other:
                    print("Not a valid command")
                    player_phase = True
        print()
        print(f"{enemy.name} attacks!")
        print()
        chance = random.randint(1,100)
        if (chance <= enemy.acc + player.armor.wgt):
            dmg_dealt = enemy.atk - player.defe
            if (dmg_dealt < 0):
                dmg_dealt = 0
            print(f"Player takes {dmg_dealt} damage!")
            player.health -= dmg_dealt
        else:
            print(f"{enemy.name} misses!")          
    if player.health >= 0:
        print("You win!")
        exp = (enemy.level//player.level) + 3
        print("Awarded " + str(exp) + " exp.")
        gold = enemy.gold
        print("Awarded " + str(gold) + "G.")
        enemy.die()
        player.exp += exp
        player.level_up()
    else:
        print("You lose.")
        player.alive = False
    print()
    input("Press enter to continue...")

def store(player, merchant):
    clear()
    print()
    print("Welcome!")
    print()
    command_success = False
    while not command_success:
        command_success = True
        command = input("What action would you like to take? (buy/sell/leave)")
        if len(command) == 0:
            continue
        command_words = command.split()
        if len(command_words) == 0:
            continue
        match command_words[0].lower():
                case "buy":
                    clear()
                    store_buy(player, merchant)
                case "sell":
                    clear()
                    store_sell(player, merchant)
                case "leave":
                    clear()
                    print("Thanks for stopping by!")
                    return
                case other:
                    print()
                    print("I'm not quite sure what you're asking.")
                    print()
                    command_success = False

def store_buy(player, merchant):
    buying = True
    while buying:
        command_success = False
        while not command_success:
            print()
            print("Here are my wares:")
            for item in merchant.items:
                print(f"{item.name}: f{item.value}")
            print()
            command_success = True
            command = input("What action would you like to take? (buy <item>/inspect <item>) ")
            if len(command) == 0:
                continue
            command_words = command.split()
            if len(command_words) == 0:
                continue
            match command_words[0].lower():
                case "inspect":  #can handle multi-word objects
                    target_name = command[8:] # everything after "inspect "
                    target = merchant.is_in_inventory(target_name)
                    if target != False:
                        clear()
                        target.describe()
                    else:
                        print("I'm not quite sure what item you're specifying.")
                        command_success = False
                case "buy":
                    target_name = command[4:] # everything after "buy "
                    target = merchant.is_in_inventory(target_name)
                    if target != False:
                        if (player.can_buy(target)):
                            player.buy(target)
                            merchant.items.remove(target)
                            print("Many thanks!")
                        else:
                            print("Sorry, you don't have enough gold to purchase this item.")
                            command_success = False
                    else:
                        print("I'm not quite sure what item you're specifying.")
                        command_success = False
                case "back":
                    clear()
                    buying = False
                case other:
                    print()
                    print("I'm not quite sure what you're asking.")
                    print()
                    command_success = False

def store_sell(player, merchant):
    selling = True
    while selling:
        command_success = False
        while not command_success:
            print()
            command_success = True
            command = input("What would you like to sell? (sell <item>/back) ")
            if len(command) == 0:
                continue
            command_words = command.split()
            if len(command_words) == 0:
                continue
            match command_words[0].lower():
                case "sell":
                    target_name = command[5:] # everything after "sell "
                    target = player.is_in_inventory(target_name)
                    if target != False:
                        player.gold += target.value
                        player.items.remove(target)
                        print("Many thanks!")
                    else:
                        print("You do not seem to have that item.")
                        command_success = False
                case "back":
                    clear()
                    selling = False
                case other:
                    print()
                    print("I'm not quite sure what you're asking.")
                    print()
                    command_success = False
