from room import Room
from player import Player
from item import Item
from item import Chest
from item import Consumable
from item import Weapon
from item import Armor
from npc import NPC
from npc import Doctor
from npc import Merchant
from monster import Monster
import os
import updater
import system
import random

player = Player()


def create_world():
    a_3 = Room("Starting Room")
    b_3 = Room("Merchant's Hallway")
    c_3 = Room("Open Space")
    d_3 = Room("Treasure Room")
    e_3 = Room("The Room before the Boss")
    f_3 = Room("The Room with the Boss")

    c_2 = Room("Open Space")
    d_2 = Room("Doctor's Storage")
    e_2 = Room("Open Space")

    c_1 = Room("Doctor's Enterance (Southern)")
    d_1 = Room("Doctor's Office")
    e_1 = Room("Doctor's Enterance (Northern)")

    c_4 = Room("Open Space")
    d_4 = Room("Open Space")
    e_4 = Room("Straggler's Corner Enterance (Eastern)")

    c_5 = Room("Open Space")
    d_5 = Room("Straggler's Corner Enterance (Southern)")
    e_5 = Room("Straggler's Corner")

    Room.connect_rooms(a_3, "north", b_3, "south")
    Room.connect_rooms(b_3, "north", c_3, "south")
    Room.connect_rooms(c_3, "north", d_3, "south")
    Room.connect_rooms(d_3, "north", e_3, "south")
    Room.connect_rooms(e_3, "north", f_3, "south")

    Room.connect_rooms(c_1, "east", c_2, "west")
    Room.connect_rooms(c_2, "east", c_3, "west")
    Room.connect_rooms(c_3, "east", c_4, "west")
    Room.connect_rooms(c_4, "east", c_5, "west")

    Room.connect_rooms(d_1, "east", d_2, "west")
    Room.connect_rooms(d_3, "east", d_4, "west")
    Room.connect_rooms(d_4, "east", d_5, "west")

    Room.connect_rooms(e_1, "east", e_2, "west")
    Room.connect_rooms(e_2, "east", e_3, "west")
    Room.connect_rooms(e_3, "east", e_4, "west")
    Room.connect_rooms(e_4, "east", e_5, "west")

    Room.connect_rooms(c_1, "north", d_1, "south")
    Room.connect_rooms(d_1, "north", e_1, "south")

    Room.connect_rooms(c_4, "north", d_4, "south")
    Room.connect_rooms(d_4, "north", e_4, "south")

    Room.connect_rooms(c_5, "north", d_5, "south")
    Room.connect_rooms(d_5, "north", e_5, "south")

    pipe = Weapon("Iron Pipe", "Strong, but has incredibly low accuracy.", 55, 50, 20, 150)
    amb = Consumable("Ambrosia", "Grants +15 to Max HP, Max SP and +8 to all other stats. Highly valuable.", 3, 15, 8, "all", 1500, 1)
    boul = Item("Boullion", "A great amount of gold.", 5, 3000)
    salve = Consumable("Salve", "Use when injured. Heals 20 HP", 1, 20, 0, "heal", 250, 1)
    leather = Armor("Leather Chestplate", "Simple protection.", 8, 10, -5, 300)
    cape = Armor("Swift Cape", "Nimble, but not too protecting.", 4, 10, 10, 200)
    iron_chest = Armor("Iron Chestplate", "Heavy but durable.", 15, 35, -25, 500)
    good_sword = Weapon("Kingmaker", "A fine weapon, fit for a king.", 25, 25, 70, 1200)
    iron = Weapon("Iron Sword", "A common weapon.", 8, 10, 70, 400)
    slim = Weapon("Slim Sword", "A lightweight blade.", 4, 25, 90, 200)
    win_cond = Item("Wedding Ring", "Your fiance told you not to come back until you could afford this.", 0, 7500)
    chest_1 = Chest("Chest", "A locked chest.", 100000, 10, amb)
    chest_1.put_in_room(d_2)
    chest_2 = Chest("Chest", "A locked chest.", 100000, 10, boul)
    chest_2.put_in_room(d_4)
    wares = [pipe, salve, iron, slim, good_sword, leather, cape, iron_chest, win_cond]
    player.location = a_3
    Monster("Slime", 2, c_3)
    Monster("Phantasm", 1, d_5)
    Monster("Imp", 2, e_1)
    Monster("Boss", 10, f_3)
    Monster("Straggler", 5, e_5)
    Merchant("Merchant", "Sells some interesting wares.", b_3, wares)
    Doctor("Doctor", "Heals, for a price.", d_1)

    free_rooms = [c_2, e_2, c_1, e_1, d_3, e_3, c_4, d_4, e_4, c_5, d_5]
    return free_rooms

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_situation():
    clear()
    print(player.location.desc)
    print()
    if player.location.has_monsters():
        print("This room contains the following monsters:")
        for m in player.location.monsters:
            print(m.name)
        print()
    if player.location.has_npcs():
        print("This room contains the following NPCS:")
        for m in player.location.npcs:
            print(m.name)
        print()
    if player.location.has_items():
        print("This room contains the following items:")
        for i in player.location.items:
            print(i.name)
        print()
    print("You can go in the following directions:")
    for e in player.location.exit_names():
        print(e)
    print()

def show_help():
    clear()
    print("go <direction> -- moves you in the given direction")
    print("inventory/inv/i -- opens your inventory")
    print("me/m -- displays information about yourself")
    print("pickup/take/p/t <item> -- picks up the item")
    print("inspect/ins <item> -- displays information about an item")
    print("drop/d <item> -- removes item from your inventory")
    print("equip/eq/e <item> -- equips item")
    print("wait/w -- allows the passage of one time-unit")
    print("use/u <item> -- consumes item")
    print("use/u chest key --uses key in a room with a chest")
    print("converse/c <npc> -- interacts with NPCs in room")
    print("attack/fight/a/f <enemy> -- initiates combat with enemy in a room")
    print("quit/exit/q/e -- quits the game")
    print()
    input("Press enter to continue...")


if __name__ == "__main__":
    free_rooms = create_world()
    playing = True
    time_counter = 0
    win = False
    while (playing and player.alive) and (not win):
        if player.is_in_inventory("Wedding Ring"): # check win condition; if player has wedding ring
            win = True
            break
        if (time_counter % 6 == 0): # summon slime randomly every 6 timesteps, if free spaces exist
            rand_pos = random.randint(0, len(free_rooms)-1)
            if (free_rooms[rand_pos].has_monsters() == False):
                Monster("Slime", player.level, free_rooms[rand_pos])
        if (time_counter % 11 == 0):# summon imp randomly every 11 timesteps, if free spaces exist
            rand_pos = random.randint(0, len(free_rooms)-1)
            if (free_rooms[rand_pos].has_monsters() == False):
                Monster("Imp", player.level, free_rooms[rand_pos])
        if (time_counter % 15 == 0):# summon phantasm randomly every 15 timesteps, if free spaces exist
            rand_pos = random.randint(0, len(free_rooms)-1)
            if (free_rooms[rand_pos].has_monsters() == False):
                Monster("Phantasm", player.level, free_rooms[rand_pos])
        print_situation()
        command_success = False
        time_passes = False
        while not command_success:
            command_success = True
            command = input("What now? ")
            if len(command) == 0:
                continue
            command_words = command.split()
            if len(command_words) == 0:
                continue
            match command_words[0].lower():
                case "go":   #cannot handle multi-word directions
                    okay = player.go_direction(command_words[1]) 
                    if okay:
                        time_passes = True
                    else:
                        print("You can't go that way.")
                        command_success = False
                case "pickup" | "p" | "take" |"t":  #can handle multi-word objects
                    target_name = command[(len(command_words[0])+1):] # everything after "pickup "
                    target = player.location.get_item_by_name(target_name)
                    if target != False: # check if item exists in room
                        if player.can_pickup(target): # check if player has enough storage
                            player.pickup(target)
                        else:
                            print("Cannot pickup item. Not enough inventory space.")
                            command_success = False
                    else:
                        print("No such item.")
                        command_success = False
                case "use" | "u":  #can handle multi-word objects
                    target_name = command[(len(command_words[0])+1):] # everything after "use "
                    target = player.is_in_inventory(target_name)
                    if target != False:
                        if (target.is_consumable()): # check if item is consumable
                            clear()
                            target.consume(player)
                        elif (target.name == "Chest Key"): # check if item is chest key
                            chest = player.location.get_item_by_name("Chest")
                            if chest != False:
                                chest.unlock(player)
                        else:
                            print(f"Cannot use {target.name}")
                            command_success = False
                    else:
                        print("Item does not exist within inventory.")
                        command_success = False
                case "inspect" | "ins":  #can handle multi-word objects
                    target_name = command[(len(command_words[0])+1):] # everything after "inspect "
                    target = player.is_in_inventory(target_name) # check if target is in inventory
                    if target != False:
                        clear()
                        target.describe()
                    else: 
                        target = player.location.get_item_by_name(target_name)
                        if target != False: # check if target in the current room
                            clear()
                            target.describe()
                        else:
                            print("Item cannot be found.")
                            command_success = False
                case "equip" | "eq" | "e":  #can handle multi-word objects
                    target_name = command[(len(command_words[0])+1):] # everything after "equip "
                    target = player.is_in_inventory(target_name)
                    if target != False: # check if item is in inventory
                        clear()
                        if (target.is_equippable()): # check if it is equippable
                            if (target.is_weapon()): # check if it is a wepaon
                                clear()
                                player.equip_weapon(target)
                            else: # case where item is not a weapon, aka, a piece of armor
                                clear()
                                player.equip_armor(target)
                        else:
                            print(f"Cannot equip {target.name}")
                            command_success = False
                    else:
                        print("Item does not exist within inventory.")
                        command_success = False
                case "drop" | "d":  #can handle multi-word objects
                    target_name = command[(len(command_words[0])+1):] # everything after "drop "
                    target = player.is_in_inventory(target_name)
                    if target != False: # check if item is in inventory
                        player.drop(target)
                    else:
                        print("Item does not exist within inventory.")
                        command_success = False
                case "inventory" | "inv" | "i": # display inventory
                    player.show_inventory()
                case "converse" | "c": # converse function, check if npc is available, then interact with them if so, according to their profession.
                    target_name = command[(len(command_words[0])+1):]
                    target = player.location.get_npc_by_name(target_name)
                    if target != False:
                        npc_type = target.npc_type() 
                        if (npc_type == "merchant"): # check if npc is merchant or doctor.
                            system.store(player, target)
                        elif (npc_type == "doctor"):
                            system.doctor(player, target)
                        time_passes = True
                    else:
                        print("No such person.")
                        command_success = False
                case "help" | "h":
                    show_help()
                case "exit" | "quit" | "ex" | "q":
                    playing = False
                case "me" | "m": # show information about self
                    player.show_status()
                case "wait" | "w": # wait function
                    time_passes = True
                case "attack" | "a" | "fight" | "f": #attacking case
                    target_name = command[(len(command_words[0])+1):]
                    target = player.location.get_monster_by_name(target_name)
                    if target != False: # check if monster exists, then initiate attacking routine if so
                        turn_count = system.combat(player, target)
                        if (turn_count != False):
                            time_counter += (turn_count // 2)
                        time_passes = True
                    else:
                        print("No such monster.")
                        command_success = False
                case "seichusengodanzuki": #debug functions testing win condiitons
                    time_counter = 0
                    win = True
                case "abaretosanamikudaki": #debug functions testing win condiitons
                    time_counter = 50
                    win = True
                case "tandenrenkisemenokata": #debug functions testing win condiitons
                    time_counter = 100
                    win = True
                case other:
                    print("Not a valid command")
                    command_success = False
        if time_passes == True:
            time_counter += 1
            updater.update_all()
    clear()
    if (win):
        if (time_counter < 75): # good ending, lowest time count
            print()
            print("You managed to get the wedding ring in quick time!")
            print("Your fiance is fairly happy about the ring, but they don't quite remember asking for it...")
            print("Then, who could have disguised as your fiance?")
            print("Turns out, the quest for the ring was a ploy by Walmart to colonize the dungeon and the merchant was colluding with them!")
            print("The merchant had disguised as your fiance, but could not escape in time to complete the perfect crime.")
            print("Not only that, but the ring costs 50 gold normally!")
            print("However, your fiance still greatly appreciates your efforts!")
            print()
            print("the end?")
        elif (time_counter < 150): # neutral ending, moderate time count
            print()
            print("You managed to get the wedding ring!")
            print("Your fiance was worried sick, but is delighted to see you return back!")
            print("The question still stands that the question of who sent you on that quest...")
            print("However, your fiance still appreciates your efforts!")
            print()
            print("the end?")
        else: # bad ending, high time count
            print()
            print("You managed to get the wedding ring!")
            print("However, your fiance was fairly unhappy about you being gone for a long time...")
            print("You should apologize to them sometime.")
            print()
            print("the end?")

