import json
from Actor import*
from Environement import*
from Inventory import*
from Item import*
from enum import Enum
import copy

class GameState(Enum):
    Roaming = 1
    Battling = 2
    Talking = 3

class Game:
    # singleton pattern
    _instance = None
 
    # this ensures only a single instance exists
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'ItemManager'): #we make sure that the class hasnt been initialised already using the "has attribute" function to check if the attribute has already been assigned
            self.ItemManager = ItemManager()
            self.InventoryManager = InventoryManager()
            self.ActorManager = ActorManager()
            self.EnvironementManager = EnvironementManager()
            self.EnvironementManager.loadNpcRefs()
            self.ActiveEnvironement = self.EnvironementManager.GetEnvironement("Forest")
            self.PlayerActor : Actor = copy.deepcopy(self.ActorManager.GetActor("Hero"))
            self.GameState = GameState.Roaming

    def GameLoop(self):
        self.ActiveEnvironement.DisplayInfo()
        while(True):
           #print("\n\n\n\n\n\n\n\n\n\n\n\n")
           #self.ActiveEnvironement.DisplayInfo()
           command = str(input("Enter command. Type \"help\" for available commands "))
           self.ProcessCommands(command)

    def DisplayCommands(self):
        print(f"{GREEN}help{RESET} - Displays a list of commands available in the current context")
        print(f"\n{GREEN}info [name]{RESET} - Displays information for the specified zone or actor. Can use self to get your own info {RED}NOT IMPLEMENTED YET{RESET}")
        self.ActiveEnvironement.DisplayCommands()
        self.PlayerActor.DisplayCommands()

    def ChangeEnvironement(self, environement : Environement):
        self.ActiveEnvironement = environement

    def ProcessCommands(self, command : str):
        match command:
               case "help":
                   self.DisplayCommands()
                   return
        if self.ActiveEnvironement.ProcessCommand(command):
            return
        if self.PlayerActor.ProcessCommand(command):
            return
        print(f"command \"{command}\" not recognised")