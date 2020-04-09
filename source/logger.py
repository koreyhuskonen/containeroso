import inspect
from colorama import Fore, Style, init
init(autoreset=True)

def getParentFunction():
    return inspect.stack()[2].function

def info(dbg_message):
    parent = getParentFunction()
    if parent == 'createNetwork':
        color = Fore.CYAN
    elif parent == 'getSSHPort':
        color = Fore.YELLOW
    elif parent == 'destroyNetwork':
        color = Fore.MAGENTA
    else:
        color = Fore.GREEN
    print(color + "--| " + dbg_message)
