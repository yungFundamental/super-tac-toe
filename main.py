import game


def main():
    print("Hello! welcome to Ultimate TicTacToe!")

    proceed = 1
    while proceed:
        proceed = game.game()
    print("\n\nSee you next time!")


if __name__ == "__main__":
    main()
