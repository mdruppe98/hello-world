import unittest
from ..game_logic.game import CrazyEightsGame
from ..game_logic.cards import Card 
from ..game_logic.player import Player

class TestCrazyEightsGame(unittest.TestCase):
    def setUp(self):
        self.player_names = ["Alice", "Bob"]
        self.game = CrazyEightsGame(self.player_names)
        # Manually set a predictable top card for some tests if needed
        # For example, self.game.discard_pile = [Card("Hearts", "7")]
        # self.game.active_suit = "Hearts" 

    def test_game_initialization(self):
        self.assertEqual(len(self.game.players), 2)
        self.assertEqual(self.game.players[0].name, "Alice")
        self.assertEqual(len(self.game.players[0].hand), CrazyEightsGame.NUM_CARDS_TO_DEAL)
        self.assertEqual(len(self.game.players[1].hand), CrazyEightsGame.NUM_CARDS_TO_DEAL)
        self.assertIsNotNone(self.game.get_top_card_discard_pile())
        self.assertFalse(self.game.get_top_card_discard_pile().is_eight) # Starter shouldn't be an 8
        self.assertEqual(len(self.game.deck), 52 - (2 * CrazyEightsGame.NUM_CARDS_TO_DEAL) - 1)
        self.assertEqual(self.game.active_suit, self.game.get_top_card_discard_pile().suit)


    def test_is_valid_play_match_suit(self):
        top_card = Card("Hearts", "7")
        self.game.discard_pile.append(top_card) # Force top card
        self.game.active_suit = "Hearts"
        
        valid_card = Card("Hearts", "10")
        self.assertTrue(self.game.is_valid_play(valid_card))

    def test_is_valid_play_match_rank(self):
        top_card = Card("Hearts", "7")
        self.game.discard_pile.append(top_card)
        self.game.active_suit = "Hearts"

        valid_card = Card("Clubs", "7")
        self.assertTrue(self.game.is_valid_play(valid_card))

    def test_is_valid_play_eight(self):
        top_card = Card("Hearts", "7")
        self.game.discard_pile.append(top_card)
        self.game.active_suit = "Hearts"
        
        eight_card = Card("Spades", "8")
        self.assertTrue(self.game.is_valid_play(eight_card))

    def test_is_valid_play_eight_on_eight(self):
        # Last card played was an 8, chosen suit was Diamonds
        self.game.discard_pile.append(Card("Clubs", "8")) 
        self.game.active_suit = "Diamonds" # User chose Diamonds

        valid_card_matching_chosen_suit = Card("Diamonds", "5")
        self.assertTrue(self.game.is_valid_play(valid_card_matching_chosen_suit))
        
        another_eight = Card("Hearts", "8")
        self.assertTrue(self.game.is_valid_play(another_eight)) # Can always play an 8

        invalid_card_not_matching_chosen_suit = Card("Spades", "5")
        self.assertFalse(self.game.is_valid_play(invalid_card_not_matching_chosen_suit))


    def test_is_invalid_play(self):
        top_card = Card("Hearts", "7")
        self.game.discard_pile.append(top_card)
        self.game.active_suit = "Hearts"

        invalid_card = Card("Clubs", "10") # Neither suit nor rank matches
        self.assertFalse(self.game.is_valid_play(invalid_card))

    def test_play_card_simple(self):
        player = self.game.get_current_player()
        # Find a playable card in player's hand
        # This setup is a bit fragile as hands are random. 
        # For robust tests, mock the hand or dealing.
        # Here, we'll set the discard pile to match one of the player's cards if possible
        
        # Simplified: give player a known card and set discard pile
        player.hand = [Card("Hearts", "Jack")]
        self.game.discard_pile = [Card("Hearts", "5")] # Top card
        self.game.active_suit = "Hearts"

        success, _ = self.game.play_card(player, 0)
        self.assertTrue(success)
        self.assertEqual(len(player.hand), 0)
        self.assertEqual(str(self.game.get_top_card_discard_pile()), "Jack of Hearts")
        self.assertTrue(self.game.game_over) # Player's hand is empty

    def test_play_eight_card_and_choose_suit(self):
        player = self.game.get_current_player()
        player.hand = [Card("Spades", "8"), Card("Hearts", "2")] # Give player an 8
        
        # Set discard pile to something that makes the 8 playable
        self.game.discard_pile = [Card("Clubs", "7")]
        self.game.active_suit = "Clubs"

        success, message = self.game.play_card(player, 0, chosen_suit_for_eight="Diamonds")
        self.assertTrue(success)
        self.assertEqual(len(player.hand), 1) # One card left
        self.assertEqual(str(self.game.get_top_card_discard_pile()), "8 of Spades")
        self.assertEqual(self.game.active_suit, "Diamonds") # Check chosen suit
        self.assertFalse(self.game.game_over)

    def test_draw_card(self):
        player = self.game.get_current_player()
        initial_hand_size = len(player.hand)
        initial_deck_size = len(self.game.deck)

        drawn_card, _ = self.game.draw_card_for_player(player)
        self.assertIsNotNone(drawn_card)
        self.assertEqual(len(player.hand), initial_hand_size + 1)
        self.assertEqual(len(self.game.deck), initial_deck_size - 1)

    def test_reshuffle_discard_into_deck(self):
        player = self.game.get_current_player()
        # Empty the deck
        self.game.deck.cards = [] 
        self.assertTrue(self.game.deck.is_empty())
        
        # Add some cards to discard pile (more than 1)
        self.game.discard_pile = [Card("Hearts", "2"), Card("Clubs", "3"), Card("Diamonds", "4")]
        top_discard_before_reshuffle = self.game.discard_pile[-1] # Diamonds 4

        drawn_card, _ = self.game.draw_card_for_player(player) # This should trigger reshuffle

        self.assertIsNotNone(drawn_card)
        self.assertEqual(len(player.hand), CrazyEightsGame.NUM_CARDS_TO_DEAL + 1)
        self.assertEqual(str(self.game.get_top_card_discard_pile()), str(top_discard_before_reshuffle)) # Top card should remain
        self.assertEqual(len(self.game.deck.cards), 2 - 1) # (3 cards in discard - 1 top card) - 1 drawn card = 1


    def test_next_turn(self):
        initial_player_index = self.game.current_player_index
        self.game.next_turn()
        expected_player_index = (initial_player_index + 1) % len(self.game.players)
        self.assertEqual(self.game.current_player_index, expected_player_index)

if __name__ == '__main__':
    unittest.main()
