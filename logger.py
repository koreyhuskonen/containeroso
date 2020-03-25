import inspect
from colorama import Fore, Style, init
init(autoreset=True)

def getParentFunction():
    return inspect.stack()[2].function

def info(dbg_message):
    parent = getParentFunction()
    if parent == 'createNetwork':
        color = Fore.CYAN
    else:
        color = Fore.MAGENTA
    print(color + "--| " + dbg_message)
