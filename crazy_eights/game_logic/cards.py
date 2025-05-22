import random

class Card:
    SUITS = ["Hearts", "Diamonds", "Clubs", "Spades"]
    RANKS = ["2", "3", "4", "5", "6", "7", "9", "10", "Jack", "Queen", "King", "Ace"] # Note: "8" is handled separately as wild

    def __init__(self, suit, rank):
        if suit not in self.SUITS:
            raise ValueError(f"Invalid suit: {suit}")
        if rank not in self.RANKS and rank != "8": # Allow "8" for wild cards
            raise ValueError(f"Invalid rank: {rank}")
        self.suit = suit
        self.rank = rank
        self.is_eight = (rank == "8")

    def __str__(self):
        return f"{self.rank} of {self.suit}"

    def __repr__(self):
        return f"Card('{self.suit}', '{self.rank}')"

class Deck:
    def __init__(self):
        self.cards = self._generate_deck()
        self.shuffle()

    def _generate_deck(self):
        deck = []
        for suit in Card.SUITS:
            for rank in Card.RANKS:
                deck.append(Card(suit, rank))
            # Add the four 8s
            deck.append(Card(suit, "8"))
        return deck

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self):
        if not self.is_empty():
            return self.cards.pop()
        return None # Or raise an error

    def is_empty(self):
        return len(self.cards) == 0

    def __len__(self):
        return len(self.cards)
