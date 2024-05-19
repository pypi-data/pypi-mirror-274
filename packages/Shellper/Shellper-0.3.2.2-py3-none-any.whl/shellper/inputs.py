from .style import *
from typing import Callable
from os import system as cmd


def inputs(word=Style.BRIGHT + ">>> " + Style.NORMAL, spilt_text=None, func: Callable = None,
           func_word: dict = None, need_arg: bool = True, end_symbol: str = None, is_cmd: bool = False):
    try:
        word = str(word)
    except TypeError:
        raise ConvertError("Name or message must can convert to string")
    text = input(word)
    if end_symbol is not None:
        if text[-1] == end_symbol:
            text = text[:-1]
        else:
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
                if need_arg:
                    command(text[1:])
                else:
                    command()
                return True
            else:
                return False
    else:
        return text.split(spilt_text)
