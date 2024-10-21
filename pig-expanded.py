import random
import time
import argparse

class Die:
    def __init__(self, sides=6):
        self.sides = sides
    
    def roll(self):
        return random.randint(1, self.sides)

class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0

    def make_decision(self, turn_total):
        raise NotImplementedError("This method should be overridden by subclasses.")

    def __str__(self):
        return f"{self.name} (Score: {self.score})"

class HumanPlayer(Player):
    def make_decision(self, turn_total):
        while True:
            decision = input(f"{self.name}, do you want to 'roll' (r) or 'hold' (h)? ").strip().lower()
            if decision in ['r', 'h']:
                return decision
            print("Invalid input. Please enter 'r' to roll or 'h' to hold.")

class ComputerPlayer(Player):
    def make_decision(self, turn_total):
        # Strategy: hold if turn_total >= min(25, 100 - score), otherwise roll
        if turn_total >= min(25, 100 - self.score):
            print(f"{self.name} decides to hold.")
            return 'h'
        else:
            print(f"{self.name} decides to roll.")
            return 'r'

class PlayerFactory:
    @staticmethod
    def create_player(player_type, name):
        if player_type.lower() == 'human':
            return HumanPlayer(name)
        elif player_type.lower() == 'computer':
            return ComputerPlayer(name)
        else:
            raise ValueError("Invalid player type. Must be 'human' or 'computer'.")

class PigGame:
    def __init__(self, player1, player2, winning_score=100):
        self.die = Die()
        self.players = [player1, player2]
        self.current_player_index = 0
        self.winning_score = winning_score
        self.turn_total = 0

    def switch_player(self):
        self.current_player_index = 1 - self.current_player_index
        self.turn_total = 0

    def roll_die(self):
        roll = self.die.roll()
        print(f"{self.get_current_player().name} rolled a {roll}")
        if roll == 1:
            print(f"Rolled a 1! No points added. Switching to the other player.")
            self.switch_player()
        else:
            self.turn_total += roll
            print(f"Turn total is now {self.turn_total}")

    def hold(self):
        player = self.get_current_player()
        player.score += self.turn_total
        print(f"{player.name} holds. Total score is now {player.score}")
        self.switch_player()

    def get_current_player(self):
        return self.players[self.current_player_index]

    def play_turn(self):
        player = self.get_current_player()
        print(f"\n{player.name}'s turn:")
        print(f"Total score: {player.score}")

        while True:
            decision = player.make_decision(self.turn_total)
            if decision == 'r':
                self.roll_die()
                if self.turn_total == 0:  # Switch happens if a 1 is rolled
                    break
            elif decision == 'h':
                self.hold()
                break

    def check_winner(self):
        for player in self.players:
            if player.score >= self.winning_score:
                return player
        return None

    def start_game(self):
        print("Welcome to the Pig game!")
        while True:
            self.play_turn()
            winner = self.check_winner()
            if winner:
                print(f"Congratulations, {winner.name}! You have won the game with {winner.score} points!")
                break

class TimedPigGame:
    def __init__(self, player1, player2, winning_score=100, time_limit=60):
        self.game = PigGame(player1, player2, winning_score)
        self.time_limit = time_limit

    def start_game(self):
        print("Welcome to the Timed Pig game!")
        start_time = time.time()

        while True:
            self.game.play_turn()
            if time.time() - start_time >= self.time_limit:
                print("Time's up!")
                winner = max(self.game.players, key=lambda p: p.score)
                print(f"Congratulations, {winner.name}! You have won the game with {winner.score} points!")
                break

            winner = self.game.check_winner()
            if winner:
                print(f"Congratulations, {winner.name}! You have won the game with {winner.score} points!")
                break

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Play the Pig game against a human or computer.")
    parser.add_argument("--player1", choices=["human", "computer"], required=True, help="Type of player 1 (human or computer)")
    parser.add_argument("--player2", choices=["human", "computer"], required=True, help="Type of player 2 (human or computer)")
    parser.add_argument("--timed", action='store_true', help="Play a timed version of the game")
    
    args = parser.parse_args()

    # Create players using the PlayerFactory
    player1 = PlayerFactory.create_player(args.player1, "Player 1")
    player2 = PlayerFactory.create_player(args.player2, "Player 2")

    # Start the appropriate game
    if args.timed:
        game = TimedPigGame(player1, player2)
    else:
        game = PigGame(player1, player2)

    game.start_game()
