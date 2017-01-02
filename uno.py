'''
This is an Uno game and my first attempt at a complete application in python.
'''

# TODO's:
# Better user interface
# Inform each player when someone is on their final card
# Add computer player
# Sort Cards in hand

# Used for shuffling the deck.
import random

# The amount of ranks to use. The ranks always start at 0.
NUM_RANKS = 10

# How many times to duplicate each card.
NUM_DUPLICATES = 2


class Card:
    ''' The base class for all cards. Just gives it a color. '''

    colors = ['blue', 'green', 'red', 'yellow']

    def __init__(self, color):
        self.color = color


class Ranked_Card(Card):
    '''
    Typical card, has a an integer greater than or equal to zero for rank.
    '''

    def __init__(self, color, rank):
        ''' Rank must be greater than 0. '''
        # Does no checking to make sure pre-condition is met.
        Card.__init__(self, color)
        self.rank = rank
        self.points = rank


class Action_Card(Card):
    ''' Action should be one of 'draw two', 'skip', or 'reverse' '''

    actions = ['draw 2', 'reverse', 'skip', 'wild draw 4', 'wild']

    def __init__(self, color, action):
        Card.__init__(self, color)
        self.action = action


class Player():
    ''' Class for most player acction. '''

    # Keeps track of the total number of players. This is currently used for the
    # player's name, but may be used for limiting the number of players in the
    # future.
    num_players = 0

    def __init__(self):
        '''
        Increases the number of players. Then gives the player their name.
        Then creates an empty array for the players hand.
        '''
        self.player_number = Player.num_players = Player.num_players + 1
        self.name = str(self.player_number)
        self.hand = []

    def display_hand(self):
        print('It is player', str(self.name) + "'s", 'turn')
        print('Your current hand is:')
        for card in self.hand:
            print('Card:', self.hand.index(card) + 1)
            if isinstance(card, Ranked_Card):
                print('Color:', card.color)
                print('Rank:', card.rank)
            else:
                # Hide color of wild cards
                if card.action not in ['wild draw 4', 'wild']:
                    print('Color:', card.color)

                print('Action:', card.action)
            print()

    def display_discard(discard):
        print('The current discard is:')
        print('Color:', discard[-1].color)
        if isinstance(discard[-1], Ranked_Card):
            print('Rank:', discard[-1].rank)
        else:
            print('Action:', discard[-1].action)

        print()

    def get_discard(self, discard):
        '''
        Card is the location of the card the player chooses or zero if they want
        to draw a card.
        '''

        # Will be the index in the players hand of the card to be discarded.
        # Initialized to None to change behavior of input loop after first
        # iteration.
        card = None

        # After the player has given a valid index in the array this will be
        # used to determine if the card has the same color and rank as the top
        # card on the discard pile.
        valid = False

        # Used to inform the user that the card they entered was invalid if it
        # was a valid location in the array and passed the inner while loop, but
        # the card at the location was not a valid discard.
        valid_message = False

        print('Which card would you like to discard?')
        print('Enter -1 to exit game or 0 to draw a card.')

        while not valid:
            card = None
            # Print this message after the first iteration of the outer loop.
            if valid_message:
                print('The card you entered could not be discarded')

            valid_message = True

            # This loop breaks at the end if the user entered 0. This was my
            # quick fix to 'not card' returning true when card == 0, which makes
            # the outer loop run again even though that is a valid input.
            while not isinstance(card, int) or card < -1 \
                    or card > len(self.hand):
                # Card is initialized to None, but guaranteed to be an integer
                # after the first loop
                if isinstance(card, int):
                    print('Invalid input. Please try again.')

                try:
                    card = int(input())
                except ValueError:
                    print('The input does not appear to be a number.')
                    # Make sure card is an int after first iteration.
                    card = -2

                # The outer loop would loop if it did not break here, even
                # though 0 is a valid value and intended to mean the user wants
                # to draw a card.
                if card == 0:
                    break

            # Make the card number match the zero-indexed array
            card -= 1

            # After subtracting 1, the 0 for discard becomes -1 and the -1 for
            # quitting becomes -2
            valid = card == -1 or card == -2
            if not valid:
                # Checks to make sure the given card is either the same color or
                # rank as the card on top of the discard pile.
                valid = valid or discard[-1].color == self.hand[card].color
                if isinstance(self.hand[card], Ranked_Card) \
                        and isinstance(discard[-1], Ranked_Card):
                    valid = valid or discard[-1].rank == self.hand[card].rank
                else:
                    valid = valid or isinstance(discard[-1], Action_Card) \
                        and discard[-1].action == self.hand[card].action
                    valid = valid or self.hand[card].action \
                        in ['wild draw 4', 'wild']

        return card

    def take_turn(self, deck, discard):
        self.display_hand()
        Player.display_discard(discard)
        # Card is the index of the card to discard or 0 if they player chose to
        # draw a new card.
        card = self.get_discard(discard)

        # Acts on the user input. card is guaranteed to be an int. If it is
        # greater than or equal to zero, it is the index in the players hand of
        # the card to discard. If it is -2 the player wants to quit the game.
        # Otherwise it must be -1, indicating the player wants to draw a card.
        # So if there is a card left in the deck, move it to the player's hand.
        # If there are no cards left in the deck, shuffle the extra cards from
        # the discard pile into the deck.
        if card >= 0:
            discard.append(self.hand.pop(card))
        elif card == -2:
            # I did not want to quit inside the get_discard method. This will
            # make it easier to force one exit point from the program if I want
            # to in the future and makes it easier to tell where the program is
            # exiting from.
            quit()
        elif len(deck) > 0:
            print('Drawing a card.')
            self.hand.append(deck.pop(len(deck) - 1))
        elif len(discard) > 1:
            deck.extend(discard)
            top_card = discard[-1]
            discard.clear()
            discard.append(top_card)
            shuffle(deck)

        if len(deck) == 0:
            print('No cards to draw.')

    def winner(self):
        ''' Prints a message when the player wins. '''

        print('Player', self.player_number, 'won')


def shuffle(deck):
    ''' Move each element in array deck to a random location in the array. '''

    # Fischer-Yates shuffle.
    for i in range(len(deck)):
        j = random.randint(0, len(deck) - 1)
        tmp = deck[i]
        deck[i] = deck[j]
        deck[j] = tmp


def deal(players, deck, discard, cards_per_player):
    ''' Given an array of player instances, take cards from the deck and put
    them in each player's hands. Then add one card from the deck to the discard.
    Deck must have enough cards before this runs or else an exceiption will be
    thrown.  '''

    shuffle(deck)

    # Take cards from the deck and add them to each player's hand until each
    # player has CARDS_CARDS_PER_PLAYER cards in their hand. If there are not
    # enough cards to give out, print a message.
    for player in players:
        for i in range(cards_per_player):
            player.hand.append(deck.pop(len(deck) - 1))

    card_found = False
    for card in deck:
        if isinstance(card, Ranked_Card):
            discard.append(deck.pop(deck.index(card)))
            card_found = True
            break

    if not card_found:
        print('No Ranked_Card in deck, exiting')
        quit()


def main_loop(players, deck, discard):
    ''' Main loop of the game. '''

    winner = None
    player_index = 0
    # Changes when reverse is played
    index_increase = True
    while not winner:
        players[player_index].take_turn(deck, discard)

        if len(players[player_index].hand) == 0:
            winner = players[player_index]
            break

        action = ''
        if isinstance(discard[-1], Action_Card):
            action = discard[-1].action

        if action in ['wild draw 4', 'wild']:
            new_color = ''
            while new_color not in Card.colors:
                if new_color != '':
                    print('Invalid color')

                new_color = input('What should the next color be? ')

            discard[-1].color = new_color

        index_increase = index_increase ^ bool(action == 'reverse')

        if index_increase:
            player_index += 1
            if player_index == len(players):
                player_index = 0

            if action == 'skip':
                player_index += 1
                if player_index == len(players):
                    player_index = 0

        else:
            player_index -= 1
            if player_index == -1:
                player_index = len(players) - 1

            if action == 'skip':
                player_index -= 1
                if player_index == -1:
                    player_index = len(players) - 1

        # Do not draw 2 if deck does not have at least 2 cards
        if action == 'draw 2' and len(deck) >= 2:
            for i in range(2):
                players[player_index].hand.append(deck.pop(-1))
        elif action == 'wild draw 4' and len(deck) >= 4:
            for i in range(4):
                players[player_index].hand.append(deck.pop(-1))

    winner.winner()


if __name__ == '__main__':
    valid = False
    while not valid:
        try:
            total_num_players = int(input('How many players? '))
            cards_per_player = int(input('How many cards for each player? '))
            valid = total_num_players > 0 and cards_per_player > 0
        except ValueError:
            pass
        if not valid:
            print('Not a valid number')

    deck = [Ranked_Card(color, rank) for i in range(total_num_players)
            for color in Card.colors for rank in range(NUM_RANKS)]

    for i in range(total_num_players):
        for color in Card.colors:
            for action in Action_Card.actions:
                deck.append(Action_Card(color, action))

    players = [Player() for i in range(total_num_players)]

    discard = []

    if len(deck) < total_num_players * cards_per_player + 1:
        print('Not enough cards. Exiting.')
    else:
        deal(players, deck, discard, cards_per_player)
        main_loop(players, deck, discard)
