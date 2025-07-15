import random

MIN_NUMBER = 1
MAX_NUMBER = 100


DIFFICULTY_LEVELS = {
    'easy': {'attempts': 10, 'description': 'Easy (10 Tries)'},
    'medium': {'attempts': 7, 'description': 'Medium (7 Tries)'},
    'hard': {'attempts': 5, 'description': 'Hard (5 Tries)'}
}

def get_difficulty_choice():

    while True:
        print("Choose Difficulty:")

        for key, value in DIFFICULTY_LEVELS.items():
            print(f" {key.capitalize()} ({value['attempts']} Tries)")

        choice = input("Enter difficulty (Easy/Medium/Hard:)").lower()

        if choice in DIFFICULTY_LEVELS:
            return choice
        else:
             print("Invalid difficulty. Please choose Easy, Medium, or Hard.")

def give_hint(secret_number, attempts_made):
    if attempts_made % 3 == 0 and attempts_made > 0:
        if secret_number % 2 == 0:
            print("Hint: The number is an EVEN number.")
        else:
            print("Hint: The number is an ODD number.")


def play_game():

    print("Welcome to Guess the Number game.")
    print(f"I'm thinking of a number between {MIN_NUMBER} and {MAX_NUMBER}")

    difficulty_choice = get_difficulty_choice()
    max_attempts = DIFFICULTY_LEVELS[difficulty_choice]['attempts']
    difficulty_description = DIFFICULTY_LEVELS[difficulty_choice]['description']

    secret_number = random.randint(MIN_NUMBER, MAX_NUMBER)
    attempts_made = 0
    attempts_left = max_attempts
    game_won = True

    while attempts_left > 0:
        print(f"Attempts left: {attempts_left}")
        try:
            guess = int(input(f"Enter your guess ({MIN_NUMBER} - {MAX_NUMBER}):"))
        except ValueError:
            print("Invalid input. Please enter a whole number.")
            continue

        if not (MIN_NUMBER <= guess <= MAX_NUMBER):
            print(f"Your guess is out of range. Please guess a number between {MIN_NUMBER} and {MAX_NUMBER}")
            continue

        attempts_made += 1
        attempts_left -= 1

        if guess == secret_number:
            print(f"Congratulations! You guessed the number {secret_number} in {attempts_made} attempts!")
            break
        elif guess < secret_number:
            print("Too low. Try again")
        else:
            print("Too high. Try again")

        if guess != secret_number:
            give_hint(secret_number, attempts_made)

    if not game_won:
        print(f"Game Over! You ran out of attempts. The number was {secret_number}.")

if __name__ == "__main__":
    play_game()




