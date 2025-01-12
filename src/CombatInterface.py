from time import sleep
import Actor
from Utils import*
from enum import Enum
from Item import Item

class Turn(Enum):
    Player = 1
    Enemy = 2

class CombatInterface:
    # singleton pattern
    _instance = None

    # this ensures only a single instance exists
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'Items'): #we make sure that the class hasnt been initialised already using the "has attribute" function to check if the attribute has already been assigned
            self.PlayerActor : Actor = {} # {name: EnvironementClass} structure
            self.EnemyNPC : Actor = None
            self.turn = Turn.Player
       
    def __str__(self):
        print(f"{YELLOW} You{RESET} are fighting {YELLOW}{self.EnemyNPC.Name} {RESET}")
        print(f"Your health is {RED}{self.PlayerActor.Health}{RESET} and the enemy's health is {RED}{self.EnemyNPC.Health}{RESET}")
        print(f"You have {RED}{self.PlayerActor.Attack}{RESET} attack and the enemy's attack is {RED}{self.EnemyNPC.Attack}{RESET}")
        return f""
    
    def CombatLoop(self):
        from Game import Game, GameState
        while Game._instance.GameState == GameState.Battling:
            if self.turn == Turn.Player:
                print(f"{YELLOW}It is your turn{RESET}")
                command = input("What would you like to do? ")
                if self.ProcessCommands(command):
                    self.turn = Turn.Enemy
            elif self.turn == Turn.Enemy:
                print(f"{YELLOW}It is the enemy's turn{RESET}")
                sleep(1)
                self.EnemyTurn()
                self.turn = Turn.Player
                print(self)

    def InitCombat(self, player : Actor, enemy : Actor):
        from Game import Game, GameState
        self.turn = Turn.Player
        self.PlayerActor = player
        self.EnemyNPC = enemy
        Game._instance.GameState = GameState.Battling
        print(f"You are now in combat with {YELLOW}{self.EnemyNPC.Name}{RESET}!")
        print(self)
        self.CombatLoop()

    def Attack(self, instigator, target):
        target.Health -= instigator.Attack*(1-target.Defense)
        print(f"{YELLOW}{instigator.Name}{RESET} attacks {YELLOW}{target.Name}{RESET} for {RED}{instigator.Attack}{RESET} damage")
        print(f"{YELLOW}{target.Name}{RESET} has {RED}{target.Health}{RESET} health remaining \n")
        if target.Health <= 0:
            print(f"{YELLOW}{target.Name}{RESET} has been defeated")
            if(target == self.EnemyNPC):
                from Game import Game
                Game._instance.ActiveEnvironement.RemoveNPC(target.Name)
                print(f"You have won the battle!")
                sleep(1)
            else:
                print(f"You have been defeated")
                sleep(1)
            from Game import Game, GameState
            Game._instance.GameState = GameState.Roaming

    def AttackWithItem(self, instigator, item : Item):
        from Item import AttackItem
        if instigator == self.PlayerActor:
            target = self.EnemyNPC
        elif instigator == self.EnemyNPC:
            target = self.PlayerActor
        else:
            return
        if isinstance(item, AttackItem):
            target.Health -= item.damage*(1-target.Defense)
            print(f"{YELLOW}{instigator.Name}{RESET} attacks {YELLOW}{target.Name}{RESET} with a {YELLOW}{item.name}{RESET} for {RED}{item.damage}{RESET} damage")
            print(f"{YELLOW}{target.Name}{RESET} has {RED}{target.Health}{RESET} health remaining \n")
            if target.Health <= 0:
                print(f"{YELLOW}{target.Name}{RESET} has been defeated")
                if(target == self.EnemyNPC):
                    from Game import Game
                    Game._instance.ActiveEnvironement.RemoveNPC(target.Name)
                    print(f"You have won the battle!")
                else:
                    print(f"You have been defeated")
                from Game import Game, GameState
                Game._instance.GameState = GameState.Roaming

    def EnemyTurn(self):
        self.Attack(self.EnemyNPC, self.PlayerActor)
        #implement randomly choosing items and abilities later

    def ProcessCommands(self, command : str):
        split_command = command.split(" ")
        match split_command[0]:
            case "help":
                self.DisplayCommands()
                return False
            case "info":
                from Utils import Utils
                itemName = Utils.JoinWordList(split_command[1:len(split_command)])
                if self.ItemManager.PrintInfo(itemName):
                    return False
            case "attack":
                self.Attack(self.PlayerActor, self.EnemyNPC)
                self.turn = Turn.Enemy
                return True
            case "flee":
                print(f"You have fled combat!")
                from Game import Game, GameState
                Game._instance.GameState = GameState.Roaming
                return True
        if self.PlayerActor.ProcessCommand(command):
            return True
        #print(f"command \"{command}\" not recognised")
        return False

    def DisplayCommands(self):
        print(f"{GREEN}help{RESET} - Displays a list of commands available in the current context")
        print(f"\n{GREEN}info [name]{RESET} - Displays information for the specified zone or actor. Can use self to get your own info {RED}NOT IMPLEMENTED YET{RESET}")
        print(f"\n{GREEN}attack{RESET} - Attack the enemy")
        print(f"\n{GREEN}flee{RESET} - Flee from combat")