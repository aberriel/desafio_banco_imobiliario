from collections import namedtuple
from src.game import Game
from unittest import TestCase
from unittest.mock import MagicMock
from pytest import fixture

import pytest


Factory = namedtuple('Factory',
                     'mock_round, mock_players, mock_houses, mock_actual_player,'
                     'players_report_info')