from tkinter import*

class TrolleyGame (object): 
    def __init__(self, root):
        self.root = root
        self.root.title("A Trolley Problem Game")
        self.root.attributes('-fullscreen', True)

        for i in range(20):  
            root.columnconfigure(i, weight=1)
            root.rowconfigure(i, weight=1)
        # Allow Escape key to exit fullscreen
        self.root.bind("<Escape>", lambda event: self.root.attributes('-fullscreen', False))

        self.start_frame = Frame(self.root)
        self.problem_frame = Frame(self.root)

        self.setup_start_screen()
        self.setup_problem_screen()

        self.show_start_screen()

    def setup_start_screen(self):
        self.start_frame.grid (row=0, column=0, rowspan=20, columnspan=20, sticky="nsew")

        title_label = Label(self.start_frame, text="The Trolley Problem", font=("Helvetica", 36, "bold"))
        title_label.grid(row=2, column=7, columnspan=6, pady=20)

        start_button = Button(self.start_frame, text="Begin the Test", font=("Helvetica", 20),
                              command=self.start_game, bg="#4CAF50", fg="white", padx=20, pady=10)
        start_button.grid(row=8, column=8, columnspan=4, pady=30)

        exit_button = Button(self.start_frame, text="Exit", font=("Helvetica", 16),
                             command=lambda: self.root.attributes('-fullscreen', False))
        exit_button.grid(row=15, column=9, columnspan=2)

    def setup_problem_screen(self):
        self.problem_frame.grid(row=0, column=0, rowspan=20, columnspan=20, sticky="nsew")
        self.problem_frame.grid_remove()  # Hide it at first

        self.problem_label = Label(self.problem_frame, text="Problem will go here.", font=("Helvetica", 18))
        self.problem_label.grid(row=3, column=3, columnspan=14, pady=30)

    def show_start_screen(self):
        self.problem_frame.grid_remove()
        self.start_frame.grid()

    def start_game(self):
        self.start_frame.grid_remove()
        self.problem_frame.grid()
        self.problem_label.config(text="This will be your first trolley dilemma!")

if __name__ == "__main__":
    root = Tk()
    game = TrolleyGame(root)

root.mainloop()
