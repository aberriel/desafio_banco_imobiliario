from collections import namedtuple
from src.house import House
from src.player.cautious_player import CautiousPlayer
from unittest import TestCase
from unittest.mock import MagicMock, patch
from pytest import fixture

import pytest


Factory = namedtuple('Factory',
                     'cautious_player, mock_name, mock_house,'
                     'mock_properties, mock_balance, mock_order')


@fixture(scope='class')
def cautious_fixture(request):
    def factory(name: str = MagicMock(),
                house: House = MagicMock(),
                properties: list = MagicMock(),
                balance: int = MagicMock(),
                order: int = MagicMock()):
        cautious_player = CautiousPlayer(
            name=name,
            house=house,
            properties=properties,
            balance=balance,
            order=order)
        return Factory(cautious_player, name, house, properties,
                       balance, order)
    request.cls.factory = factory


@pytest.mark.usefixtures('cautious_fixture')
class TestCautiousPlayer(TestCase):
    def setUp(self):
        fac = TestCautiousPlayer.factory()
        self.cautious_player: CautiousPlayer = fac.cautious_player
        self.mock_name = fac.mock_name
        self.mock_house = fac.mock_house
        self.mock_properties = fac.mock_properties
        self.mock_balance = fac.mock_balance
        self.mock_order = fac.mock_order

    def tearDown(self):
        pass

    def test_init(self):
        assert self.cautious_player.name == self.mock_name
        assert self.cautious_player.house == self.mock_house
        assert self.cautious_player.properties == self.mock_properties
        assert self.cautious_player.balance == self.mock_balance
        assert self.cautious_player.order == self.mock_order

    def test_buy__can_buy(self):
        property = MagicMock()
        property.purchase_price = 100
        property.owner = None
        self.cautious_player.balance = 200
        self.cautious_player.properties = []
        self.cautious_player.player_info = {'buy_payments': []}
        response = self.cautious_player.buy(property)

        assert response is True
        assert len(self.cautious_player.properties) == 1
        assert self.cautious_player.properties == [property]
        assert property.owner == self.cautious_player
        assert self.cautious_player.balance == 100
        assert len(self.cautious_player.player_info['buy_payments']) == 1
        assert self.cautious_player.player_info['buy_payments'] == [100]

    def test_buy_cannot_buy(self):
        property = MagicMock()
        property.purchase_price = 180
        property.owner = None
        self.cautious_player.balance = 200
        self.cautious_player.properties = []
        self.cautious_player.player_info = {'buy_payments': []}
        response = self.cautious_player.buy(property)

        assert response is True
        assert len(self.cautious_player.properties) == 0
        assert self.cautious_player.properties == []
        assert property.owner is None
        assert self.cautious_player.balance == 200
        assert len(self.cautious_player.player_info['buy_payments']) == 0
        assert self.cautious_player.player_info['buy_payments'] == []
