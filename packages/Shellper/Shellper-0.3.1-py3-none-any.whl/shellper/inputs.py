from .log import *
from .style import *
from os import system as cmd
from typing import Callable


def inputs(word=Style.BRIGHT + ">>> " + Style.NORMAL, spilt_text=None, func: Callable = None,
           end_symbol: str = None, is_cmd: bool = False):
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
    else:
        return text.split(spilt_text)
