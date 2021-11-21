from src.house import House
from unittest.mock import MagicMock
import pytest


def test_create_house():
    mock_position = MagicMock()
    mock_players = MagicMock()
    mock_property = MagicMock()
    house = House(position=mock_position, players=mock_players, property=mock_property)
    assert house.position == mock_position
    assert house.players == mock_players
    assert house.property == mock_property


def test_create_house_players_none():
    mock_position = MagicMock()
    mock_property = MagicMock()
    house = House(position=mock_position, players=None, property=mock_property)
    assert house.property == mock_property
    assert house.position == mock_position
    assert house.players is not None and house.players == []


def test_house__str__without_property():
    mock_position = MagicMock()
    house = House(position=mock_position, players=[2, 3, 4], property=None)
    assert house.__str__() == f'({mock_position}) (P: NO NAME) 3 Players'


def test_house__str__with_property_without_name():
    mock_position = MagicMock()
    mock_property = MagicMock()
    mock_property.name = None
    house = House(position=mock_position, players=[2, 3, 4], property=mock_property)
    assert house.__str__() == f'({mock_position}) (P: NO NAME) 3 Players'


def test_house__str__with_property_with_name():
    mock_position = MagicMock()
    mock_property = MagicMock()
    mock_property.name = 'nome_teste'
    house = House(position=mock_position, players=[2, 3, 4], property=mock_property)
    assert house.__str__() == f'({mock_position}) (P: nome_teste) 3 Players'

def test_house__repr__():
    mock_position = MagicMock()
    mock_property = MagicMock()
    mock_players = MagicMock()
    house = House(position=mock_position, players=mock_players, property=mock_property)
    assert house.__repr__() == house.__str__()
