
# ANSI color codes
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
RESET = "\033[0m"

def JoinWordList(list):
        returnstr = ""
        for element in list:
            returnstr += element + " "
        return returnstr.strip()