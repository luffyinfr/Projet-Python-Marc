import json
from Actor import*
from Environement import*
from Inventory import*
from Item import*
from enum import Enum
import copy
import Utils
from CombatInterface import*
from DialogueManager import DialogueManager

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
            self.CombatInterface = CombatInterface()
            self.ActiveEnvironement = self.EnvironementManager.GetEnvironement("Village")
            self.PlayerActor : Actor = copy.deepcopy(self.ActorManager.GetActor("Hero"))
            self.GameState = GameState.Roaming
            self.DialogueManager = DialogueManager()

    def GameLoop(self):
        self.ActiveEnvironement.DisplayInfo()
        while(True):
           #print("\n\n\n\n\n\n\n\n\n\n\n\n")
           #self.ActiveEnvironement.DisplayInfo()
           command = str(input("Enter command. Type \"help\" for available commands "))
           if command == "exit":
               break
           self.ProcessCommands(command.lower())

    def DisplayCommands(self):
        print(f"{GREEN}help{RESET} - Displays a list of commands available in the current context")
        print(f"\n{GREEN}info [name]{RESET} - Displays information for the specified zone or actor. Can use self to get your own info {RED}NOT IMPLEMENTED YET{RESET}")
        self.ActiveEnvironement.DisplayCommands()
        self.PlayerActor.DisplayCommands()

    def ChangeEnvironement(self, environement : Environement):
        self.ActiveEnvironement = environement
        environement.DisplayInfo()

    def ProcessCommands(self, command : str):
        split_command = command.split(" ")
        match split_command[0]:
            case "help":
                self.DisplayCommands()
                return
            case "info":
                itemName = Utils.JoinWordList(split_command[1:len(split_command)])
                if self.ItemManager.PrintInfo(itemName):
                    return
        match self.GameState:
            case GameState.Roaming:
                if self.ProcessRoamingCommands(command):
                    return
            case GameState.Talking:
                if self.ProcessTalkingCommands(command):
                    return
        if self.PlayerActor.ProcessCommand(command):
            return
        #print(f"command \"{command}\" not recognised")

    def ProcessRoamingCommands(self, command : str):
        if self.ActiveEnvironement.ProcessCommand(command):
            return
        
    def ProcessBattlingCommands(self, command : str):
        CombatInterface._instance.ProcessCommands(command)

    def ProcessTalkingCommands(self, command : str):
        pass
    def SetState(self, state : GameState):
        self.GameState = state