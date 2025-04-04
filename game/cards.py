from game.constants import SUITS, RANKS, NUM_DECKS
import random


def create_deck(num_decks=NUM_DECKS):
    return [(rank, suit) for _ in range(num_decks) for suit in SUITS.keys() for rank in RANKS.keys()]

def deal_card(deck):
    return deck.pop(random.randint(0, len(deck) - 1))

def calculate_hand_value(hand):
    value = sum(RANKS[rank] for rank, _ in hand)
    aces = sum(1 for rank, _ in hand if rank == 'A')
    while value > 21 and aces:
        value -= 10
        aces -= 1
    return value

def suggest_move(player_hand, dealer_upcard):
    player_value = calculate_hand_value(player_hand)
    dealer_upcard_value = RANKS[dealer_upcard[0]]

    if 'A' in [card[0] for card in player_hand]:
        return "Hit" if player_value <= 17 or (player_value == 18 and dealer_upcard_value in [9, 10, 11]) else "Stand"

    return "Hit" if player_value <= 11 or (player_value == 12 and dealer_upcard_value not in [4, 5, 6]) or \
                    (13 <= player_value <= 16 and dealer_upcard_value > 6) else "Stand"