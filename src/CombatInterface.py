import Actor
from Utils import*
from enum import Enum

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
    
    def InitCombat(self, player : Actor, enemy : Actor):
        from Game import Game, GameState
        self.turn = Turn.Player
        self.PlayerActor = player
        self.EnemyNPC = enemy
        Game._instance.GameState = GameState.Battling
        print(f"You are now in combat with {YELLOW}{self.EnemyNPC.Name}{RESET}!")
        print(self)

    def Attack(self, instigator, target):
        target.Health -= instigator.Attack*(1-target.Defense)
        print(f"{YELLOW}{instigator.Name}{RESET} attacks {YELLOW}{target.Name}{RESET} for {RED}{instigator.Attack}{RESET} damage")
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
        self.turn = Turn.Player

    def ProcessCommands(self, command : str):
        split_command = command.split(" ")
        match split_command[0]:
            case "attack":
                self.Attack(self.PlayerActor, self.EnemyNPC)
                return
            case "flee":
                print(f"You have fled combat!")
                from Game import Game, GameState
                Game._instance.GameState = GameState.Roaming
                return