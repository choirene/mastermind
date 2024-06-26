import requests
import json
import os
from dotenv import load_dotenv
from number import Number

load_dotenv()

def generate_random_integers(api_key, num, min_val, max_val, replacement):
    url = 'https://api.random.org/json-rpc/4/invoke'
    headers = {'content-type': 'application/json'}

    params = {
        "jsonrpc": "2.0",
        "method": "generateIntegers",
        "params": {
            "apiKey": api_key,
            "n": num,
            "min": min_val,
            "max": max_val,
            "base": 10,
        },
        "id": 42,
        "replacement": replacement,
    }

    response = requests.post(url, data=json.dumps(params), headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        if 'error' in result:
            print("Error:", result['error']['message'])
        else:
            return result['result']['random']['data']
    else:
        print("Failed to connect. Status code:", response.status_code)

def game_setup():
    print("Welcome to mastermind! Please try guessing the 4 digit number.")
    api_key = os.getenv("API_KEY")
    if api_key is None:
        print("API key not found. Please set it in the .env file.")
    else:
        num = 4  # Number of random integers to generate
        min_val = 0  # Minimum value of the random integers
        max_val = 7  # Maximum value of the random integers
        replacement = True # True = lets nums repeat. False = nums will not repeat

        solution = Number(num_list=generate_random_integers(api_key, num, min_val, max_val, replacement))
        player_turn(solution, 0)

def player_turn(solution, guesses, max_guesses=10):
    player_guess = input("Guess a number \n")

    while not ((len(player_guess) == 4) and (player_guess.isnumeric())):
        player_guess = input("Guess a valid 4 digit number. \n")
    
    player_guess = Number(string_num=player_guess)

    if player_guess.string_num == solution.string_num:
        game_end(True)
    elif guesses == max_guesses:
        print(f"The number was {solution.string_num}")
        game_end(False)
    else:
        (correct_nums, correct_places) = judge_guess(solution, player_guess)

        format_output = lambda num: f"{num} number" if num == 1 else f"{num} numbers"

        print(f"You have guessed {format_output(correct_nums)} correctly. You have {format_output(correct_places)} in the correct place.")
        guesses += 1
        print(f"{max_guesses-guesses} guesses remaining.")
        print("~~~~~~")
        player_turn(solution, guesses)

def judge_guess(solution, player_guess):
    correct_nums = 0
    correct_places = 0
    index = 0
    
    for num in player_guess.num_list:
        if num in solution.freq_dict:
            if player_guess.freq_dict[num] > solution.freq_dict[num]:
                correct_nums += (solution.freq_dict[num] / player_guess.freq_dict[num])
            else:
                correct_nums += 1

            if solution.num_list[index] == player_guess.num_list[index]:
                correct_places += 1
        index += 1
    return(int(correct_nums), correct_places)

def game_end(player_win):
    if player_win:
        print("Congrats!")
    else: 
        print("Better luck next time.")
    play_again = input("Want to play again?")
    if play_again == "Y":
        game_setup()
    else:
        print("Thanks for playing!")

game_setup()