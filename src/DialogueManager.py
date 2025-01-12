from time import sleep
from Actor import Actor
import json
from Utils import*

class DialogueManager:
        # singleton pattern
    _instance = None

    # this ensures only a single instance exists
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'Actors'): #we make sure that the class hasnt been initialised already using the "has attribute" function to check if the attribute has already been assigned
            self.talkingActor : Actor = None 
            self.dialogue = ""
            self.activeNode : DialogueNode = None
            from Game import Game
            self.playerActor = Game._instance.PlayerActor
       
    def __str__(self):
        for Actor in self.Actors:
            print(self.Actors[Actor])
        return f""
    

    def StartDialogue(self, actor : Actor, dialogue : str):
        self.talkingActor = actor
        self.dialogue = dialogue
        from Game import Game, GameState
        Game._instance.GameState = GameState.Talking
        self.activeNode = DialogueNode(dialogue, 1, actor) #the default starting node is 1
        self.DialogueLoop()

    def DialogueLoop(self):
        from Game import Game, GameState
        while Game._instance.GameState == GameState.Talking:
            print(self.activeNode)
            command = input("What would you like to do? ")
            self.ProcessCommands(command)
            sleep(1)

    def DisplayCommands(self):
        print(f"{GREEN}Exit{RESET} - Leave the conversation")
        print(f"{GREEN}[dialogue number]{RESET} - Select a dialogue option. Also works by typing the dialogue text.")

    def ProcessCommands(self, command : str):
        if command == "help":
            self.DisplayCommands()
            return
        if command == "exit":
            print(f"You have left the conversation with {YELLOW}{self.talkingActor.Name}{RESET}")
            from Game import Game, GameState
            Game._instance.GameState = GameState.Roaming
            return
        num = 1
        for response in self.activeNode.Responses:
            if command == str(num) or command == response:
                print(f"{YELLOW}{self.playerActor.Name}{RESET}: {response}")
                self.activeNode = DialogueNode(self.dialogue, self.activeNode.Responses[response], self.talkingActor)
                if len(self.activeNode.Responses) == 0:
                    from Game import Game, GameState
                    Game._instance.GameState = GameState.Roaming
                    print(f"The conversation with {YELLOW}{self.talkingActor.Name}{RESET} has ended.")
                return
            num += 1
        print(f"{RED}Invalid response, please try again{RESET}")

class DialogueNode:
    def __init__(self, dialogue : str, dialogueId : int, assignedActor : Actor):
        self.Text = ""
        self.Responses = {} # {response: dialogueId}
        self.Actor = assignedActor
        self.load(dialogue, dialogueId)

    def __str__(self):
        print(f"{YELLOW}{self.Actor.Name}{RESET}: {self.Text}")
        num = 1
        for response in self.Responses:
            print(f"{num}: {response}")
            num += 1
        return f""

    def load(self, dialogue : str, dialogueId : int):
        try:
            with open("World\Dialogue.json", "r") as file:
                data = json.load(file)
                dialogue_data = data.get(dialogue)
                for data in dialogue_data:
                    if data.get("id") == str(dialogueId):
                        self.Text = data.get("text")
                        responses = data.get("options")
                        for response in responses:
                            self.Responses[response.get("text")] = response.get("targetNodeId")
                        return
        except FileNotFoundError:
            print("Error: The file does not exist.")
        except json.JSONDecodeError:
            print("Error: The JSON file is not properly formatted.")

    def DisplayResponses(self):
        for i, response in enumerate(self.Responses):
            print(f"{i+1}: {response[0]}")

    def ProcessResponse(self, response : int):
        return self.Responses[response-1][1]

    def Display(self):
        print(self)
        self.DisplayResponses()