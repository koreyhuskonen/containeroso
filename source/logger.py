import inspect
from colorama import Fore, Style, init
init(autoreset=True)

def getParentFunction():
    return inspect.stack()[2].function

def info(dbg_message):
    parent = getParentFunction()
    if parent == 'startContaineroso':
        color = Fore.GREEN
    elif parent == 'createNetwork':
        color = Fore.CYAN
    elif parent == 'getSSHPort':
        color = Fore.YELLOW
    else:
        color = Fore.MAGENTA
    print(color + "--| " + dbg_message)
