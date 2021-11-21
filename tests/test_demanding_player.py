from collections import namedtuple
from src.house import House
from src.player.demanding_player import DemandingPlayer
from unittest import TestCase
from unittest.mock import MagicMock
from pytest import fixture

import pytest


Factory = namedtuple('Factory',
                     'demanding_player, mock_name, mock_house,'
                     'mock_properties, mock_balance, mock_order')


@fixture(scope='class')
def demanding_fixture(request):
    def factory(name: str = MagicMock(),
                house: House = MagicMock(),
                properties: list = MagicMock(),
                balance: int = MagicMock(),
                order: int = MagicMock()):
        demanding_player = DemandingPlayer(
            name=name,
            house=house,
            properties=properties,
            balance=balance,
            order=order)
        return Factory(demanding_player, name, house, properties,
                       balance, order)
    request.cls.factory = factory


@pytest.mark.usefixtures('demanding_fixture')
class TestDemandingPlayer(TestCase):
    def setUp(self):
        fac = TestDemandingPlayer.factory()
        self.demanding_player: DemandingPlayer = fac.demanding_player
        self.mock_name = fac.mock_name
        self.mock_house = fac.mock_house
        self.mock_properties = fac.mock_properties
        self.mock_balance = fac.mock_balance
        self.mock_order = fac.mock_order

    def tearDown(self):
        pass

    def test_init(self):
        assert self.demanding_player.name == self.mock_name
        assert self.demanding_player.house == self.mock_house
        assert self.demanding_player.properties == self.mock_properties
        assert self.demanding_player.balance == self.mock_balance
        assert self.demanding_player.order == self.mock_order

    def test_buy_success(self):
        self.demanding_player.balance = 300
        self.demanding_player.player_info = {'buy_payments': []}
        self.demanding_player.properties = []
        property = MagicMock()
        property.purchase_price = 150
        property.rent_amount = 90
        property.owner = None
        response = self.demanding_player.buy(property)

        assert response is True
        assert self.demanding_player.balance == 150
        assert len(self.demanding_player.player_info['buy_payments']) == 1
        assert self.demanding_player.player_info['buy_payments'] == [150]
        assert len(self.demanding_player.properties) == 1
        assert self.demanding_player.properties == [property]
        assert property.owner == self.demanding_player

    def test_buy__not_buy_by_value(self):
        self.demanding_player.balance = 300
        self.demanding_player.player_info = {'buy_payments': []}
        self.demanding_player.properties = []
        property = MagicMock()
        property.purchase_price = 150
        property.rent_amount = 10
        property.owner = None
        response = self.demanding_player.buy(property)

        assert response is True
        assert self.demanding_player.balance == 300
        assert len(self.demanding_player.player_info['buy_payments']) == 0
        assert self.demanding_player.player_info['buy_payments'] == []
        assert len(self.demanding_player.properties) == 0
        assert self.demanding_player.properties == []
        assert property.owner is None

    def test_buy__negative_balance(self):
        self.demanding_player.balance = 130
        self.demanding_player.player_info = {'buy_payments': []}
        self.demanding_player.properties = []
        property = MagicMock()
        property.purchase_price = 150
        property.rent_amount = 90
        property.owner = None
        response = self.demanding_player.buy(property)

        assert response is False
        assert self.demanding_player.balance == -20
        assert len(self.demanding_player.player_info['buy_payments']) == 0
        assert self.demanding_player.player_info['buy_payments'] == []
        assert len(self.demanding_player.properties) == 0
        assert self.demanding_player.properties == []
        assert property.owner is None
