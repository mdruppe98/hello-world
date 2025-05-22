import random
from .cards import Card, Deck
from .player import Player

class CrazyEightsGame:
    NUM_CARDS_TO_DEAL = 5 # Standard rule, can be 7 or 8 too

    def __init__(self, player_names):
        if not 2 <= len(player_names) <= 6: # Typically 2-4, but allowing up to 6
            raise ValueError("Crazy Eights is typically played by 2 to 6 players.")
        
        self.deck = Deck()
        self.players = [Player(name) for name in player_names]
        self.discard_pile = []
        self.current_player_index = 0
        self.active_suit = None # For when an Eight is played, this stores the chosen suit
        self.game_over = False
        self.winner = None

        self._deal_initial_cards()
        self._initialize_starter_card()

    def _deal_initial_cards(self):
        for _ in range(self.NUM_CARDS_TO_DEAL):
            for player in self.players:
                card = self.deck.deal()
                if card:
                    player.add_card_to_hand(card)
                else:
                    raise Exception("Not enough cards in deck to deal initial hands.")

    def _initialize_starter_card(self):
        starter_card = self.deck.deal()
        if not starter_card:
            raise Exception("Deck is empty, cannot draw a starter card.")

        while starter_card.is_eight:
            print("An Eight was drawn as the starter card. Burying it in the deck and drawing another.")
            # Simplest way to bury: add to a temporary list, then add deck, then shuffle deck.
            # More robust would be to insert at a random position.
            temp_deck_cards = self.deck.cards 
            self.deck.cards = [] # Clear current deck
            self.deck.cards.append(starter_card) # Add the eight
            self.deck.cards.extend(temp_deck_cards) # Add rest of the cards
            self.deck.shuffle() # Re-shuffle
            
            starter_card = self.deck.deal()
            if not starter_card:
                 raise Exception("Deck became empty while trying to find a non-Eight starter card.")

        self.discard_pile.append(starter_card)
        self.active_suit = starter_card.suit # Initial suit is the suit of the starter card

    def get_current_player(self):
        return self.players[self.current_player_index]

    def get_top_card_discard_pile(self):
        if not self.discard_pile:
            return None
        return self.discard_pile[-1]

    def is_valid_play(self, card_to_play):
        top_card = self.get_top_card_discard_pile()
        # This should ideally not be called if top_card is None, but as a safeguard:
        if not top_card: 
            return True # No card on discard pile, any card is valid (should only be at game start)

        if card_to_play.is_eight:
            return True
        
        # If an Eight was the last card played, match the active_suit declared for it
        if top_card.is_eight:
            return card_to_play.suit == self.active_suit
        
        # Standard play: match suit or rank of the top card
        return card_to_play.suit == top_card.suit or card_to_play.rank == top_card.rank

    def play_card(self, player, card_index_in_hand, chosen_suit_for_eight=None):
        if player != self.get_current_player():
            # It's good practice to return a more informative error or raise an exception
            return False, "It's not this player's turn."

        if not 0 <= card_index_in_hand < len(player.hand):
            return False, "Invalid card index."

        card_to_play = player.hand[card_index_in_hand]

        if not self.is_valid_play(card_to_play):
            # Provide more specific feedback if possible
            top_card = self.get_top_card_discard_pile()
            expected_suit = self.active_suit if top_card.is_eight else top_card.suit
            return False, f"Invalid play. Card must match rank ({top_card.rank}) or suit ({expected_suit}), or be an Eight."

        # Valid play
        # remove_card_from_hand should ideally take the card object itself or its index
        # If it takes the card object, ensure the object in hand is the one being removed
        player.hand.pop(card_index_in_hand) # More direct if index is known
        self.discard_pile.append(card_to_play)
        
        if card_to_play.is_eight:
            if not chosen_suit_for_eight or chosen_suit_for_eight not in Card.SUITS:
                # This state should ideally be prevented by UI forcing a choice
                return False, "An Eight was played, but a valid suit was not chosen. This is an internal error."
            self.active_suit = chosen_suit_for_eight
            message = f"{player.name} played an {card_to_play} and chose {chosen_suit_for_eight}."
        else:
            self.active_suit = card_to_play.suit # The suit of the played card is now the active suit
            message = f"{player.name} played {card_to_play}."

        if player.has_empty_hand():
            self.game_over = True
            self.winner = player
            return True, f"{message} {player.name} wins!"
        
        return True, message


    def draw_card_for_player(self, player):
        if player != self.get_current_player():
            return None, "It's not this player's turn to draw."

        if self.deck.is_empty():
            if len(self.discard_pile) <= 1: # Only top card, or empty discard (shouldn't happen)
                return None, "Stock is empty and no cards in discard pile to reshuffle. Player must pass if unable to play."

            print("Stock is empty. Reshuffling discard pile (excluding top card) into stock...")
            top_card = self.discard_pile.pop() # Keep the top card
            self.deck.cards = self.discard_pile[:-1] # All but the last one (which is now top_card)
            self.deck.shuffle()
            self.discard_pile = [top_card] # Reset discard pile with only the previous top card
            
            if self.deck.is_empty(): # Still empty after trying to reshuffle (e.g. only 1 card was in discard)
                 return None, "Stock is empty after attempting reshuffle. Player must pass if unable to play."


        card_drawn = self.deck.deal()
        if card_drawn:
            player.add_card_to_hand(card_drawn)
            return card_drawn, f"{player.name} drew {card_drawn}."
        
        # This case should be rare if reshuffling logic is correct
        return None, "Deck is unexpectedly empty after attempting to draw." 


    def next_turn(self):
        if not self.game_over:
            self.current_player_index = (self.current_player_index + 1) % len(self.players)
            # active_suit is managed by play_card. It persists if an 8 was played.
            # It's updated by a non-8 play. It's not changed by drawing a card.
            # No specific action for active_suit needed here in next_turn.

    def get_game_state_summary(self):
        player = self.get_current_player()
        top_card = self.get_top_card_discard_pile()
        
        # Determine the "effective" suit for the next play
        effective_suit = self.active_suit
        if top_card and not top_card.is_eight: # If last card wasn't an 8, its suit is the one to match
            effective_suit = top_card.suit

        summary = {
            "current_player_name": player.name,
            "current_player_hand": [str(card) for card in player.hand],
            "top_discard_card": str(top_card) if top_card else "None",
            "effective_suit": effective_suit if effective_suit else (top_card.suit if top_card else "None"),
            "cards_in_stock": len(self.deck),
            "game_over": self.game_over,
            "winner_name": self.winner.name if self.winner else None,
            "all_players_card_counts": {p.name: len(p.hand) for p in self.players}
        }
        return summary
