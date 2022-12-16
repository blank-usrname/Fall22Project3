class NPC: # define non player characters
    def __init__(self, name, desc, location): # npc's have name, descriptions, and locations
        self.name = name
        self.desc = desc
        self.location = None
        location.add_npcs(self)

    def inspect(self): # function specifying when inspecting NPCs
        print()
        print(self.desc)
        print()
        print("Press enter to continue...")

    def npc_type(self):  # function specifying type of NPC
        return "generic"

class Merchant(NPC):
    def __init__(self, name, desc, location, items):
        super().__init__(name, desc,location)
        self.items = items # merchant sells list of items

    def sell(self, item):
        # certain items are limited supply, such as non consumable items
        if (not item.is_consumable()):
            self.items.remove(item) # remove item from inventory if item is non consumable

    def is_in_inventory(self, name): # check if item exists within merchant's inventory
        for i in self.items:
            if i.name.lower() == name.lower():
                return i
        return False

    def npc_type(self): # function specifying type of NPC
        return "merchant"


class Doctor(NPC):
    def __init__(self, name, desc, location):
        super().__init__(name, desc,location)
    
    def npc_type(self): # function specifying type of NPC
        return "doctor"
