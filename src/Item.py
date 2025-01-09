import json
from enum import Enum
from Actor import*

class ObjectType(Enum):
    Healing = 1
    Combat = 2

class_registry = {}
class Item:
    def __init__(self, name):
        self.name = name

    @classmethod
    def register(cls, item_type):
        """Decorator to register a subclass with the given type name."""
        def wrapper(subclass):
            class_registry[item_type] = subclass
            return subclass
        return wrapper

    @staticmethod
    def create(item_type, **kwargs):
        """Factory method to create an item based on its type."""
        item_class = class_registry.get(item_type)
        if not item_class:
            raise ValueError(f"Unknown item type: {item_type}")
        return item_class(**kwargs)
    

@Item.register("ItemA")
class ItemA(Item):
    def __init__(self, name, damage):
        super().__init__(name)
        self.damage = damage

    def __str__(self):
        return f"{self.name} (Damage: {self.damage})"
    
    def Use(self, caller):
        from Game import Game
        from Game import GameState
        if(Game._instance.GameState == GameState.Battling):
            #implement damaging here
            pass
        
    
@Item.register("ItemB")
class ItemB(Item):
    def __init__(self, name, healing):
        super().__init__(name)
        self.healing = healing

    def __str__(self):
        return f"{self.name} (Healing: {self.healing})"
    
    def Use(self, caller):
        from Game import Game
        from Game import GameState
        if(Game._instance.GameState == GameState.Roaming):
            caller.Heal(self.healing)
    
class ItemManager:
    # singleton pattern
    _instance = None

    # this ensures only a single instance exists
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'Items'): #we make sure that the class hasnt been initialised already using the "has attribute" function to check if the attribute has already been assigned
            self.Items = {} # {name: itemclass} structure
            self.load()
       
    def __str__(self):
        for item in self.Items:
            print(self.Items[item])
        return f""

    def load(self):
        try:
            with open("World\\items.json", "r") as file:
                data = json.load(file)
            
            for name, rest in data.items():
                self.Items[name] = Item.create(name, **rest)
            else:
                print(f"Actor '{name}' not found in the JSON file.")
        except FileNotFoundError:
            print("Error: The file does not exist.")
        except json.JSONDecodeError:
            print("Error: The JSON file is not properly formatted.")

    def GetItem(self, name):
        if(name in self.Items):
            return self.Items[name]
        return None