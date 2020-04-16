import inspect
from colorama import Fore, Style, init
init(autoreset=True)

def getCallStack():
    stack = [s.function for s in inspect.stack()]
    return stack

def info(dbg_message):
    stack = getCallStack()
    if 'createNetwork' in stack:
        color = Fore.CYAN
    elif 'destroyNetwork' in stack:
        color = Fore.MAGENTA
    elif 'buildImage' in stack:
        color = Fore.BLUE
    else:
        color = Fore.GREEN
    print(color + "--| " + dbg_message)
