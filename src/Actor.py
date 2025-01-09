import json
from Inventory import *

class Actor:
    def __init__(self, name : str):
        self.name = name
        self.Health = 0
        self.MaxHealth = 0
        self.Attack = 0
        self.inventory = None
        self.load(name)

    def __str__(self):
        return f"{self.name}({self.Health},{self.Attack})"



    def load(self, name : str):
        try:
            with open("World\\actors.json", "r") as file:
                data = json.load(file)
            
            # Find the actor by name
            actor_data = data.get(name)
            if actor_data:
                self.inventory = InventoryManager._instance.GetInventory(actor_data.get("Inventory"))
                self.inventory.Owner = self
                self.Health = actor_data.get("Health", 0)  # Default to 0 if not found
                self.MaxHealth = self.Health
                self.Attack = actor_data.get("Attack", 0)  # Default to 0 if not found
            else:
                print(f"Actor '{name}' not found in the JSON file.")
        except FileNotFoundError:
            print("Error: The file 'actors.json' does not exist.")
        except json.JSONDecodeError:
            print("Error: The JSON file is not properly formatted.")

    def Heal(self, amount : int):
        self.Health += amount
        if self.Health > self.MaxHealth:
            self.Health = self.MaxHealth

    def DisplayCommands(self):
        self.inventory.DisplayCommands()

    def ProcessCommand(self, command : str):
        return self.inventory.ProcessCommand(command)

class ActorManager:
    # singleton pattern
    _instance = None

    # this ensures only a single instance exists
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'Actors'): #we make sure that the class hasnt been initialised already using the "has attribute" function to check if the attribute has already been assigned
            self.Actors = {} # {name: inventoryClass} structure
            self.load()
       
    def __str__(self):
        for Actor in self.Actors:
            print(self.Actors[Actor])
        return f""

    def load(self):
        try:
            with open("World\\actors.json", "r") as file:
                data = json.load(file)
            for name in data:
                self.Actors[name] = Actor(name)
        except FileNotFoundError:
            print("Error: The file does not exist.")
        except json.JSONDecodeError:
            print("Error: The JSON file is not properly formatted.")

    def GetActor(self, name):
        if(name in self.Actors):
            return self.Actors[name]
        return None
    