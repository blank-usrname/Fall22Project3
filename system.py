import os
import system
import random

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def attack_enemy(player, enemy):
    clear()
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
        enemy.die()
        exp = (enemy.level//player.level) + 3
        print("Awarded " + str(exp) + " exp.")
        player.exp += exp
        player.level_up()
    else:
        print("You lose.")
        player.alive = False
    print()
    input("Press enter to continue...")