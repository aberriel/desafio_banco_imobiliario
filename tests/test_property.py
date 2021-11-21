from src.property import Property
from unittest.mock import MagicMock


def test_create_property():
    mock_purchase_price = MagicMock()
    mock_rent_amount = MagicMock()
    mock_name = MagicMock()
    mock_owner = MagicMock()
    mock_house = MagicMock()
    property = Property(
        purchase_price=mock_purchase_price,
        rent_amount=mock_rent_amount,
        name=mock_name,
        owner=mock_owner,
        house=mock_house)
    assert property.purchase_price == mock_purchase_price
    assert property.rent_amount == mock_rent_amount
    assert property.name == mock_name
    assert property.owner == mock_owner
    assert property.house == mock_house


def test_property__str__with_name():
    mock_purchase_price = MagicMock()
    mock_rent_amount = MagicMock()
    mock_owner = MagicMock()
    mock_house = MagicMock()
    property = Property(
        purchase_price=mock_purchase_price,
        rent_amount=mock_rent_amount,
        name='A Casa',
        owner=mock_owner,
        house=mock_house)
    assert property.__str__() == f'A Casa | C: R${mock_purchase_price} | A: R${mock_rent_amount}'


def test_property__str__without_name():
    mock_purchase_price = MagicMock()
    mock_rent_amount = MagicMock()
    mock_owner = MagicMock()
    mock_house = MagicMock()
    property = Property(
        purchase_price=mock_purchase_price,
        rent_amount=mock_rent_amount,
        name=None,
        owner=mock_owner,
        house=mock_house)
    assert property.__str__() == f'C: R${mock_purchase_price} | A: R${mock_rent_amount}'


def test_to_json_with_owner():
    mock_purchase_price = MagicMock()
    mock_rent_amount = MagicMock()
    mock_name = MagicMock()
    mock_owner = MagicMock()
    mock_owner.name = 'Anselmo'
    mock_house = MagicMock()
    property = Property(
        purchase_price=mock_purchase_price,
        rent_amount=mock_rent_amount,
        name=mock_name,
        owner=mock_owner,
        house=mock_house)
    assert property.to_json() == {
        'owner': 'Anselmo',
        'purchase_price': mock_purchase_price,
        'rent_amount': mock_rent_amount,
        'name': mock_name,
        'house': mock_house}


def test_to_json_without_owner():
    mock_purchase_price = MagicMock()
    mock_rent_amount = MagicMock()
    mock_name = MagicMock()
    mock_house = MagicMock()
    property = Property(
        purchase_price=mock_purchase_price,
        rent_amount=mock_rent_amount,
        name=mock_name,
        owner=None,
        house=mock_house)
    assert property.to_json() == {
        'owner': 'NO OWNER',
        'purchase_price': mock_purchase_price,
        'rent_amount': mock_rent_amount,
        'name': mock_name,
        'house': mock_house}
