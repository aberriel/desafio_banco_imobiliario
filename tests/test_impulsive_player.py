from collections import namedtuple
from src.house import House
from src.player.impulsive_player import ImpulsivePlayer
from unittest import TestCase
from unittest.mock import MagicMock
from pytest import fixture
import pytest


Factory = namedtuple('Factory',
                     'impulsive_player, mock_name, mock_house,'
                     'mock_properties, mock_balance, mock_order')


@fixture(scope='class')
def impulsive_fixture(request):
    def factory(name: str = MagicMock(),
                house: House = MagicMock(),
                properties: list = MagicMock(),
                balance: int = MagicMock(),
                order: int = MagicMock()):
        impulsive_player = ImpulsivePlayer(
            name=name,
            house=house,
            properties=properties,
            balance=balance,
            order=order)
        return Factory(impulsive_player, name, house, properties,
                       balance, order)
    request.cls.factory = factory


@pytest.mark.usefixtures('impulsive_fixture')
class TestImpulsivePlayer(TestCase):
    def setUp(self):
        fac = TestImpulsivePlayer.factory()
        self.impulsive_player: ImpulsivePlayer = fac.impulsive_player
        self.mock_name = fac.mock_name
        self.mock_house = fac.mock_house
        self.mock_properties = fac.mock_properties
        self.mock_balance = fac.mock_balance
        self.mock_order = fac.mock_order

    def tearDown(self):
        pass

    def test_init(self):
        assert self.impulsive_player.name == self.mock_name
        assert self.impulsive_player.house == self.mock_house
        assert self.impulsive_player.properties == self.mock_properties
        assert self.impulsive_player.balance == self.mock_balance
        assert self.impulsive_player.order == self.mock_order

    def test_buy(self):
        self.impulsive_player.balance = 100
        self.impulsive_player.player_info = {'buy_payments': []}
        self.impulsive_player.properties = []
        property = MagicMock()
        property.purchase_price = 80
        property.owner = None
        result = self.impulsive_player.buy(property)

        assert result is True
        assert self.impulsive_player.balance == 20
        assert len(self.impulsive_player.player_info['buy_payments']) == 1
        assert self.impulsive_player.player_info['buy_payments'] == [80]
        assert property.owner == self.impulsive_player
        assert len(self.impulsive_player.properties) == 1
        assert self.impulsive_player.properties == [property]

    def test_buy__negative_balance(self):
        self.impulsive_player.balance = 100
        self.impulsive_player.player_info = {'buy_payments': []}
        self.impulsive_player.properties = []
        property = MagicMock()
        property.purchase_price = 120
        property.owner = None
        result = self.impulsive_player.buy(property)

        assert result is False
        assert self.impulsive_player.balance == -20
        assert len(self.impulsive_player.player_info['buy_payments']) == 0
        assert self.impulsive_player.player_info['buy_payments'] == []
        assert self.impulsive_player.properties == []
        assert property.owner is None
