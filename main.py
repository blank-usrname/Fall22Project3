from room import Room
from player import Player
from item import Item
from item import Consumable
from monster import Monster
import os
import updater

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
    i = Item("Rock", "This is just a rock.")
    j = Consumable("Crest of Flames", "Grants +10 to Max HP and +5 to all other stats.", 10, 5, "all")
    k = Consumable("Salve", "Heals 20 HP", 20, 0, "heal")
    i.put_in_room(a_2)
    j.put_in_room(a_1)
    k.put_in_room(a_3)
    player.location = a_1
    Monster("Slime", 1, a_2)

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
    print("save <file1/file2/file3> -- saves current session to file")
    print("load <file1/file2/file3> -- saves current session to file")
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
                        player.pickup(target)
                    else:
                        print("No such item.")
                        command_success = False
                case "use":  #can handle multi-word objects
                    target_name = command[4:] # everything after "use "
                    target = player.is_in_inventory(target_name)
                    if target != False:
                        target.consume(player)
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
                        player.attack_monster(target)
                    else:
                        print("No such monster.")
                        command_success = False
                case other:
                    print("Not a valid command")
                    command_success = False
        if time_passes == True:
            updater.update_all()




