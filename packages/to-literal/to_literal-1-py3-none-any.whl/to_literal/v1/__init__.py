from typing import Union
from typing import Literal
from typing import List

import typing

def toLiteral(array: Union[list, tuple]) -> List:
    """
    Convierte una lista/tupla a un Literal[]

    
    :param array: (Union[list, tuple]): Lista/Tupla sobre valores de forma en general
    
    :returns: Literal[]: Devuelve el array convertido a un Literal definido

    """

    def parse(array) -> Literal:
        val = f"literal = typing.Literal{array}"
        exec(val, globals())

        return literal

    if isinstance(array, tuple):
        array = list(array)
        return parse(array)

    if isinstance(array, list):
        return parse(array)
        
        