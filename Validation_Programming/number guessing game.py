import random

computer_choice = random.randint(1, 100)

print("Which number is in my mind? make sure you choose a number between 1 and 100")

while True:
    try:
        player_choice = int(input())
        if player_choice >= 1 and player_choice <= 100:
            if player_choice == computer_choice:
                print(f"You Win! The number is {computer_choice} and you guessed it correctly!")
                break
            elif player_choice < computer_choice:
                print("The number that i want you to guess is greater than this number, try again!")
            else:
                print("The number that i want you to guess is less than this number, try again!")
        else:
            print("Choose a number between 1 and 100 please!")
    except ValueError:
        print("Invalid input, Choose a number between 1 and 100 please!")