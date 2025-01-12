import json
from Actor import *
from CombatInterface import *
import copy

# ANSI color codes
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
RESET = "\033[0m"

class Environement:
    def __init__(self, name : str):
        self.name = name
        self.AdjacentEnvironements = {}
        self.NPCs = {}

    def __str__(self):
        self.DisplayInfo()
        return f""


    def loadNPCs(self): #assign the NPC references
        try:
            with open("World\Environements.json", "r") as file:
                data = json.load(file)
            
            env_data = data.get(self.name)
            if env_data:
                npc_data = env_data.get("Actors")
                actor_manager = ActorManager._instance
                for npc in npc_data:
                    self.NPCs[npc] = copy.deepcopy(actor_manager.GetActor(npc))
        except FileNotFoundError:
            print("Error: The file 'actors.json' does not exist.")
        except json.JSONDecodeError:
            print("Error: The JSON file is not properly formatted.")

    def loadAdjacentEnvironements(self): #assign the environement references
        try:
            with open("World\Environements.json", "r") as file:
                data = json.load(file)
            
            env_data = data.get(self.name)
            if env_data:
                adj_envs = env_data.get("AdjacentEnvironements")
                env_manager = EnvironementManager._instance
                for env in adj_envs:
                    self.AdjacentEnvironements[env] = env_manager.GetEnvironement(env)
        except FileNotFoundError:
            print("Error: The file 'actors.json' does not exist.")
        except json.JSONDecodeError:
            print("Error: The JSON file is not properly formatted.")

    def DisplayInfo(self):
        print(f"You are in the {GREEN}{self.name}{RESET}")

        #print all acessible Environements
        adjacentText = f"the {GREEN}{self.name}{RESET} is adjacent to the {GREEN}{list(self.AdjacentEnvironements.keys())[0]}{RESET}"
        if len(self.AdjacentEnvironements)>2:
            for env in self.AdjacentEnvironements.keys()[1,-1]:
                adjacentText += f", the {GREEN}{env}{RESET}"
        if len(self.AdjacentEnvironements)>1:
            adjacentText += f" and the {GREEN}{list(self.AdjacentEnvironements.keys())[len(self.AdjacentEnvironements)-1]}{RESET}"
        print(adjacentText)

        #print all acessible NPCs
        if len(self.NPCs)>0:
            adjacentText = f"You can go meet the {YELLOW}{list(self.NPCs.keys())[0]}{RESET}"
            if len(self.NPCs)>2:
                for env in self.NPCs.keys()[1,-1]:
                    adjacentText += f", the {YELLOW}{env}{RESET}"
            if len(self.NPCs)>1:
                adjacentText += f" and the {YELLOW}{list(self.NPCs.keys())[len(self.NPCs)-1]}{RESET}"
            print(adjacentText)

    def ProcessCommand(self, command : str):
        match command:
            case "environement info":
                self.DisplayInfo()
                return True
        split_command = command.split(" ")
        match split_command[0]:
            case "move":
                return self.FindEnvironement(split_command[1])
            case "talk":
                npc = self.FindNPC(split_command[1])
                if npc and npc.dialogue != "":
                    from DialogueManager import DialogueManager
                    DialogueManager._instance.StartDialogue(npc, npc.dialogue)
                    print(self) 
                    return True
                print(f"The {YELLOW}{npc.name}{RESET} does not seem to want to talk to you.")
                return True
            case "attack":
                npc = self.FindNPC(split_command[1])
                if npc:
                    from Game import Game, GameState
                    CombatInterface._instance.InitCombat(Game._instance.PlayerActor, npc)
                    print(self) 
                    return True
                print(f"{RED}NPC {split_command[1]} not found{RESET}")
                return True
        return False

    def DisplayCommands(self):
        print(f"{GREEN}environement info{RESET} - Displays the environement's information")
        print(f"{GREEN}move [location]{RESET} - Moves to the specified location if it is available")
        print(f"{GREEN}talk [npc]{RESET} - Talks to the specified NPC")
        print(f"{GREEN}attack [npc]{RESET} - Attacks the specified NPC")

    def FindEnvironement(self, envName):
        for env in self.AdjacentEnvironements:
            if env.lower() == envName:
                from Game import Game
                Game._instance.ChangeEnvironement(self.AdjacentEnvironements[env])
                return True
        return False
    
    def FindNPC(self, npcName):
        for npc in self.NPCs:
            if npc.lower() == npcName:
                return self.NPCs[npc]
        return None

    def RemoveNPC(self, npcName):
        if npcName.lower() in map(str.lower, self.NPCs.keys()):
            self.NPCs.pop(npcName)
            return True

class EnvironementManager:
    # singleton pattern
    _instance = None

    # this ensures only a single instance exists
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'Items'): #we make sure that the class hasnt been initialised already using the "has attribute" function to check if the attribute has already been assigned
            self.Environements = {} # {name: EnvironementClass} structure
            self.load()
       
    def __str__(self):
        for Inventory in self.Inventories:
            print(self.Inventories[Inventory])
        return f""

    def load(self):
        try:
            with open("World\Environements.json", "r") as file:
                data = json.load(file)
            for name in data:
                self.Environements[name] = Environement(name)
        except FileNotFoundError:
            print("Error: The file does not exist.")
        except json.JSONDecodeError:
            print("Error: The JSON file is not properly formatted.")
        for env in self.Environements: #now that all the environements are set up we can set up the environement references
            self.Environements[env].loadAdjacentEnvironements()
            

    def loadNpcRefs(self):
        for env in self.Environements:
            self.Environements[env].loadNPCs()

    def GetEnvironement(self, name):
        if(name in self.Environements):
            return self.Environements[name]
        return None