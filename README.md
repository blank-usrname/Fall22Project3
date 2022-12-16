# Reed CS 122 Final Project

## DOCUMENTED BUGS

* For some reason, "Boss" and "Straggler" move, even though they should not be able to.
* Level up system does not account for non-integer values properly, and will skip assignment of stats if non-integer (?) value is inputted. Be careful here!

## A "story", of sorts

Your fiancee demands that you buy them a specific ring. 
Specifically, the ring found in the deep dark scary cave filled with
monsters. You make the trek there, but find that a merchant has already
obtained the ring, and is willing to sell it to you for 7.5k gold.
Can you find the ring in time to propose to your fiancee in a timely
manner?

## Implemented features
* "drop" command (1 pt)
* "wait" command (1 pt)
* "me" command (2 pt)
* Bigger world (2 pt)
* Inventory max size/carrying capacity (2 pt)
* "inspect" command (2 pt)
* Loot (3 pt) (?), partial implementation, only 2/5 enemy types have loot implemented.
* More monsters (3 pt), 5 enemy types implemented, with differing stats and AI
* Special rooms (3 pt, maybe 1 or 2) (?), not necessarily implemented, NPC's were implemented however, such as a doctor and a merchant,
* Player attributes (3 pt), Strength (Str/2 adds 1 point to damage), Defense (Def/2 reduces 1 point of damage), Dexterity (Dex/2 adds 1 point to accuract), Speed (Spd/2 adds 1 point of evasion)
* Weapons (2 pt), different weapons have different properties, such as carrying weight, strength bonus, and accuracy
* Armor (2 pt), different armor have different properties, such as carrying weight, defense bonus, and evasion modifier
* Auto-generating monsters (2 pt), monsters generate after period of time in spaces free of monsters, with stats based on player level
* Victory condition (2 pt), victory condition is from synopsis above, with different endings based on efficiency of task
* Healing items (2 pt), Healing items are consumable items, which stack as well
* Locked chests (2 pt)
* Stacking items (2 pt), Consumable item type, number of items in a stack is a property of them
* Command abbreviations (1 pt), many commands have simple abbreviations, not quite so complicated
* Currency (4 pt), gold is implemented, with enemies dropping gold, merchants allowing for the buying and selling of items.
* Leveling up (4 pt), Level up system is implemented, with experience points, and a system that, at each level up, the distribution of a few points to non-HP stats.
* ADDITIONAL FEATURE: Combat (1-3 pts?), combat system overhauled, with commands to attack, use item, change equipment, inspect stats of self/enemy, run away; enemies also have semi-unique AI in how they act within combat.
