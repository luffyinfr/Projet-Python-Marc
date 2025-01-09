import json
from Item import *

# ANSI color codes
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
RESET = "\033[0m"

class Inventory:
    def __init__(self, name : str):
        self.name = name
        self.itemList = []
        self.Owner : Actor = None
        self.load(name)

    def __str__(self):
        print(f"Inventory {self.name}:")
        for item in self.itemList:
            print(item.name)
        return f""

    def load(self, name : str):
        try:
            with open("World/Inventories.json", "r") as file:
                data = json.load(file)
            
            # Find the inventory by name
            inventory_data = data.get(name)
            itemManager = ItemManager._instance
            if inventory_data:
                for item in inventory_data:
                    itemClass = itemManager.GetItem(item)
                    if(itemClass):
                        self.itemList.append(itemClass)
            else:
                print(f"Inventory '{name}' not found in the JSON file.")
        except FileNotFoundError:
            print("Error: The file 'Inventory.json' does not exist.")
        except json.JSONDecodeError:
            print("Error: The JSON file is not properly formatted.")

    def DisplayCommands(self):
        print(f"{GREEN}Inventory{RESET} - Displays Inventory")
        print(f"{GREEN}Inventory Use [Item]{RESET} - Uses the named item if available")
        print(f"{GREEN}Inventory info [Item]{RESET} - Displays info for the given item if available")

    def ProcessCommand(self, command : str):
        if command.lower() == "inventory":
            print(self)
            return True
        split_command = command.split(" ")
        match split_command[0].lower():
            case "use":
                if(split_command[0] in self.itemList):
                    self.itemList[split_command[0]].Use(self.Owner)
                    return True
            case "info":
                if(split_command[0] in self.itemList):
                    print(self.itemList[split_command[0]])
                    return True
        return False
                

class InventoryManager:
    # singleton pattern
    _instance = None

    # this ensures only a single instance exists
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'Inventories'): #we make sure that the class hasnt been initialised already using the "has attribute" function to check if the attribute has already been assigned
            self.Inventories = {} # {name: inventoryClass} structure
            self.load()
       
    def __str__(self):
        for Inventory in self.Inventories:
            print(self.Inventories[Inventory])
        return f""

    def load(self):
        try:
            with open("World\\Inventories.json", "r") as file:
                data = json.load(file)
            for name in data:
                self.Inventories[name] = Inventory(name)
        except FileNotFoundError:
            print("Error: The file does not exist.")
        except json.JSONDecodeError:
            print("Error: The JSON file is not properly formatted.")

    def GetInventory(self, name):
        if(name in self.Inventories):
            return self.Inventories[name]
        return None