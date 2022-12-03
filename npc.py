class NPC:
    def __init__(self, name, desc, location):
        self.name = name
        self.desc = desc
        self.location = None
        location.add_npcs(self)

    def inspect(self):
        print()
        print(self.desc)
        print()
        print("Press enter to continue...")

class Merchant(NPC):
    def __init__(self, name, desc, location, items):
        super().__init__(name, desc,location)
        self.items = items
        self.desc = desc

    
    def is_in_inventory(self, name):
        for i in self.items:
            if i.name.lower() == name.lower():
                return i
        return False


class Doctor(NPC):
    def __init__(self, name, desc):
        self.name = name
        self.desc = desc
    
    def inspect(self):
        print()
        print(self.desc)
        print()
        print("Press enter to continue...")
