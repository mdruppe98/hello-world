import unittest
from ..game_logic.cards import Card, Deck # Adjusted import for running tests from root

class TestCard(unittest.TestCase):
    def test_card_creation(self):
        card = Card("Hearts", "Ace")
        self.assertEqual(card.suit, "Hearts")
        self.assertEqual(card.rank, "Ace")
        self.assertFalse(card.is_eight)
        self.assertEqual(str(card), "Ace of Hearts")

    def test_eight_card(self):
        card = Card("Clubs", "8")
        self.assertTrue(card.is_eight)
        self.assertEqual(str(card), "8 of Clubs")

    def test_invalid_suit(self):
        with self.assertRaises(ValueError):
            Card("Moons", "7")

    def test_invalid_rank(self):
        with self.assertRaises(ValueError):
            Card("Spades", "1") # Rank "1" is not defined, "Ace" is

class TestDeck(unittest.TestCase):
    def setUp(self):
        self.deck = Deck()

    def test_deck_creation(self):
        self.assertEqual(len(self.deck.cards), 52)
        # Check for unique cards
        self.assertEqual(len(set(str(card) for card in self.deck.cards)), 52)

    def test_deck_shuffle(self):
        deck1_order = [str(card) for card in self.deck.cards]
        self.deck.shuffle()
        deck2_order = [str(card) for card in self.deck.cards]
        self.assertNotEqual(deck1_order, deck2_order, "Deck shuffle should change card order (highly probable)")
        self.assertEqual(len(self.deck.cards), 52) # Ensure shuffle doesn't change card count

    def test_deck_deal(self):
        top_card = self.deck.cards[-1] # Expected card to be dealt
        dealt_card = self.deck.deal()
        self.assertEqual(str(dealt_card), str(top_card))
        self.assertEqual(len(self.deck.cards), 51)

    def test_deal_empty_deck(self):
        deck = Deck()
        for _ in range(52):
            deck.deal()
        self.assertTrue(deck.is_empty())
        self.assertIsNone(deck.deal())

    def test_deck_len(self):
        self.assertEqual(len(self.deck), 52)
        self.deck.deal()
        self.assertEqual(len(self.deck), 51)

if __name__ == '__main__':
    unittest.main()
