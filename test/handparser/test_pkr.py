from datetime import datetime
from decimal import Decimal as D
from collections import OrderedDict
import pytz
from pytz import UTC
from pytest import mark, fixture
from poker.handhistory import HandHistoryPlayer
from poker.room.pkr import PKRHandHistory
from poker.card import Card
from poker.hand import Combo
from .pkr_hands import HANDS


@fixture
def hand_header(request):
    h = PKRHandHistory(request.instance.hand_text)
    h.parse_header()
    return h


@fixture
def hand(request):
    hh = PKRHandHistory(request.instance.hand_text)
    hh.parse()
    return hh

class TestHoldemHand:
    hand_text = HANDS['holdem_full']

    @mark.parametrize('attribute, expected_value', [
        ('game_type', 'CASH'),
        ('sb', D('0.25')),
        ('bb', D('0.50')),
        ('date', UTC.localize(datetime(2013, 10, 5, 1, 15, 45))),
        ('game', 'HOLDEM'),
        ('limit', 'NL'),
        ('ident', '2433297728'),
        ('last_ident', '2433297369'),
        ('tournament_ident', None),
        ('tournament_name', None),
        ('tournament_level', None),
        ('table_name', "#52121155 - Rapanui's Leela"),
        ('buyin', D('50')),
        ('currency', 'USD'),
        ('money_type', 'R'),
    ])
    def test_header(self, hand_header, attribute, expected_value):
        assert getattr(hand_header, attribute) == expected_value


    @mark.parametrize('attribute, expected_value', [
        ('players', [
        HandHistoryPlayer(name='laxi23', stack=D('51.89'), seat=1, combo=None),
        HandHistoryPlayer(name='NikosMRF', stack=D('50'), seat=2, combo=None),
        HandHistoryPlayer(name='Capricorn', stack=D('33.6'), seat=3, combo=None),
        HandHistoryPlayer(name='Walkman', stack=D('50'), seat=4, combo=Combo('9s6d')),
        HandHistoryPlayer(name='Empty Seat 5', stack=0, seat=5, combo=None),
        HandHistoryPlayer(name='barly123', stack=D('50.35'), seat=6, combo=None),
        ]),
        ('button', HandHistoryPlayer(name='Capricorn', stack=D('33.6'), seat=3, combo=None)),
        ('max_players', 6),   # maybe imprecise
        ('hero', HandHistoryPlayer(name='Walkman', stack=D('50'), seat=4, combo=Combo('9s6d'))),
        ('preflop_actions', ('laxi23 folds',
                           'Capricorn calls $0.50',
                           'Walkman folds',
                           'barly123 raises to $1.25',
                           'Capricorn calls $1.25')),
        ('flop', (Card('7d'), Card('3c'), Card('Jd'))),
        ('flop_pot', D('2.75')),
        ('flop_actions', ('barly123 checks',
                        'Capricorn bets $1.37',
                        'barly123 raises to $4.11',
                        'Capricorn calls $4.11')),
        ('turn', Card('Js')),
        ('turn_pot', D('10.97')),
        ('turn_actions', ('barly123 checks', 'Capricorn checks')),
        ('river', Card('5h')),
        ('river_pot', D('10.97')),
        ('river_actions', ('barly123 checks', 'Capricorn checks')),
        ('total_pot', D('10.97')),
        ('rake', D('0.54')),
        ('winners', ('barly123',)),
        ('show_down', True),
        ('board', (Card('7d'), Card('3c'), Card('Jd'), Card('Js'), Card('5h')))
        ])
    def test_body(self, hand, attribute, expected_value):
        assert getattr(hand, attribute) == expected_value
