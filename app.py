import random
import json
import os
from datetime import datetime

# --- Constants ---
MIN_NUMBER = 1
MAX_NUMBER = 100
HIGH_SCORES_FILE = 'high_scores.txt'

# Difficulty settings: (max_attempts, description)
DIFFICULTY_LEVELS = {
    'easy': {'attempts': 10, 'description': 'Easy (10 Tries)'},
    'medium': {'attempts': 7, 'description': 'Medium (7 Tries)'},
    'hard': {'attempts': 5, 'description': 'Hard (5 Tries)'}
}

# --- High Score Management ---

def load_high_scores():
    """Loads high scores from the high_scores.txt file."""
    if not os.path.exists(HIGH_SCORES_FILE):
        return []
    try:
        with open(HIGH_SCORES_FILE, 'r') as f:
            # Each line is a JSON string representing a score entry
            scores = [json.loads(line) for line in f if line.strip()]
        return scores
    except json.JSONDecodeError:
        print(f"Warning: Could not decode high scores from {HIGH_SCORES_FILE}. Starting with empty scores.")
        return []
    except Exception as e:
        print(f"An error occurred while loading high scores: {e}")
        return []

def save_high_score(username, score, difficulty_name, max_attempts):
    """Saves a new high score to the high_scores.txt file."""
    high_scores = load_high_scores()
    new_entry = {
        'username': username,
        'score': score,  # Number of attempts taken
        'difficulty': difficulty_name,
        'max_attempts': max_attempts,
        'date': datetime.now().isoformat()
    }
    high_scores.append(new_entry)

    # Sort scores: fewer attempts are better (lower score), then by date for ties
    # If scores are tied, prefer the one with fewer max_attempts (harder difficulty)
    # If still tied, prefer the more recent one
    high_scores.sort(key=lambda x: (x['score'], x['max_attempts'], datetime.fromisoformat(x['date'])), reverse=False)

    # Keep only top 10 scores
    top_scores = high_scores[:10]

    try:
        with open(HIGH_SCORES_FILE, 'w') as f:
            for entry in top_scores:
                f.write(json.dumps(entry) + '\n')
        print("High score saved!")
    except Exception as e:
        print(f"Error saving high score: {e}")

def display_leaderboard():
    """Displays the current high scores."""
    high_scores = load_high_scores()
    print("\n--- Leaderboard ---")
    if not high_scores:
        print("No high scores yet. Play to get on the board!")
        return

    for i, entry in enumerate(high_scores):
        print(f"{i + 1}. {entry['username']} - Attempts: {entry['score']} ({entry['difficulty']})")
    print("-------------------\n")

# --- Game Logic ---

def get_difficulty_choice():
    """Prompts the user to choose a difficulty level."""
    while True:
        print("\nChoose Difficulty:")
        for key, value in DIFFICULTY_LEVELS.items():
            print(f"  {key.capitalize()} ({value['attempts']} Tries)")
        choice = input("Enter difficulty (Easy/Medium/Hard): ").lower()
        if choice in DIFFICULTY_LEVELS:
            return choice
        else:
            print("Invalid difficulty. Please choose Easy, Medium, or Hard.")

def give_hint(secret_number, attempts_made):
    """Provides a hint based on the secret number."""
    if attempts_made % 3 == 0 and attempts_made > 0: # Hint after every 3 wrong tries
        if secret_number % 2 == 0:
            print("Hint: The number is an EVEN number.")
        else:
            print("Hint: The number is an ODD number.")

def play_game():
    """Main function to play the Guess the Number game."""
    print("Welcome to Guess the Number!")
    print(f"I'm thinking of a number between {MIN_NUMBER} and {MAX_NUMBER}.")

    difficulty_choice = get_difficulty_choice()
    max_attempts = DIFFICULTY_LEVELS[difficulty_choice]['attempts']
    difficulty_description = DIFFICULTY_LEVELS[difficulty_choice]['description']

    secret_number = random.randint(MIN_NUMBER, MAX_NUMBER)
    attempts_left = max_attempts
    attempts_made = 0
    game_won = False

    while attempts_left > 0:
        print(f"\nAttempts left: {attempts_left}")
        try:
            guess = int(input(f"Enter your guess ({MIN_NUMBER}-{MAX_NUMBER}): "))
        except ValueError:
            print("Invalid input. Please enter a whole number.")
            continue

        if not (MIN_NUMBER <= guess <= MAX_NUMBER):
            print(f"Your guess is out of range. Please guess between {MIN_NUMBER} and {MAX_NUMBER}.")
            continue

        attempts_made += 1
        attempts_left -= 1

        if guess == secret_number:
            print(f"Congratulations! You guessed the number {secret_number} in {attempts_made} attempts!")
            game_won = True
            break
        elif guess < secret_number:
            print("Too Low! Try again.")
        else:
            print("Too High! Try again.")

        give_hint(secret_number, attempts_made)

    if not game_won:
        print(f"\nGame Over! You ran out of attempts. The number was {secret_number}.")

    if game_won:
        username = input("Enter your username for the leaderboard: ")
        save_high_score(username, attempts_made, difficulty_description, max_attempts)

    display_leaderboard()

# --- Main Game Loop ---
if __name__ == "__main__":
    while True:
        play_game()
        play_again = input("Do you want to play again? (yes/no): ").lower()
        if play_again != 'yes':
            print("Thanks for playing!")
            break