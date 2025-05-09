from tkinter import *

#2:30-4:30am May 8, 2025 Olivia
#working on track tracking/flowchart user choices affecting the final score bar
#will do a second pass b/c it's not continuous gameplay yet

class TrackNode: #each node represents each trolley problem presented to the user
    def __init__(self, left_group, right_group, reward_type, red_path=False):
        self.left = left_group #the "left" track with some set group of people on it
        self.right = right_group #the "right" track with some set group of people on it 
        self.reward = reward_type  # classifies which choice is "utilitarian" or "deontological"
        self.red_path = red_path #if the path is particularly morally challenging/illogical
        #add self.danger_path = danger_path #choices that identify psycho edge cases??

class TrolleyGame(object): 
    def __init__(self, root):
        self.root = root
        self.root.title("A Trolley Problem Game")
        self.root.attributes('-fullscreen', True)

        # scoring system 
        self.utilitarian_score = 0
        self.deontological_score = 0
        self.conflicted_score = 0 # i added this, 0 is baseline conflicted human

        # track system variables
        self.current_track = "left"  # start on left track
        self.previous_track = None

        # timer variables
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

        # Define track nodes with the trolley problems
        # this flow needs a lot of work...because the philosophical classification of each scenerio depends 
        # on which track they're currently on and their past choices
        self.track_nodes = [
            TrackNode("5 people", "1 person", "utilitarian"),
            TrackNode("a family member", "5 people", "deontological", red_path=True),
            TrackNode("5 of your closest friends", "a baby", "deontological"),
            TrackNode("2 brilliant doctors", "another family member", "deontological", red_path=True),
            TrackNode("5 preschoolers", "an active shooter", "deontological", red_path=True),
            TrackNode("nothing", "a bomb (will stop the train but kill everyone inside it)", "deontological"),
            TrackNode("an assassin with a 75%% chance of killing you and a couple innocent bystanders", "nothing", "deontological"), 
            #wanna add a spin the wheel thing or roll the dice thing here
            TrackNode("you, your partner, and your child", "10 doctors, 10 soldiers, 10 engineers, and 1 infant", "deontological", red_path=True),

        ]

        self.math_problems = [
            {"question": "12 + 15?", "answer": 27},
            {"question": "8 x 7?", "answer": 56}
        ]

        # Create all frames
        self.start_frame = Frame(self.root)
        self.problem_frame = Frame(self.root)
        self.math_frame = Frame(self.root)
        self.result_frame = Frame(self.root)

        # Setup all screens
        self.setup_start_screen()
        self.setup_problem_screen()
        self.setup_math_screen()
        self.setup_result_screen()

        self.show_start_screen()

    def setup_start_screen(self):
        for i in range(30):  
            self.start_frame.columnconfigure(i, weight=1)
            self.start_frame.rowconfigure(i, weight=1)

        self.start_frame.grid(row=0, column=0, rowspan=30, columnspan=30, sticky="nsew")

        # Centered title
        title_label = Label(self.start_frame, text="The Trolley Problem", font=("Helvetica", 36, "bold"))
        title_label.grid(row=6, column=5, columnspan=20, pady=20)

        # Centered start button
        start_button = Button(self.start_frame, text="Begin the Test", font=("Helvetica", 20),
            command=self.start_game, bg="#4CAF50", fg="white", padx=20, pady=10)
        start_button.grid(row=10, column=10, columnspan=10, pady=28)

        # Centered exit button
        exit_button = Button(self.start_frame, text="Exit", font=("Helvetica", 16),
            command=lambda: self.root.attributes('-fullscreen', False))
        exit_button.grid(row=15, column=13, columnspan=4)

    def setup_problem_screen(self):
        self.problem_frame.grid(row=0, column=0, rowspan=30, columnspan=30, sticky="nsew")
        self.problem_frame.grid_remove()  # Hide it first

        for i in range(30):  
            self.problem_frame.columnconfigure(i, weight=1)
            self.problem_frame.rowconfigure(i, weight=1)

        # Timer in top right
        self.timer_label = Label(self.problem_frame, text="Time: 30", font=("Helvetica", 16))
        self.timer_label.grid(row=1, column=28, columnspan=2, pady=10, padx=10, sticky="ne")

        # Centered problem description
        self.problem_label = Label(self.problem_frame, text="", font=("Helvetica", 18), 
                             wraplength=900, justify="center")
        self.problem_label.grid(row=5, column=5, columnspan=20, pady=30)

         # Track status indicator
        self.track_status = Label(self.problem_frame, text="", font=("Helvetica", 16, "italic"),
                                 fg="#666666")
        self.track_status.grid(row=7, column=5, columnspan=20)

        # Centered challenge button
        self.challenge_button = Button(self.problem_frame, text="Solve Math Challenge First", 
                                 font=("Helvetica", 14), command=self.show_math_challenge, 
                                 bg="#FFC107", padx=10, pady=5)
        self.challenge_button.grid(row=10, column=10, columnspan=10, pady=10)

       # Centered choice buttons
        self.switch_button = Button(self.problem_frame, text="Switch Tracks", font=("Helvetica", 16),
            command=lambda: self.make_choice(True),
            bg="#2196F3", fg="white", padx=15, pady=8)
        self.switch_button.grid(row=15, column=7, columnspan=6, pady=20)

        self.stay_button = Button(self.problem_frame, text="Stay on Track", font=("Helvetica", 16),
            command=lambda: self.make_choice(False),
            bg="#FF5722", fg="white", padx=15, pady=8)
        self.stay_button.grid(row=15, column=17, columnspan=6, pady=20)

        self.switch_button.config(state=DISABLED)
        self.stay_button.config(state=DISABLED)

    def setup_math_screen(self):
        self.math_frame.grid(row=0, column=0, rowspan=30, columnspan=30, sticky="nsew")
        self.math_frame.grid_remove()

        for i in range(30):  
            self.math_frame.columnconfigure(i, weight=1)
            self.math_frame.rowconfigure(i, weight=1)

        # Centered math challenge elements
        self.math_label = Label(self.math_frame, text="", font=("Helvetica", 24))
        self.math_label.grid(row=5, column=10, columnspan=10, pady=20)

        self.math_entry = Entry(self.math_frame, font=("Helvetica", 18), width=10, justify='center')
        self.math_entry.grid(row=10, column=12, columnspan=6, pady=10)

        self.submit_button = Button(self.math_frame, text="Submit", font=("Helvetica", 16),
            command=self.check_math_answer)
        self.submit_button.grid(row=15, column=12, columnspan=6, pady=10)

        self.math_feedback = Label(self.math_frame, text="", font=("Helvetica", 16), fg="red")
        self.math_feedback.grid(row=20, column=10, columnspan=10)

    def setup_result_screen(self):
        self.result_frame.grid(row=0, column=0, rowspan=30, columnspan=30, sticky="nsew")
        self.result_frame.grid_remove()

        for i in range(30):  
            self.result_frame.columnconfigure(i, weight=1)
            self.result_frame.rowconfigure(i, weight=1)

        self.result_label = Label(self.result_frame, text="", font=("Helvetica", 18), wraplength=900, justify="center")
        self.result_label.grid(row=5, column=5, columnspan=20, pady=30)

        self.progress_label = Label(self.result_frame, text="Your Moral Leaning", font=("Helvetica", 14))
        self.progress_label.grid(row=10, column=10, columnspan=10)

        self.progress_canvas = Canvas(self.result_frame, width=400, height=30, bg="white", highlightthickness=1, highlightbackground="black")
        self.progress_canvas.grid(row=11, column=10, columnspan=10, pady=20)


        # Add track history 
        self.track_history_label = Label(self.result_frame, text="Track Paths Taken:", font=("Helvetica", 14))
        self.track_history_label.grid(row=12, column=10, columnspan=10, pady=(20, 5))
        
        self.track_history_text = Text(self.result_frame, height=8, width=60, font=("Helvetica", 12))
        self.track_history_text.grid(row=13, column=10, columnspan=10)


        # Restart Button
        restart_button = Button(self.result_frame, text="Play Again", font=("Helvetica", 16), command=self.restart_game)
        restart_button.grid(row=15, column=13, columnspan=4, pady=10)

        # Exit Button
        exit_button = Button(self.result_frame, text="Exit", font=("Helvetica", 16), command=self.root.quit)
        exit_button.grid(row=16, column=13, columnspan=4)

    def show_start_screen(self):
        self.problem_frame.grid_remove()
        self.math_frame.grid_remove()
        self.result_frame.grid_remove()
        self.start_frame.grid()



    def start_game(self):
        self.start_frame.grid_remove()
        self.problem_frame.grid()
        # Restart scores when game restarts
        self.utilitarian_score = 0
        self.deontological_score = 0
        self.conflicted_score = 0
        self.current_problem = 0
        self.current_track = "left"
        self.previous_track = None
        self.track_history = []
        self.load_problem()

    def load_problem(self):
        if self.current_problem < len(self.track_nodes):
            node = self.track_nodes[self.current_problem]
            
            # Determine what's on current track and alternative track
            current_side_group = node.left if self.current_track == "left" else node.right
            other_side_group = node.right if self.current_track == "left" else node.left
            
            # Create description based on track
            description = f"The trolley is headed toward {current_side_group}.\n"
            description += f"You can switch tracks to divert it toward {other_side_group}.\n"
            description += "What will you do?"
            
            # Update UI
            self.problem_label.config(text=description)
            self.track_status.config(text=f"Currently on {self.current_track.upper()} track")
            
            # Reset button states
            self.switch_button.config(state=DISABLED)
            self.stay_button.config(state=DISABLED)
            self.challenge_button.config(state=NORMAL)

            self.start_timer()
        else:
            # Hide all other frames
            self.problem_frame.grid_remove()
            self.math_frame.grid_remove()
            self.start_frame.grid_remove()
            
            # Show result screen
            self.show_results()


    def show_results(self):
        # Build summary text
        summary = f"Congratulations! You've completed all dilemmas. We've concluded you have questionable morals!\n\n"
        summary += f"Utilitarian choices: {self.utilitarian_score}\n"
        summary += f"Deontological choices: {self.deontological_score}\n"
        summary += f"Conflicted decisions: {self.conflicted_score}\n"

        if self.utilitarian_score > self.deontological_score:
            summary += "\n\nYou lean utilitarian – you prioritize the greater good over individual rights."
        elif self.deontological_score > self.utilitarian_score:
            summary += "\n\nYou lean deontological – you respect moral duties over outcomes."
        else:
            summary += "\n\nYou're morally conflicted – or indecisive!"

        # Update result text and progress bar
        self.result_label.config(text=summary)
        self.update_progress_bar()
        
        # Fill in the track history
        self.track_history_text.delete(1.0, END)
        for i, history in enumerate(self.track_history):
            scenario = self.track_nodes[i]
            left_group = scenario.left
            right_group = scenario.right
            
            history_text = f"Scenario {i+1}: "
            history_text += f"Left track: {left_group}, Right track: {right_group}\n"
            history_text += f"Your choice: {'Switched' if history['switched'] else 'Stayed'} tracks\n"
            history_text += f"You killed: {history['killed']}\n\n"
            
            self.track_history_text.insert(END, history_text)
        
        # Show the result frame
        self.result_frame.grid()

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

    def make_choice(self, switch):
        if self.timer_id:
            self.root.after_cancel(self.timer_id)

        node = self.track_nodes[self.current_problem]
        
        # Track the history of choices
        killed_group = node.left if self.current_track == "left" else node.right
        
        # Store history for this scenario
        self.track_history.append({
            "switched": switch,
            "killed": killed_group,
            "red_path": node.red_path
        })
        
        # Handle switching tracks
        if switch:
            self.previous_track = self.current_track
            self.current_track = "right" if self.current_track == "left" else "left"
            
            # Check if this was a "red path" switch (ethically conflicted)
            if node.red_path:
                self.conflicted_score += 1
            
            # Update score based on reward type
            if node.reward == "utilitarian":
                self.utilitarian_score += 1
            elif node.reward == "deontological":
                self.deontological_score += 1
        else:
            # Not switching tracks
            if node.reward == "utilitarian":
                self.deontological_score += 1
            elif node.reward == "deontological":
                self.utilitarian_score += 1
        
        print(f"Choice made: {'Switch' if switch else 'Stay'}")
        print(f"Killed: {killed_group}")
        print(f"Utilitarian: {self.utilitarian_score}, Deontological: {self.deontological_score}, Conflicted: {self.conflicted_score}")

        # Move to next problem
        self.current_problem += 1
        self.load_problem()


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
                self.switch_button.config(state=NORMAL)
                self.stay_button.config(state=NORMAL)
                self.challenge_button.config(state=DISABLED)
            else:
                self.math_feedback.config(text="Incorrect. Try again.")
                self.math_entry.delete(0, END)
        except ValueError:
            self.math_feedback.config(text="Please enter a valid number.")
            self.math_entry.delete(0, END)

    def update_progress_bar(self):
        total = self.utilitarian_score + self.deontological_score
        if total == 0:
            percent_util = 50  # neutral start
        else:
            percent_util = (self.utilitarian_score / total) * 100

        # Clear previous bar
        self.progress_canvas.delete("all")

        # Determine bar width
        bar_width = int((percent_util / 100) * 400)

        # Draw utilitarian portion (blue), remainder red
        self.progress_canvas.create_rectangle(0, 0, bar_width, 30, fill="#2196F3", width=0)
        self.progress_canvas.create_rectangle(bar_width, 0, 400, 30, fill="#FF5722", width=0)

        # Draw text label centered
        leaning = ""
        if percent_util > 70:
            leaning = "Strongly Utilitarian"
        elif percent_util > 55:
            leaning = "Moderately Utilitarian"
        elif percent_util > 45:
            leaning = "Neutral"
        elif percent_util > 30:
            leaning = "Moderately Deontological"
        else:
            leaning = "Strongly Deontological"

        self.progress_canvas.create_text(200, 15, text=leaning, font=("Helvetica", 12, "bold"), fill="white")  

    def restart_game(self):
        self.result_frame.grid_remove()
        self.show_start_screen()

if __name__ == "__main__":
    root = Tk()
    game = TrolleyGame(root)
    root.mainloop()