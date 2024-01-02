"""
COMP.CS.100
Week 13, the 5th project of the course.
title: Hangman game with virtual keyboard.

(This is a simple Hangman game with virtual keyboard. The code set a random word
from the list;WORD. The user should try to guess its letters by pressing the
virtual keyboard buttons. By each incorrect guess, the image of the Hangman gets
one step closer to completion. After 7 steps/ 7 incorrect guesses the Hangman
completes and the user loses the game. The user can reset the game by pressing
"Reset" button at any stage. He/she can quit the game by pressing "Quit" button.)

Creator: Maral Nourimand
"""

from tkinter import *
import random


WORDS = ["test", "python", "word", "whatever", "Tampere"]
LETTERS = ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P",
           "A", "S", "D", "F", "G", "H", "J", "K", "L",
           "Z", "X", "C", "V", "B", "N", "M"]


class Hangman:
    """
    This a GUI class which displays the Hangman game.
    """
    def __init__(self):
        """
        Constructor
        """
        self.__main_window = Tk()
        self.__main_window.title("Hangman Game")

        # Variables to store game state
        self.__word = ""
        self.__guesses = set()
        self.__remaining_attempts = 7

        # Image variables
        # we have 7 steps and for each step we have one PNG image.
        # So we create a list of 7 PNG images in this class.
        self.__image_steps = []
        for i in range(0, 8):
            image = PhotoImage(file=f"STEP_0{i}.png")
            self.__image_steps.append(image)

        # to create labels and Entry
        self.__lbl_welcome = Label(self.__main_window,
                                   text="Let's guess the word!")

        self.__lbl_instruct = Label(self.__main_window,
                                    text="Press any letter on the keyboard!")

        self.__lbl_word = Label(self.__main_window, text=" ")
        self.__lbl_attempts = Label(self.__main_window, text="Attempts left: 7")
        self.__entry_guess = Entry(self.__main_window, width=30)
        self.__lbl_image = Label(self.__main_window, image=self.__image_steps[0])
        self.__btn_new_game = Button(self.__main_window, text="Reset",
                                     command=self.new_game, background="yellow")
        self.__btn_quit_game = Button(self.__main_window, text="Quit",
                                      command=self.quit, background="orange")

        # Position the GUI elements
        self.__lbl_welcome.grid(row=0, column=0, columnspan=5)
        self.__lbl_instruct.grid(row=1, column=0, columnspan=5)
        self.__lbl_word.grid(row=2, column=0, columnspan=6, padx=10, pady=10)
        self.__lbl_attempts.grid(row=3, column=0, columnspan=6, padx=10, pady=5)
        self.__entry_guess.grid(row=4, column=0, columnspan=6, padx=10, pady=5)
        self.__lbl_image.grid(row=1, column=6, rowspan=3, columnspan=3)
        self.__btn_new_game.grid(row=4, column=5)
        self.__btn_quit_game.grid(row=4, column=6)

        # Creating buttons for each character of the virtual keyboard.
        row, col = 5, 0
        for letter in LETTERS:
            Button(self.__main_window, text=letter, width=10,
                   command=lambda c=letter: self.keypress(c)).grid(row=row,
                                                                   column=col)
            col += 1
            if col > 9 or letter == "L":
                col = 0
                row += 1

        # to start the game
        self.new_game()
        self.__main_window.mainloop()

    def new_game(self):
        """
        This method starts a new game. It resets the previous game, set a new
        random word to guess, clears up the Hangman image, sets the remaining
        attempts to 7 and starts receiving keyboard inputs.
        """
        # Choose a random word to guess
        self.__word = random.choice(WORDS).upper()

        # Reset game state
        self.__guesses = set()
        self.__remaining_attempts = 7

        # Update labels
        self.update_word_label()
        self.update_image()
        self.__lbl_attempts.config(
            text=f"Attempts left: {self.__remaining_attempts}")

    def keypress(self, char):
        """
        This method handles the keyboard input, i.e. what buttons are pressed by
        the user to guess the word. It also checks whether the user has won or
        not.

        :param char: str, the key of the keyboard which is pressed.
        """
        # Check if the guessed letter is in the word to guess
        char = char.upper()
        if char in self.__word:
            self.__guesses.add(char)
        else:
            self.__remaining_attempts -= 1
            self.update_image()

        # Update the word label and check if the game is won or lost
        self.update_word_label()
        self.__lbl_attempts.config(
            text=f"Attempts left: {self.__remaining_attempts}")

        if self.__remaining_attempts == 0:
            self.__lbl_word.config(
                text="You lost! The word was " + self.__word, background="red")

        elif all(char in self.__guesses for char in self.__word):
            self.__lbl_word.config(
                text="Congratulations! You guessed the word.", background="green")

        # Clear the entry field
        self.__entry_guess.delete(0, 'end')

    def update_word_label(self):
        """
        This method updates the word label. If any letter is guessed correctly,
        it prints the letter in the correct position and prints underscores
        for unknown letters.
        """
        # Display the word to guess with underscores for unknown letters
        word_display = " ".join(
            char if char in self.__guesses else "_" for char in self.__word)
        self.__lbl_word.config(text=word_display, background="white")

    def update_image(self):
        """
        This method updates the Hangman image if the user guesses wrongly.
        It completes the image step by step.
        """
        self.__lbl_image.configure(
            image=self.__image_steps[7 - self.__remaining_attempts])

    def quit(self):
        """
        This method ends the game and closes the window.
        """
        self.__main_window.destroy()


def main():
        game = Hangman()


if __name__ == "__main__":
    main()
