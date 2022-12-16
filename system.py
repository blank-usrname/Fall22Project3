import os
import random

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def combat_help():
    clear()
    print("inventory/inv/i -- opens your inventory")
    print("me/m -- displays information about yourself")
    print("enemy/en -- displays information about yourself")
    print("inspect/ins <item> -- displays information about an item in inventory")
    print("equip/eq/e <item> -- equips item")
    print("use/u <item> -- consumes item")
    print("attack/a -- deals damage to enemy")
    print("run/r -- initiates running against enemy")
    print()
    input("Press enter to continue...")

def combat(player, enemy):
    """
    Reworked combat system, functions similar to the main game loop in main.py.
    Loop runs while both parties have greater than 0 HP.
    Player can choose to display inventory, status of self or enemy, use certain items (consumable),
    change equipment mid battle, attack, or run.
    """
    clear()
    print()
    print(enemy.name + " draws near!")
    turn_count = 0 # recorded and returned for the eventual calculation of determining which ending is achieved (2 turn_counts adds 1 to time_counter)
    while ((player.health > 0) and (enemy.health > 0)):
        print()
        print("Your health is " + str(player.health) + ".")
        print(enemy.name + "'s health is " + str(enemy.health) + ".")
        print()
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
                case "inventory" | "inv" | "i": # display inventory
                    player.show_inventory()
                    player_phase = True
                case "use" | "u":  #can handle multi-word objects
                    target_name = command[(len(command_words[0])+1):] # everything after "use "
                    target = player.is_in_inventory(target_name)
                    if target != False: # check if item is in inventory
                        if (target.is_consumable()): # check if item is consumable
                            clear()
                            target.consume(player)
                        else:
                            print(f"Cannot use {target.name}")
                            player_phase = True
                    else:
                        print("Item does not exist within inventory.")
                        player_phase = True
                case "me" | "m": # display information about self
                    player.show_status()
                    player_phase = True
                case "equip" | "eq" | "e":  #can handle multi-word objects
                    target_name = command[(len(command_words[0])+1):] # everything after "equip "
                    target = player.is_in_inventory(target_name) # checks if item is in inventory
                    if target != False:
                        if (target.is_equippable()): # checks if item is equippable, and whether it is a weapon or armor
                            if (target.is_weapon()):
                                clear()
                                player.equip_weapon(target)
                            else:
                                clear()
                                player.equip_armor(target)
                        else:
                            print(f"Cannot equip {target.name}")
                            player_phase = True
                    else:
                        print("Item does not exist within inventory.")
                        player_phase = True
                case "enemy" | "en": # display information about enemy
                    enemy.show_status()
                    player_phase = True
                case "attack" | "a": # attack, more info displayed in attack function.
                    attack(player, enemy)
                case "run" | "r": # run from battle, guaranteed if player's speed is greater than enemies, otherwise, 50/50 chance of success.
                    chance = random.random()
                    if (player.spd > enemy.spd or chance <= .5):
                        enemy.health = enemy.mhp
                        return turn_count
                    else:
                        print()
                        print("Attempt failed!")
                        print()
                        player_phase = False
                case other:
                    print("Not a valid command")
                    player_phase = True
        print()
        turn_count += 1
        if (enemy.health > 0): # check if enemy died before they could take an action.
            enemy.behavior(player)
            print()    
    if player.health > 0: # case where player wins battle
        print("You win!") 
        exp = enemy.exp # player exp and gold gain determined from enemy.
        print("Awarded " + str(exp) + " exp.")
        gold = enemy.gold
        print("Awarded " + str(gold) + "G.")
        drops = enemy.drop()
        if (drops != False): # checks if enemy dropped any items
            print(f"{enemy.name} dropped {drops.name}!")
            if (drops.wgt + player.curr_carry > player.carry): # checks if player can fit item into inventory
                print(f"Player picked up {drops.name}... then promptly set it down as they have no more inventory space.")
            else:
                print(f"Player picked up {drops.name}.") 
                player.pickup(drops)
        enemy.die()
        player.exp += exp # player exp and gold gain awarded
        player.gold += gold
        player.level_up() # level up function, checks if level up conditions is met and performs level up routine if so.
        print()
        input("Press enter to continue...")
        return turn_count 
    else: # condition where player dies in battle
        print("You lose.")
        print()
        input("Press enter to continue...")
        player.alive = False
        return False
    

# attack routine, checks if initiator hits, and deals damage to target if so.
# NOTE: attack function is agnostic of who is initiator or target, enemies also utilize attack function against player
def attack(party, target):
    print()
    print(f"{party.name} attacks!")
    print()
    chance = random.randint(1,100) # checks hit rate
    if (chance <= party.get_acc()-target.get_eva()): # if random number is less than attacker's accuracy minus the target's evasion, attacker hits
        dmg_dealt = party.get_dmg(target) # returns damage dealt
        if (dmg_dealt < 0): # makes sure damage dealt isn't negative
            dmg_dealt = 0
        print(f"{target.name} takes {dmg_dealt} damage!")
        target.health -= dmg_dealt
    else:
        print(f"{party.name} misses!")   

# store routine
def store(player, merchant):
    clear()
    print()
    print("Welcome!")
    print()
    command_success = False
    while not command_success: # check for whether or not player decides to buy, sell, or leave
        command_success = True
        command = input("What action would you like to take? ([b]uy/[s]ell/[l]eave)")
        if len(command) == 0:
            continue
        command_words = command.split()
        if len(command_words) == 0:
            continue
        match command_words[0].lower():
            case "buy" | "b":
                clear()
                store_buy(player, merchant) # choosing buy leads into the store purchase function,
                command_success = False
            case "sell" | "s":
                clear()
                store_sell(player, merchant)
                command_success = False
            case "leave" | "l" | "exit" | "e":
                clear()
                print("Thanks for stopping by!")
                command_success = True
            case other:
                print()
                print("I'm not quite sure what you're asking.")
                print()
                command_success = False

# store purchase function
def store_buy(player, merchant):
    buying = True
    while buying:
        command_success = False
        while not command_success:
            print()
            print("Here are my wares:")
            for item in merchant.items:
                print(f"{item.name}: {item.value}")
            print()
            command_success = True
            command = input("What action would you like to take? ([b]uy <item>/[i]nspect <item>/cancel) ")
            if len(command) == 0:
                continue
            command_words = command.split()
            if len(command_words) == 0:
                continue
            match command_words[0].lower():
                case "inspect" | "i":  #inspect is similar in function to inspect in overworld
                    target_name = command[(len(command_words[0])+1):] # everything after "inspect "
                    target = merchant.is_in_inventory(target_name)
                    if target != False:
                        clear()
                        target.describe()
                    else:
                        print("I'm not quite sure what item you're specifying.")
                        command_success = False
                case "buy" | "b": # buy case, 
                    target_name = command[(len(command_words[0])+1):] # everything after "buy "
                    target = merchant.is_in_inventory(target_name)
                    if target != False:
                        if (player.can_buy(target)): # checks if player has enough money
                            if (target.wgt + player.curr_carry > player.carry): # checks if player can carry item
                                print("You cannot hold this item in your inventory.")
                                command_success = False
                            else: # both conditions fulfilled
                                player.buy(target) # item added in player's inventory, gold taken
                                merchant.sell(target) # item removed from merchant's inventory if item is not consumable
                                print("Many thanks!")
                        else:
                            print("Sorry, you don't have enough gold to purchase this item.")
                            command_success = False
                    else:
                        print("I'm not quite sure what item you're specifying.")
                        command_success = False
                case "cancel" | "c": # return to first menu
                    clear()
                    buying = False
                case other:
                    print()
                    print("I'm not quite sure what you're asking.")
                    print()
                    command_success = False
        
# store sell function
def store_sell(player, merchant):
    selling = True
    while selling:
        command_success = False
        while not command_success:
            print()
            command_success = True
            command = input("What would you like to sell? ([s]ell <item>/[i]nspect <item (in player inventory)>/[c]ancel) ")
            if len(command) == 0:
                continue
            command_words = command.split()
            if len(command_words) == 0:
                continue
            match command_words[0].lower():
                case "sell" | "s": #
                    target_name = command[(len(command_words[0])+1):] # everything after "sell "
                    target = player.is_in_inventory(target_name) 
                    if target != False: # checks if item specified is in plaer's inventory
                        player.sell(target) # player sells item
                        print("Many thanks!")
                    else:
                        print("You do not seem to have that item.")
                        command_success = False
                case "inspect" | "i":  #inspect is similar in function to inspect in overworld
                    target_name = command[(len(command_words[0])+1):] # everything after "inspect "
                    target = player.is_in_inventory(target_name)
                    if target != False:  # checks if item specified is in plaer's inventory
                        target.describe()
                    else:
                        print("Item not found.") 
                        command_success = False
                case "cancel" | "c": # return to original menu
                    clear()
                    selling = False
                case other:
                    print()
                    print("I'm not quite sure what you're asking.")
                    print()
                    command_success = False

#doctor function, describes behavior of doctor
def doctor(player, doctor):
    doctoring = True
    print()
    print("Hello. I can offer healing for you.")
    while doctoring:
        command_success = False
        while not command_success:
            if (player.mhp == player.health): # check if player is already at max HP,
                print("It seems you are already at good health!")
                doctoring = False
                command_success = True
            else:
                cost = (player.mhp - player.health) * 5 # fee is intentionally less per HP compared to salve, but requires being able to pay off to heal to max hp,
                # and requires trekking to doctor's office.
                print(f"It will cost {cost} gold to heal you.")
                command_success = True
                command = input(f"Would you like to request healing today? ([y]es/[n]o) ")
                if len(command) == 0:
                    continue
                command_words = command.split()
                if len(command_words) == 0:
                    continue
                match command_words[0].lower():
                    case "yes" | "y": # player asks for healing
                        if (player.gold < cost): # checks if player can purchase healing services
                            print("Sorry, you do not have enough gold.")
                        else: # heals player to max health, takes service fee
                            player.gold -= cost
                            player.health = player.mhp
                            print("You have been healed!")
                            doctoring = False
                    case "no" | "n" | "cancel" | "c": # end doctor session
                        clear()
                        doctoring = False
                    case other:
                        print()
                        print("I'm not quite sure what you're asking.")
                        print()
                        command_success = False
    print()
    print("Have a good day.")
    print()
    input("Press enter to continue...")
