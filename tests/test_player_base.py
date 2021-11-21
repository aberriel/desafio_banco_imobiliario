from collections import namedtuple
from src.house import House
from src.player.player_base import Player
from pytest import fixture
from unittest import TestCase
from unittest.mock import MagicMock, patch

import pytest


Factory = namedtuple('Factory',
                     'player_base, mock_name, mock_house, mock_properties, '
                     'mock_balance, mock_order')


@fixture(scope='class')
def player_fixture(request):
    def factory(name: str = MagicMock(),
                house: House = MagicMock(),
                properties: list = MagicMock(),
                balance: int = MagicMock(),
                order: int = MagicMock()):
        player_base = Player(
            name=name,
            house=house,
            properties=properties,
            balance=balance,
            order=order)
        return Factory(player_base, name, house, properties,
                       balance, order)
    request.cls.factory = factory


@pytest.mark.usefixtures('player_fixture')
class TestPlayerBase(TestCase):
    def setUp(self):
        fac = TestPlayerBase.factory()
        self.player_base: Player = fac.player_base
        self.mock_name: str = fac.mock_name
        self.mock_house: House = fac.mock_house
        self.mock_properties: list = fac.mock_properties
        self.mock_balance: int = fac.mock_balance
        self.mock_order: int = fac.mock_order

    def tearDown(self):
        pass

    def test_init(self):
        assert self.player_base.name == self.mock_name
        assert self.player_base.house == self.mock_house
        assert self.player_base.properties == self.mock_properties
        assert self.player_base.balance == self.mock_balance
        assert self.player_base.order == self.mock_order

    def test_rent_success(self):
        self.player_base.balance = 300
        property = MagicMock()
        property.rent_amount = 20
        property.owner = MagicMock()
        property.owner.balance = 300
        property.owner.player_info = {'amounts_received': []}

        result = self.player_base.rent(property)

        assert self.player_base.balance == 280
        assert property.owner.balance == 320
        assert len(self.player_base.player_info['rent_payments']) == 1
        assert self.player_base.player_info['rent_payments'] == [20]
        assert len(property.owner.player_info['amounts_received']) == 1
        assert property.owner.player_info['amounts_received'] == [20]
        assert result is True

    def test_rent_mine(self):
        self.player_base.balance = 300
        property = MagicMock()
        property.rent_amount = 20
        property.owner = self.player_base
        result = self.player_base.rent(property)

        assert result is True
        assert self.player_base.balance == 300
        assert self.player_base.player_info['rent_payments'] == []
        assert property.owner.player_info['amounts_received'] == []

    def test_rent_final_balance_negative(self):
        self.player_base.balance = 80
        property = MagicMock()
        property.rent_amount = 100
        property.owner = MagicMock()
        property.owner.balance = 300
        property.owner.player_info = {'rent_payments': [], 'amounts_received': []}
        result = self.player_base.rent(property)

        assert result is False
        assert self.player_base.balance == -20
        assert self.player_base.player_info['rent_payments'] == []
        assert property.owner.player_info['amounts_received'] == []

    @patch.object(Player, 'buy')
    @patch.object(Player, 'rent')
    def test_buy_or_rent__without_property(self, mock_rent, mock_buy):
        result = self.player_base.buy_or_rent()
        assert result is True
        mock_buy.assert_not_called()
        mock_rent.assert_not_called()

    @patch.object(Player, 'buy')
    @patch.object(Player, 'rent')
    def test_buy_or_rent__call_buy(self, mock_rent, mock_buy):
        property = MagicMock()
        property.owner = None
        result = self.player_base.buy_or_rent(property)
        assert result == mock_buy()
        mock_buy.assert_called()
        mock_rent.assert_not_called()

    @patch.object(Player, 'buy')
    @patch.object(Player, 'rent')
    def test_buy_or_rent__call_rent(self, mock_rent, mock_buy):
        property = MagicMock()
        result = self.player_base.buy_or_rent(property)
        assert result == mock_rent()
        mock_buy.assert_not_called()
        mock_rent.assert_called()

    def test_lose_all(self):
        property_1 = MagicMock()
        property_1.owner = MagicMock()
        property_2 = MagicMock()
        property_2.owner = MagicMock()
        property_3 = MagicMock()
        property_3.owner = MagicMock()
        list_properties = [property_1, property_2, property_3]
        self.player_base.properties = list_properties
        self.player_base.lose_all()

        assert property_1.owner is None
        assert property_2.owner is None
        assert property_3.owner is None

    def test_next_house(self):
        self.player_base.house = 16
        result = self.player_base.get_next_house(2, 20)
        assert result == 18

    def test_next_house_back_to_start(self):
        self.player_base.house = 16
        result = self.player_base.get_next_house(6, 20)
        assert result == 1
