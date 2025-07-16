import random
import os

MIN_NUMBER = 1
MAX_NUMBER = 100
HIGHSCORE_FILE = "highscores.txt"

DIFFICULTY_LEVELS = {
    'easy': {'attempts': 10, 'description': 'Easy (10 Tries)'},
    'medium': {'attempts': 7, 'description': 'Medium (7 Tries)'},
    'hard': {'attempts': 5, 'description': 'Hard (5 Tries)'}
}

def get_difficulty_choice():
    """Prompts the user to choose a difficulty level."""
    while True:
        print("\nChoose Difficulty:")
        for key, value in DIFFICULTY_LEVELS.items():
            print(f" {key.capitalize()} ({value['attempts']} Tries)")
        choice = input("Enter difficulty (Easy/Medium/Hard): ").lower()
        if choice in DIFFICULTY_LEVELS:
            return choice
        else:
            print("Invalid difficulty. Please choose Easy, Medium, or Hard.")

def give_hint(secret_number, attempts_made, guess):
    """Provides hints based on attempts made and guess proximity."""
    if attempts_made % 3 == 0 and attempts_made > 0:
        print("Hint:")
        if secret_number % 2 == 0:
            print("  The number is an EVEN number.")
        else:
            print("  The number is an ODD number.")

        
        if attempts_made % 5 == 0: 
            if secret_number % 3 == 0:
                print("  The number is divisible by 3.")
            else:
               
                if abs(secret_number % 10) <= 2 or abs(secret_number % 10 - 10) <= 2:
                    print(f"  The number is close to a multiple of 10 (e.g., {round(secret_number / 10) * 10}).")
                elif secret_number < guess:
                    print("  Consider guessing a bit lower next time.")
                else:
                    print("  Consider guessing a bit higher next time.")


def save_highscore(username, score):
    """Saves the player's username and score to the highscore file."""
    try:
        with open(HIGHSCORE_FILE, 'a') as f:
            f.write(f"{username},{score}\n")
    except IOError:
        print("Error: Could not save high score.")

def load_highscores():
    """Loads high scores from the file and returns them as a sorted list."""
    highscores = []
    if not os.path.exists(HIGHSCORE_FILE):
        return highscores
    try:
        with open(HIGHSCORE_FILE, 'r') as f:
            for line in f:
                try:
                    username, score_str = line.strip().split(',')
                    highscores.append({'username': username, 'score': int(score_str)})
                except ValueError:
                    continue 
    except IOError:
        print("Error: Could not load high scores.")
    
    
    highscores.sort(key=lambda x: x['score'])
    return highscores

def display_leaderboard(highscores):
    """Displays the top high scores."""
    print("\n--- Leaderboard ---")
    if not highscores:
        print("No high scores yet. Be the first to set one!")
        return

    for i, entry in enumerate(highscores[:10]): 
        print(f"{i+1}. {entry['username']} - {entry['score']} attempts")
    print("-------------------")


def play_game():
    """Main function to play the Guess the Number game."""
    print("Welcome to Guess the Number game.")
    display_leaderboard(load_highscores())
    print(f"I'm thinking of a number between {MIN_NUMBER} and {MAX_NUMBER}")

    difficulty_choice = get_difficulty_choice()
    max_attempts = DIFFICULTY_LEVELS[difficulty_choice]['attempts']
    difficulty_description = DIFFICULTY_LEVELS[difficulty_choice]['description']

    secret_number = random.randint(MIN_NUMBER, MAX_NUMBER)
    attempts_made = 0
    attempts_left = max_attempts
    game_won = False 

    while attempts_left > 0:
        print(f"\nAttempts left: {attempts_left} ({difficulty_description})")
        try:
            guess = int(input(f"Enter your guess ({MIN_NUMBER} - {MAX_NUMBER}): "))
        except ValueError:
            print("Invalid input. Please enter a whole number.")
            continue

        if not (MIN_NUMBER <= guess <= MAX_NUMBER):
            print(f"Your guess is out of range. Please guess a number between {MIN_NUMBER} and {MAX_NUMBER}.")
            continue

        attempts_made += 1
        attempts_left -= 1

        if guess == secret_number:
            print(f"\nCongratulations! You guessed the number {secret_number} in {attempts_made} attempts!")
            game_won = True 
            username = input("Enter your username for the high score: ")
            save_highscore(username, attempts_made)
            display_leaderboard(load_highscores()) 
            break
        elif guess < secret_number:
            print("Too low. Try again.")
        else:
            print("Too high. Try again.")

        if guess != secret_number: 
            give_hint(secret_number, attempts_made, guess)

    if not game_won:
        print(f"\nGame Over! You ran out of attempts. The number was {secret_number}.")

if __name__ == "__main__":
    play_game() 




