from .cards import Card # Assuming Card is in cards.py within the same package

class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []

    def add_card_to_hand(self, card):
        if isinstance(card, Card):
            self.hand.append(card)
        else:
            raise TypeError("Only Card objects can be added to a player's hand.")

    def remove_card_from_hand(self, card_to_remove):
        '''Removes a card from the player's hand.
        Returns the card if found and removed, otherwise None.
        '''
        # Need to be careful if cards are just strings or actual Card objects
        # Assuming card_to_remove will be a Card object or identifiable (e.g. by string representation)
        
        # If card_to_remove is a Card object, try to find and remove it directly
        if isinstance(card_to_remove, Card):
            try:
                self.hand.remove(card_to_remove)
                return card_to_remove
            except ValueError: # Card not in hand
                # Try to find by string representation if direct object match fails
                # This might be necessary if the card object passed is not the exact same instance
                # as the one in hand, but represents the same card.
                for i, card_in_hand in enumerate(self.hand):
                    if str(card_in_hand) == str(card_to_remove):
                        return self.hand.pop(i)
                return None


        # If card_to_remove is a string (e.g., "Ace of Spades")
        elif isinstance(card_to_remove, str):
            for i, card in enumerate(self.hand):
                if str(card) == card_to_remove:
                    return self.hand.pop(i)
            return None
        else:
            raise TypeError("card_to_remove must be a Card object or its string representation.")


    def has_empty_hand(self):
        return len(self.hand) == 0

    def __str__(self):
        if not self.hand:
            return f"{self.name}'s hand is empty."
        hand_str = ", ".join(str(card) for card in self.hand)
        return f"{self.name}'s hand: {hand_str}"

    def __repr__(self):
        return f"Player('{self.name}')"
