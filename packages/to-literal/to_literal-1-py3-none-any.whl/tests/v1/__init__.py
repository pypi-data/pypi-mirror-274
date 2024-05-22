import pytest
import typing

import os, sys
ruta_proyecto = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
sys.path.insert(0, ruta_proyecto)

from src.to_literal.v1 import toLiteral

def test_toLiteral():

    """
    
    """
    
    literal_array = toLiteral([ 1, 2, 3, 4, 5 ])
    literal_array_str_type = str(type(literal_array))
    
    print(literal_array_str_type)
    assert literal_array_str_type == "<class 'typing._LiteralGenericAlias'>"
