import json
import Utils
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
        self.itemList = {}
        self.Owner : Actor = None
        self.load(name)

    def __str__(self):
        print(f"Inventory {self.name}:")
        for item in self.itemList:
            print(item)
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
                        self.itemList[itemClass.name.lower()] = itemClass
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
        if command == "inventory":
            print(self)
            return False
        split_command = command.split(" ")
        if split_command[0] == "inventory":
            item = Utils.JoinWordList(split_command[2:len(split_command)])
            match split_command[1]:
                case "use":
                    if(item in (key.lower() for key in self.itemList.keys())):
                        self.itemList[item].Use(self.Owner)
                        self.itemList.pop(item)
                        print(f"Used the {YELLOW}{item}{RESET}")
                        return True
                    print(f"{RED}There is no item named {item} in the inventory {RESET}")
                    return False
                case "info":
                    if(item in (key.lower() for key in self.itemList.keys())):
                        print(self.itemList[item])
                        self.itemList.pop("item")
                        return True
                    print(f"{RED}There is no item named {item} in the inventory {RESET}")
                    return False
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