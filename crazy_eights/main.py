from game_logic.game import CrazyEightsGame
from game_logic.cards import Card # For chosen_suit_for_eight

def get_player_names():
    num_players = 0
    while True:
        try:
            num_players_str = input("Enter the number of players (2-6): ")
            num_players = int(num_players_str)
            if 2 <= num_players <= 6:
                break
            else:
                print("Please enter a number between 2 and 6.")
        except ValueError:
            print("Invalid input. Please enter a number.")
    
    player_names = []
    for i in range(num_players):
        while True:
            name = input(f"Enter name for Player {i+1}: ").strip()
            if name:
                player_names.append(name)
                break
            else:
                print("Name cannot be empty.")
    return player_names

def display_game_state(game):
    state = game.get_game_state_summary()
    print("\n" + "="*30)
    print(f"Current Player: {state['current_player_name']}")
    print(f"Top Discard Card: {state['top_discard_card']}")
    print(f"Effective Suit for Play: {state['effective_suit']}")
    print(f"Cards in Stock: {state['cards_in_stock']}")
    
    current_player_obj = game.get_current_player()
    print(f"{current_player_obj.name}'s Hand:")
    for i, card_str in enumerate(state['current_player_hand']):
        print(f"  {i+1}: {card_str}")
    print("="*30 + "\n")

def get_player_action(player_name, hand_size):
    while True:
        action = input(f"{player_name}, choose an action: (P)lay card, (D)raw card: ").strip().upper()
        if action in ['P', 'D']:
            if action == 'P' and hand_size == 0:
                print("Your hand is empty. You must draw or the game should have ended.")
                # This case should ideally be handled by game logic ending turn or game
                continue # Or handle as pass if applicable
            return action
        else:
            print("Invalid action. Enter 'P' to play or 'D' to draw.")

def get_card_to_play(hand_size):
    while True:
        try:
            card_choice_str = input(f"Enter the number of the card you want to play (1-{hand_size}): ")
            card_choice_idx = int(card_choice_str) - 1
            if 0 <= card_choice_idx < hand_size:
                return card_choice_idx
            else:
                print(f"Invalid card number. Please choose between 1 and {hand_size}.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def get_suit_choice_for_eight():
    while True:
        suit_choice = input("You played an Eight! Choose a suit (H)earts, (D)iamonds, (C)lubs, (S)pades: ").strip().upper()
        if suit_choice == 'H': return "Hearts"
        if suit_choice == 'D': return "Diamonds"
        if suit_choice == 'C': return "Clubs"
        if suit_choice == 'S': return "Spades"
        print("Invalid suit choice. Please enter H, D, C, or S.")


def main():
    print("Welcome to Crazy Eights!")
    
    player_names = get_player_names()
    try:
        game = CrazyEightsGame(player_names)
    except ValueError as e:
        print(f"Error starting game: {e}")
        return
    except Exception as e: # Catch other potential errors from game setup
        print(f"An unexpected error occurred during game setup: {e}")
        return

    while not game.game_over:
        current_player = game.get_current_player()
        display_game_state(game)
        
        action = get_player_action(current_player.name, len(current_player.hand))
        
        if action == 'D': # Draw card
            drawn_card, message = game.draw_card_for_player(current_player)
            # The message from draw_card_for_player already states what was drawn or if a pass must occur.
            print(message) 

            # Simplified rule: drawing a card ends the player's turn.
            # If stock was empty and no reshuffle possible, the message would indicate this.
            # The player essentially "passes" if they cannot draw.
            if "must pass" in message or drawn_card is None and "Stock is empty" in message :
                 print(f"{current_player.name} passes their turn.")
            elif drawn_card:
                 # Message already printed "Player drew X"
                 pass # Turn will proceed to next_turn()

            game.next_turn()


        elif action == 'P': # Play card
            if not current_player.hand: 
                print("Your hand is empty. You should draw or pass if unable to draw.")
                game.next_turn() 
                continue

            card_idx_to_play = get_card_to_play(len(current_player.hand))
            card_obj_to_play = current_player.hand[card_idx_to_play] 
            
            chosen_suit = None
            if card_obj_to_play.is_eight:
                chosen_suit = get_suit_choice_for_eight()
            
            played_successfully, message = game.play_card(current_player, card_idx_to_play, chosen_suit_for_eight=chosen_suit)
            
            print(message)
            if played_successfully:
                if game.game_over:
                    break 
                game.next_turn()
            else:
                # Invalid play, player's turn continues. Loop will re-prompt.
                pass 

    if game.winner:
        print(f"\nCongratulations {game.winner.name}! You won the game!")
    else:
        # This might be reached if game_over is set without a winner (e.g. stalemate if stock and all hands exhausted, no valid plays)
        # Or if the loop breaks for other reasons.
        print("\nGame over.")
        if game.get_game_state_summary()['cards_in_stock'] == 0 and \
           all(not any(game.is_valid_play(card) for card in p.hand) for p in game.players):
            print("The game is a draw (stalemate: stock is empty and no player can make a valid move).")


    print("Final card counts:")
    for p_name, count in game.get_game_state_summary()['all_players_card_counts'].items():
        print(f"  {p_name}: {count} cards")

if __name__ == "__main__":
    main()
