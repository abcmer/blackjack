import itertools
from random import shuffle
import time


class Table(object):
    """Table class."""

    def __init__(self, min_bet=5, max_bet=100):
        self.game_mode = 'debug'
        self.min_bet = min_bet
        self.max_bet = max_bet
        self.players = []
        self.dealer = Player({'id': 'dealer', 'name': 'Max', 'chips': 1000000})
        self.shoe = Shoe(1)
        self.game_on = False

    def add_player(self, player):
        """Adds a player."""
        self.players.append(player)

    def remove_player(self, player_id):
        """Remove player."""
        player_to_remove = [
            player for player in self.players if player.id == player_id
        ][0]

    def start_game(self):
        """Start game."""
        self.game_on = True
        self.shoe.shuffle()
        while any([player.chips >= self.min_bet for player in self.players]):
            self.clear_table()
            self.take_bets()
            self.deal_cards()
            self.play_hand()
            self.pay_out_and_collect()

        print('GAME OVER!')

    def take_bets(self):
        """Take bets."""
        for player in self.players:
            while True:
                bet_amt = input(f'{player} how much would you like to bet? ')
                if not is_valid_bet_amt(bet_amt, self.min_bet, self.max_bet,
                                        player.chips):
                    continue
                else:
                    break
            player.hand.set_bet_amt(int(bet_amt))

    def clear_table(self):
        # Add old cards to discard_pile for each player
        for player in self.players:
            if player.hand:
                self.shoe.discard_pile += player.hand.cards
            player.hand = Hand()

        # Add dealers cards to discard pile
        if self.dealer.hand:
            self.shoe.discard_pile += self.dealer.hand.cards
        self.dealer.hand = Hand()

    def deal_cards(self):
        """Deal cards."""
        game_command('Dealing the cards...')
        # sleep(.5 * len(self.players))
        # done_dealing is true when all players and the dealer have 2 cards
        done_dealing = all(
            [[len(player.hand.cards) == 2 for player in self.players],
             len(self.dealer.hand.cards) == 2])

        while not done_dealing:
            for player in self.players:
                if len(player.hand.cards) < 2:
                    player.hand.cards.append(self.shoe.get_top_card())
            self.dealer.hand.cards.append(self.shoe.get_top_card())
            # reset done_dealing
            done_dealing = all(
                [[len(player.hand.cards) == 2 for player in self.players],
                 len(self.dealer.hand.cards) == 2])

    def play_hand(self):
        """Play Hand."""

        if self.dealer.hand.check_for_blackjack():
            print(f'BLACKJACK FOR DEALER {hand}')
            # Set all other player hands to dealer_blackjack
            for player in self.players:
                player.hand.set_status('dealer_blackjack')

        for player in self.players:
            hand = player.hand

            if hand.check_for_blackjack():
                print(f'BLACKJACK FOR {player} with {hand}!!!!')
                continue

            while hand.status not in ('bust', 'stay', 'dealer_blackjack'):
                if 'Ace' in [card.rank for card in hand.cards]:
                    total = hand.calculate_total()
                    print(
                        f'{player} you have {player.hand} for a total of {total} (or {total - 10})'
                    )
                    game_legend('H=Hit, S=Stay')
                    decision = input('Decision:')
                    ace = [card for card in hand.cards
                           if card.rank == 'Ace'][0]
                    # TODO -- Add logic for changing 11 to 1 if bust
                else:
                    print('')
                    print(
                        f'{player} you have {player.hand} for a total of {player.hand.calculate_total()}.'
                    )
                    print('What would you like to do?')
                    game_legend('H=Hit, S=Stay')
                    decision = input('Decision: ')

                if decision == 'H':
                    hand.set_status('hit')
                    hand.hit(self.shoe.get_top_card())
                    if hand.check_for_bust():
                        print(f'{player} BUSTS!!!!!')
                    if hand.calculate_total() == 21:
                        print(f'Nice Hit {player}')
                        print(
                            f'You have {player.hand} for a total of {player.hand.calculate_total()}.'
                        )
                        hand.set_status('stay')
                elif decision == 'S':
                    hand.set_status('stay')
                    continue

        # Process dealers turn
        dealer_hand = self.dealer.hand
        while (dealer_hand.calculate_total() < 17):
            dealer_hand.hit(self.shoe.get_top_card())
            if dealer_hand.check_for_bust():
                print(f'DEALER BUSTS with {dealer_hand}')

    def pay_out_and_collect(self):
        """Pay out and collect."""
        dealer_hand = self.dealer.hand
        print(
            f'Dealer has {dealer_hand} for a total of {dealer_hand.calculate_total()}'
        )
        dealer_total = self.dealer.hand.calculate_total()

        # For each player check if they beat dealer
        for player in self.players:
            hand = player.hand
            bet_amt = player.hand.bet_amt

            if hand.calculate_total() > 21:
                player.subtract_chips(bet_amt)
                print(
                    f'{player} loses {bet_amt} dollars. Total remaining chips: {player.chips}'
                )
            elif dealer_total > 21:
                player.add_chips(bet_amt)
                print(
                    f'{player} wins {bet_amt} dollars. Total remaining chips: {player.chips}'
                )
            elif (hand.calculate_total() > dealer_total):
                player.add_chips(bet_amt)
                print(
                    f'{player} wins {bet_amt} dollars. Total remaining chips: {player.chips}'
                )
            elif (hand.status == 'blackjack') and (
                    dealer_hand.status == 'blackjack'):
                print(f'{player} and dealer both have blackjack. PUSH')
            elif (hand.calculate_total() <= dealer_total):
                player.subtract_chips(bet_amt)
                print(
                    f'{player} loses {bet_amt} dollars. Total remaining chips: {player.chips}'
                )


class Shoe(object):
    """Shoe class."""

    def __init__(self, deck_count=6):
        suits = ['Spades', 'Clubs', 'Diamonds', 'Hearts']
        ranks = [
            '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen',
            'King', 'Ace'
        ]
        # Create deck of cards and multiply by deck_count to create shoe
        self.cards = [Card(rank, suit) for suit in suits
                      for rank in ranks] * deck_count
        self.discard_pile = []

    def shuffle(self):
        """Shuffle the cards."""
        game_command('Dealer is shuffling...')
        # sleep(3)
        shuffle(self.cards)

    def reset(self):
        """Move all cards from discard pile to shoe."""
        self.cards = self.discard_pile
        self.discard_pile = []
        # sleep(3) # Simulate reset time when game mode is not debug
        self.shuffle()

    def get_top_card(self):
        """Gets top card from the shoe, handles end of shoe."""
        if len(self.cards) > 0:
            return self.cards.pop(0)
        else:  # If no more cards, reset the shoe
            print('Dealer is resetting the shoe...')
            self.reset()
            return self.get_top_card()


class Card(object):
    """Card class."""

    def __init__(self, rank, suit):
        if rank in ('Jack', 'Queen', 'King'):
            value = 10
        elif rank == 'Ace':
            value = 11
        else:
            value = int(rank)
        self.rank = rank
        self.suit = suit
        self.value = value

    def __repr__(self):
        return f'{self.rank} of {self.suit}'


class Player(object):
    """Player class."""

    def __init__(self, player_config):
        self.id = player_config['id']
        self.name = player_config['name']
        self.chips = player_config['chips']
        self.hand = Hand()

    def __repr__(self):
        return f'{self.name}'

    def add_chips(self, amt):
        """Add amt to players chips."""
        self.chips += amt

    def subtract_chips(self, amt):
        """Subtract amt fro players chips."""
        self.chips -= amt


class Hand(object):
    """Hand class."""

    def __init__(self):
        self.bet_amt = 0
        self.cards = []
        self.status = None

    def __repr__(self):
        return f'{self.cards}'

    def calculate_total(self):
        return sum([card.value for card in self.cards])

    def set_status(self, status):
        assert status in ('hit', 'stay', 'split', 'bust', 'double', 'ace',
                          'blackjack', 'dealer_blackjack')
        self.status = status

    def set_outcome(self, outcome):
        assert outcome in ('win', 'lose')

    def check_for_blackjack(self):
        if (self.calculate_total() == 21) and (len(self.cards) == 2):
            self.status = 'blackjack'
            return True

    def hit(self, card):
        self.cards.append(card)
        self.set_status('hit')

    def check_for_bust(self):
        """Check if total of cards is greater than 21."""
        if self.calculate_total() > 21:
            self.set_status('bust')
            self.set_outcome('lose')
            return True

    def set_bet_amt(self, amt):
        """Set current bet to the amount provided."""
        self.bet_amt = amt


def is_valid_bet_amt(amt, min_bet, max_bet, chips_available):
    """Validates player input of bet amt."""
    try:
        amt = int(amt)
    except ValueError:
        game_warning('Bet amount must be full dollar')
        return False
    if not (min_bet <= amt <= max_bet):
        game_warning(f'Amount must be between ${min_bet} and ${max_bet}')
        return False
    elif amt > chips_available:
        game_warning('You may not bet more than you have')
    else:
        return True


def sleep(seconds):
    time.sleep(seconds) if MODE != 'debug' else time.sleep(0)


def game_command(message):
    print('')
    print(f'{message}')
    print('')


def game_legend(message):
    print('')
    print(f'     {message}')
    print('')


def game_warning(message):
    print(f'*** {message} ***')
    print('')


if __name__ == "__main__":
    """Simulate a game."""

    MODE = 'debug'
    players = [{
        'id': 1,
        'name': 'Player 1',
        'chips': 100
    }, {
        'id': 2,
        'name': 'Player 2',
        'chips': 100
    }]

    # Create a game
    table = Table(min_bet=10, max_bet=25)

    # Add players to the table
    for player_config in players:
        player = Player(player_config)
        table.add_player(player)

    table.start_game()
