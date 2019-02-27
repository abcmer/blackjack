"""Test module."""
import unittest

from blackjack import Table, Player, Card, Hand, is_valid_bet_amt

class SetUpGame(unittest.TestCase):
    """Test case for Table."""
    def setUp(self):
        self.table = Table(min_bet=10, max_bet=25)
        player_configs = [{
            'id': 1,
            'name': 'Player 1',
            'chips': 100
        }, {
            'id': 2,
            'name': 'Player 2',
            'chips': 100
        }]
        self.players = [Player(pc) for pc in player_configs]

    def test_add_players(self):
        """Test add players."""
        for player in self.players:
            self.table.add_player(player)
        self.assertEqual(len(self.table.players), 2)

class TestPlayer(unittest.TestCase):
    """Test case for player."""

    def setUp(self):
        player_config = {
        'id': 1,
        'name': 'Chris Money Maker',
        'chips': 100
    }
        self.player = Player(player_config)

    def test_add_chips(self):
        """Test add chips to player."""
        self.player.add_chips(10)
        self.assertEqual(self.player.chips, 110)

    def test_subtract_chips(self):
        """Test subtract chips from player."""
        self.player.subtract_chips(10)
        self.assertEqual(self.player.chips, 90)

class TestHand(unittest.TestCase):
    """Test case for hand."""

    def setUp(self):
        """Setup function."""
        self.hand = Hand()

    def test_set_status(self):
        self.hand.set_status('hit')
        self.assertEqual(self.hand.status, 'hit')

    def test_invalid_status(self):
        with self.assertRaises(Exception) as context:
            self.hand.set_status('Its Complicated')

    def test_check_for_blackjack(self):
        self.hand.cards = [
            Card('Ace', 'Hearts'),
            Card('Jack', 'Clubs')
        ]
        is_blackjack = self.hand.check_for_blackjack()    
        self.assertTrue(is_blackjack)    
        self.assertEqual(self.hand.status, 'blackjack')  

    def test_not_a_blackjack(self):
        """Test check_for_blackjack() when not a blackjack."""
        self.hand.cards = [
            Card('King', 'Hearts'),
            Card('Jack', 'Clubs')
        ]
        is_blackjack = self.hand.check_for_blackjack()    
        self.assertFalse(is_blackjack)    
        self.assertEqual(self.hand.status, None)  

    def test_false_blackjack(self):
        """Test check_for_black() returns None for a hand with more than 2 cards."""
        self.hand.cards = [
            Card('10', 'Hearts'),
            Card('9', 'Clubs'),
            Card('2','Spades')
        ]
        is_blackjack = self.hand.check_for_blackjack()   
        self.assertFalse(is_blackjack)    
        self.assertEqual(self.hand.status, None)  

    def test_hit(self):
        """Test hit."""
        self.hand.cards = [
            Card('5', 'Hearts'),
            Card('10', 'Clubs')
        ]
        self.hand.hit(Card('4','Spades'))
        self.assertEqual(len(self.hand.cards), 3)
        self.assertEqual(self.hand.calculate_total(), 19)

    def test_calulate_total(self):
        """Test calculate total."""
        self.hand.cards = [
            Card('2', 'Hearts'),
            Card('3', 'Clubs'),
            Card('6', 'Diamonds'),
            Card('4', 'Spades'),
            Card('5', 'Hearts')
        ]
        self.assertEqual(self.hand.calculate_total(), 20)

    def test_check_for_bust_positive(self):
        """Test check for bust."""
        self.hand.cards = [
            Card('10', 'Hearts'),
            Card('4', 'Clubs'),
            Card('King','Spades')
        ]
        is_bust = self.hand.check_for_bust()   
        self.assertTrue(is_bust)    
        self.assertEqual(self.hand.status, 'bust') 

    def test_check_for_bust_negative(self):
        """Test check for bust."""
        self.hand.cards = [
            Card('10', 'Hearts'),
            Card('4', 'Clubs'),
            Card('6','Spades')
        ]
        is_bust = self.hand.check_for_bust()   
        self.assertFalse(is_bust)
        self.assertEqual(self.hand.status, None)  

    def test_set_bet_amt(self):
        """Test set bet amt."""
        self.hand.set_bet_amt(10)
        self.assertEqual(self.hand.bet_amt, 10)


class TestDealCards(unittest.TestCase):
    """Test case for dealing cards."""

    def setUp(self):
        self.table = Table(min_bet=10, max_bet=25)
        player_configs = [{
            'id': 1,
            'name': 'Player 1',
            'chips': 100
        }, {
            'id': 2,
            'name': 'Player 2',
            'chips': 100
        }]
        self.table.players = [Player(pc) for pc in player_configs]
        self.table.deal_cards()

    def test_deal_cards_basic(self):
        """Test deal cards and assert each player got 2 cards."""
        self.table.deal_cards()
        for player in self.table.players:
            self.assertEqual(len(player.hand.cards), 2)
        self.assertEqual(len(self.table.dealer.hand.cards), 2)

    def test_not_enough_cards(self):
        """Test dealing when not enough cards in the shoe."""
        self.table.shoe.cards = self.table.shoe.cards[0:2] # Set deck to two cards
        self.table.deal_cards()
        for player in self.table.players:
            self.assertEqual(len(player.hand.cards), 2)
        self.assertEqual(len(self.table.dealer.hand.cards), 2)
        

class TestValidations(unittest.TestCase):
    """Test case for player input validations."""

    def test_valid_bet_amt(self):
        """Test validate bet amt input."""
        self.assertTrue(is_valid_bet_amt(15, 10, 20, 100))

    def test_bet_below_min(self):
        """Test invalid bet below min."""
        self.assertFalse(is_valid_bet_amt(5, 10, 20, 100)) 

    def test_bet_above_max(self):
        """Test invalid bet above max."""
        self.assertFalse(is_valid_bet_amt(5, 10, 20, 100))

        

