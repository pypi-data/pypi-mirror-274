from .log import *
from .style import *
from typing import Callable
from os import system as cmd


def inputs(word=Style.BRIGHT + ">>> " + Style.NORMAL, spilt_text=None, func: Callable = None,
           func_word: dict = None, end_symbol: str = None, is_cmd: bool = False):
    try:
        word = str(word)
    except TypeError:
        raise ConvertError("Name or message must can convert to string")
    text = input(word)
    if end_symbol is not None:
        if text[-1] == end_symbol:
            text = text[:-1]
        else:
            error("System", f"The last character of your command must be '{end_symbol}'.{Style.RESET}",
                  e_type="Symbol Error")
            return False
    if is_cmd:
        cmd(text)
    elif func is not None:
        func(text.split(spilt_text))
    elif func_word is not None:
        text = text.split(spilt_text)
        command = text[0]
        for i in func_word:
            if command == i:
                command = func_word[i]
                command(text[1:])
                return True
            else:
                error("System", f"The command '{command}' is not valid", e_type="Function Undefined")
                return False
    else:
        return text.split(spilt_text)
