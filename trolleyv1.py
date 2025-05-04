from tkinter import*

class TrolleyGame (object): 
    def __init__(self, root):
        self.root = root
        self.root.title("A Trolley Problem Game")
        self.root.attributes('-fullscreen', True)
        self.utilitarian_score = 0
        self.deontological_score = 0
        self.time_left = 30
        self.timer_id = None

# Grid to work with
        for i in range(30):  
            self.root.columnconfigure(i, weight=1)
            self.root.rowconfigure(i, weight=1)

# Allow Escape key to exit the fullscreen
        self.root.bind("<Escape>", lambda event: self.root.attributes('-fullscreen', False))

# Store which problem we're on
        self.current_problem = 0

        self.trolley_problems = [
            {
                "description": "The trolley is headed toward five people. You can pull the lever and steer it towards a track with one person. What will you do?",
                "utilitarian_option": "Pull the lever",
                "deontological_option": "Do nothing"
            },
            {
                "description": "The trolley is headed toward five people. You can pull the lever and steer it towards a track with your close friend. What will you do?",
                "utilitarian_option": "Pull the lever",
                "deontological_option": "Do nothing"
            },
            {
                "description": "The trolley is headed toward your entire family. You can pull the lever and steer it towards a track with 5 people. What will you do?",
                "utilitarian_option": "Pull the lever",
                "deontological_option": "Do nothing"
            },
            {
                "description": "The trolley is headed toward 2 doctors. You can pull the lever and steer it towards a track with your only child. What will you do?",
                "utilitarian_option": "Pull the lever",
                "deontological_option": "Do nothing"
            },
            {
                "description": "The trolley is headed toward Jonas Salk (inventor of the Polio vaccine). You can pull the lever and steer it towards a track with a trusted family member. What will you do?",
                "utilitarian_option": "Pull the lever",
                "deontological_option": "Do nothing"
            }
        ]


        self.math_problems = [
            {"question": "12 + 15?", "answer": 27},
            {"question": "8 x 7?", "answer": 56}
        ]

        self.math_frame = Frame(self.root)
        self.setup_math_screen()

        self.start_frame = Frame(self.root)
        self.problem_frame = Frame(self.root)

# Screen Set Up
        self.setup_start_screen()
        self.setup_problem_screen()

        self.show_start_screen()

    def setup_start_screen(self):
        self.start_frame.grid (row=0, column=0, rowspan=20, columnspan=20, sticky="nsew")

        title_label = Label(self.start_frame, text="The Trolley Problem", font=("Helvetica", 36, "bold"))
        title_label.grid(row=2, column=10, columnspan=6, pady=20)

        start_button = Button(self.start_frame, text="Begin the Test", font=("Helvetica", 20),
                              command=self.start_game, bg="#4CAF50", fg="white", padx=20, pady=10)
        start_button.grid(row=8, column=10, columnspan=4, pady=30)

        exit_button = Button(self.start_frame, text="Exit", font=("Helvetica", 16),
                             command=lambda: self.root.attributes('-fullscreen', False))
        exit_button.grid(row=15, column=10, columnspan=2)

    def setup_problem_screen(self):
        self.problem_frame.grid(row=0, column=0, rowspan=20, columnspan=20, sticky="nsew")
        self.problem_frame.grid_remove()  # Hide it first

        for i in range(30):  
            self.problem_frame.columnconfigure(i, weight=1)
            self.problem_frame.rowconfigure(i, weight=1)

        self.timer_label = Label(self.problem_frame, text="Time: 30", font=("Helvetica", 16))
        self.timer_label.grid(row=0, column=28, columnspan=2, pady=10, padx=10, sticky="ne")

        self.problem_label = Label(self.problem_frame, text="", font=("Helvetica", 18), wraplength=900, justify="center", anchor="center")
        self.problem_label.grid(row=3, column=5, columnspan=24, pady=30)

        # Utilitarian button
        self.utilitarian_button = Button(self.problem_frame, text="", font=("Helvetica", 16),
            command=lambda: self.make_choice("utilitarian"),
            bg="#2196F3", fg="white", padx=15, pady=8)
        self.utilitarian_button.grid(row=10, column=9, columnspan=5, pady=20)

        # Deontological button
        self.deontological_button = Button(self.problem_frame, text="", font=("Helvetica", 16),
            command=lambda: self.make_choice("deontological"),
            bg="#FF5722", fg="white", padx=15, pady=8)
        self.deontological_button.grid(row=10, column=16, columnspan=5, pady=20)

        self.utilitarian_button.config(state=DISABLED)
        self.deontological_button.config(state=DISABLED)

        self.challenge_button = Button(self.problem_frame, text="Solve Math Challenge First", font=("Helvetica", 14),
            command=self.show_math_challenge, bg="#FFC107", padx=10, pady=5)
        self.challenge_button.grid(row=8, column=12, columnspan=4, pady=10)

    def show_start_screen(self):
        self.problem_frame.grid_remove()
        self.start_frame.grid()

    def start_game(self):
        self.start_frame.grid_remove()
        self.problem_frame.grid()
        self.load_problem()
        # Restart scores when game restarts
        self.utilitarian_score = 0
        self.deontological_score = 0
        self.current_problem = 0

    def load_problem(self):
        
        if self.current_problem < len(self.trolley_problems):
            problem = self.trolley_problems[self.current_problem]

            self.problem_label.config(text=problem["description"])
            self.utilitarian_button.config(text=problem["utilitarian_option"])
            self.deontological_button.config(text=problem["deontological_option"])

            self.utilitarian_button.config(state=DISABLED)
            self.deontological_button.config(state=DISABLED)
            self.challenge_button.config(state=NORMAL)

            self.start_timer()
        else:
            summary = f"You've completed all dilemmas.\n\nUtilitarian choices: {self.utilitarian_score}\nDeontological choices: {self.deontological_score}"
            if self.utilitarian_score > self.deontological_score:
                summary += "\n\nYou lean utilitarian – you prioritize the greater good over individual rights."
            elif self.deontological_score > self.utilitarian_score:
                summary += "\n\nYou lean deontological – you respect moral duties over outcomes."
            else:
                summary += "\n\nYou're morally balanced – or indecisive!"
            self.problem_label.config(text=summary)
            self.utilitarian_button.grid_remove()
            self.deontological_button.grid_remove()
            self.challenge_button.grid_remove()
            self.timer_label.grid_remove()

    def start_timer(self):
        if self.timer_id is not None:
            self.root.after_cancel(self.timer_id)

        self.time_left = 30
        self.update_timer()

    def update_timer(self):
        self.timer_label.config(text=f"Time: {self.time_left}")
        if self.time_left <= 0:
            self.make_choice("deontological")
        else:
            self.time_left -= 1
            self.timer_id = self.root.after(1000, self.update_timer)

    def make_choice(self, choice):
        if self.timer_id:
            self.root.after_cancel(self.timer_id)

        print(f"Choice made: {choice}")
        if choice == "utilitarian":
            self.utilitarian_score += 1
        else:
            self.deontological_score += 1
        print(f"Utilitarian: {self.utilitarian_score}, Deontological: {self.deontological_score}")
            
        self.current_problem +=1
        self.load_problem()

    def setup_math_screen(self):
        self.math_frame.grid(row=0, column=0, rowspan=30, columnspan=30, sticky="nsew")
        self.math_frame.grid_remove()

        self.math_label = Label(self.math_frame, text="", font=("Helvetica", 20))
        self.math_label.grid(row=2, column=10, columnspan=10, pady=20)

        self.math_entry = Entry(self.math_frame, font=("Helvetica", 18), width=10, justify='center')
        self.math_entry.grid(row=5, column=12, columnspan=6, pady=10)

        self.submit_button = Button(self.math_frame, text="Submit", font=("Helvetica", 16),
            command=self.check_math_answer)
        self.submit_button.grid(row=7, column=12, columnspan=6, pady=10)

        self.math_feedback = Label(self.math_frame, text="", font=("Helvetica", 16), fg="red")
        self.math_feedback.grid(row=9, column=10, columnspan=10)

    def show_math_challenge(self):
        problem = self.math_problems[self.current_problem % len(self.math_problems)]
        self.current_math_answer = problem["answer"]
        self.math_label.config(text=problem["question"])
        self.math_feedback.config(text="")
        self.math_entry.delete(0, END)

        self.problem_frame.grid_remove()
        self.math_frame.grid()

    def check_math_answer(self):
        try:
            entered = int(self.math_entry.get())
            if entered == self.current_math_answer:
                self.math_frame.grid_remove()
                self.problem_frame.grid()
                self.utilitarian_button.config(state=NORMAL)
                self.deontological_button.config(state=NORMAL)
                self.challenge_button.config(state=DISABLED)
            else:
                self.math_feedback.config(text="Incorrect. Try again.")
                self.math_entry.delete(0, END)
        except ValueError:
            self.math_feedback.config(text="Please enter a valid number.")
            self.math_entry.delete(0, END)

if __name__ == "__main__":
    root = Tk()
    game = TrolleyGame(root)

root.mainloop()
