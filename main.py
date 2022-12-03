from room import Room
from player import Player
from item import Item
from item import Consumable
from item import Weapon
from item import Armor
from npc import NPC
from npc import Merchant
from monster import Monster
import os
import updater
import system

player = Player()


def create_world():
    a_1 = Room("You are in room 1")
    a_2 = Room("You are in room 2")
    a_3 = Room("You are in room 3")
    a_4 = Room("You are in room 4")
    Room.connect_rooms(a_1, "east", a_2, "west")
    Room.connect_rooms(a_3, "east", a_4, "west")
    Room.connect_rooms(a_1, "north", a_3, "south")
    Room.connect_rooms(a_2, "north", a_4, "south")
    pipe = Weapon("Iron Pipe", "Strong, but only hits 1/4 of the time.", 15, 40, 25, 250)
    armor = Armor("Diamond chestplate", "testing different armors.", 10, 10, 1000)
    i = Item("Rock", "This is just a rock.", 10, 0)
    j = Consumable("Ambrosia", "Grants +10 to Max HP and +5 to all other stats.", 3, 10, 5, "all", 3500)
    test_unpurchasable = Item("test_item", "you should not purchase this item!", 40, 10000000)
    test_item = Consumable("Salve", "Use when injured. Heals 20 HP", 1, 20, 0, "heal", 100)
    test_weapon = Weapon("Excalipoor", "A legendary sword?.", 3, 25, 80, 1000)
    wares = [test_unpurchasable, test_item, test_weapon]
    pipe.put_in_room(a_1)
    i.put_in_room(a_2)
    j.put_in_room(a_1)
    player.location = a_1
    Monster("Slime", 1, a_2)
    Merchant("test", "test_merchant", a_1, wares)

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
    print("inventory -- opens your inventory")
    print("me -- displays information about yourself")
    print("pickup <item> -- picks up the item")
    print("inspect <item> -- displays information about an item")
    print("drop <item> -- removes item from your inventory")
    print("equip <item> -- equips item")
    print("use <item> -- equips item")
    print("store -- brings up store")
    # print("save <file1/file2/file3> -- saves current session to file")
    # print("load <file1/file2/file3> -- saves current session to file")
    print("quit -- quits the game")
    print()
    input("Press enter to continue...")


if __name__ == "__main__":
    create_world()
    playing = True
    while playing and player.alive:
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
                case "pickup":  #can handle multi-word objects
                    target_name = command[7:] # everything after "pickup "
                    target = player.location.get_item_by_name(target_name)
                    if target != False:
                        if player.can_pickup(target):
                            player.pickup(target)
                        else:
                            print("Cannot pickup item. Not enough inventory space.")
                            command_success = False
                    else:
                        print("No such item.")
                        command_success = False
                case "use":  #can handle multi-word objects
                    target_name = command[4:] # everything after "use "
                    target = player.is_in_inventory(target_name)
                    if target != False:
                        if (target.is_consumable()):
                            clear()
                            target.consume(player)
                        else:
                            print(f"Cannot use {target.name}")
                            command_success = False
                    else:
                        print("Item does not exist within inventory.")
                        command_success = False
                case "inspect":  #can handle multi-word objects
                    target_name = command[8:] # everything after "inspect "
                    target = player.is_in_inventory(target_name)
                    if target != False:
                        clear()
                        target.describe()
                    else:
                        target = player.location.get_item_by_name(target_name)
                        if target != False:
                            clear()
                            target.describe()
                        else:
                            print("Item cannot be found.")
                            command_success = False
                case "equip":  #can handle multi-word objects
                    target_name = command[6:] # everything after "equip "
                    target = player.is_in_inventory(target_name)
                    if target != False:
                        clear()
                        if (target.is_equippable()):
                            if (target.is_weapon()):
                                clear()
                                player.equip_weapon(target)
                            else:
                                clear()
                                player.equip_armor(target)
                        else:
                            print(f"Cannot equip {target.name}")
                            command_success = False
                    else:
                        print("Item does not exist within inventory.")
                        command_success = False
                case "drop":  #can handle multi-word objects
                    target_name = command[5:] # everything after "drop "
                    target = player.is_in_inventory(target_name)
                    if target != False:
                        player.drop(target)
                    else:
                        print("Item does not exist within inventory.")
                        command_success = False
                case "inventory":
                    player.show_inventory()
                case "store":
                    target_name = command[6:]
                    target = player.location.get_npc_by_name(target_name)
                    if target != False:
                        system.store(player, target)
                    else:
                        print("No such monster.")
                        command_success = False
                case "help":
                    show_help()
                case "exit":
                    playing = False
                case "me":
                    player.show_status()
                case "wait":
                    time_passes = True
                case "attack":
                    target_name = command[7:]
                    target = player.location.get_monster_by_name(target_name)
                    if target != False:
                        system.attack_enemy(player, target)
                    else:
                        print("No such monster.")
                        command_success = False
                case other:
                    print("Not a valid command")
                    command_success = False
        if time_passes == True:
            updater.update_all()




