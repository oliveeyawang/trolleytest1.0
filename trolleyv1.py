from tkinter import *
import random

#2:30- May 12, 2025 Olivia
#worked on stroop test
#worked on UI design

def generate_random_math_problem():
        operation = random.choice(["+", "×"])
    
        if operation == "+":
            # Find two numbers that add up to ≤ 50
            a = random.randint(1, 49)
            b = random.randint(1, 50 - a)
            question = f"{a} + {b}?"
            answer = a + b

        else:  # multiplication
            # Choose factors where product ≤ 50
            factors = [(x, y) for x in range(1, 11) for y in range(1, 11) if x * y <= 50]
            a, b = random.choice(factors)
            question = f"{a} × {b}?"
            answer = a * b

        return {"question": question, "answer": answer}
class TrackNode: #each node represents each trolley problem presented to the user
    def __init__(self, left_group, right_group, reward_type, red_path=False):
        self.left = left_group #the "left" track with some set group of people on it
        self.right = right_group #the "right" track with some set group of people on it 
        self.reward = reward_type  # classifies which choice is "utilitarian" or "deontological"
        self.red_path = red_path #if the path is particularly morally challenging/illogical
        #add self.danger_path = danger_path #choices that identify psycho edge cases??

class TrolleyGame(object): 
    def __init__(self, root):
        self.choices_enabled = False
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

        self.stroop_tasks = [
            {"word": "RED", "color": "blue", "correct": "blue"},
            {"word": "GREEN", "color": "red", "correct": "red"},
            {"word": "BLUE", "color": "green", "correct": "green"},
            {"word": "YELLOW", "color": "purple", "correct": "purple"},
            {"word": "PURPLE", "color": "yellow", "correct": "yellow"},
            {"word": "BLACK", "color": "orange", "correct": "orange"},
            {"word": "ORANGE", "color": "black", "correct": "black"},
            {"word": "WHITE", "color": "green", "correct": "green"},
            {"word": "GRAY", "color": "red", "correct": "red"},
            {"word": "BROWN", "color": "blue", "correct": "blue"}
        ]

        # Create all frames
        self.start_frame = Frame(self.root)
        self.problem_frame = Frame(self.root)
        self.math_frame = Frame(self.root)
        self.stroop_frame = Frame(self.root)
        self.result_frame = Frame(self.root)

        # Setup all screens
        self.setup_start_screen()
        self.setup_problem_screen()
        self.setup_math_screen()
        self.setup_stroop_screen() 
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
        start_button = Label(self.start_frame, text="Begin the Test",
                     font=("Helvetica", 20), bg="#a0fc8d", fg="black",
                     padx=20, pady=10, cursor="hand2")
        start_button.grid(row=10, column=10, columnspan=10, pady=28)

        start_button.bind("<Button-1>", lambda e: self.start_game())
        start_button.bind("<Enter>", lambda e: start_button.config(bg="#90e37a"))
        start_button.bind("<Leave>", lambda e: start_button.config(bg="#a0fc8d"))

        # Centered exit button
        exit_button = Label(self.start_frame, text="Exit", font=("Helvetica", 16),
                    bg="#ff776d", fg="black", padx=20, pady=10, cursor="hand2")
        exit_button.grid(row=15, column=13, columnspan=4)

        exit_button.bind("<Button-1>", lambda e: self.root.attributes('-fullscreen', False))
        exit_button.bind("<Enter>", lambda e: exit_button.config(bg="#e4665d"))
        exit_button.bind("<Leave>", lambda e: exit_button.config(bg="#ff776d"))

    def setup_problem_screen(self):
        self.problem_frame.grid(row=0, column=0, rowspan=30, columnspan=30, sticky="nsew")
        self.problem_frame.grid_remove()  # Hide it first
        self.feedback_label = Label(self.problem_frame, text="", font=("Helvetica", 14), fg="red")
        self.feedback_label.grid(row=20, column=10, columnspan=10)

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
        self.challenge_button = Button(self.problem_frame, text="Complete Task First", 
                                 font=("Helvetica", 14), command=self.show_math_challenge, 
                                 bg="#FFC107", padx=10, pady=5)
        self.challenge_button.grid(row=10, column=10, columnspan=10, pady=10)

       # Centered choice buttons
        # Stay Button
        self.stay_button = Label(self.problem_frame, text="Stay on Track", font=("Helvetica", 16),
                         fg="black", bg="#8afcfd", padx=15, pady=8, cursor="hand2")
        self.stay_button.grid(row=15, column=7, columnspan=6, pady=20)

        self.stay_button.bind("<Button-1>", self.handle_stay_click)
        self.stay_button.bind("<Enter>", lambda e: self.stay_button.config(bg="#75d7d8") if self.choices_enabled else None)
        self.stay_button.bind("<Leave>", lambda e: self.stay_button.config(bg="#8afcfd") if self.choices_enabled else self.stay_button.config(bg="#cccccc"))

        # Switch Button
        self.switch_button = Label(self.problem_frame, text="Switch Tracks", font=("Helvetica", 16),
                           fg="black", bg="#f291de", padx=15, pady=8, cursor="hand2")
        self.switch_button.grid(row=15, column=17, columnspan=6, pady=20)

        self.switch_button.bind("<Button-1>", self.handle_switch_click)
        self.switch_button.bind("<Enter>", lambda e: self.switch_button.config(bg="#c0469e") if self.choices_enabled else None)
        self.switch_button.bind("<Leave>", lambda e: self.switch_button.config(bg="#f28bde") if self.choices_enabled else self.switch_button.config(bg="#cccccc"))

    def handle_stay_click(self, event=None):
            print("Stay clicked")
            self.fake_button_click(False)

    def handle_switch_click(self, event=None):
            print("Switch clicked")
            self.fake_button_click(True)
            
    def fake_button_click(self, switch):
        if self.choices_enabled:
            self.feedback_label.config(text="")
            self.make_choice(switch)
        else:
            self.feedback_label.config(text="You must complete the task first.")
            self.root.after(2000, lambda: self.feedback_label.config(text=""))

    def setup_math_screen(self):
        self.math_frame.grid(row=0, column=0, rowspan=30, columnspan=30, sticky="nsew")
        self.math_frame.grid_remove()

        for i in range(30):  
            self.math_frame.columnconfigure(i, weight=1)
            self.math_frame.rowconfigure(i, weight=1)

        self.task_type_label = Label(self.math_frame, text="", font=("Helvetica", 20, "italic"))
        self.task_type_label.grid(row=3, column=10, columnspan=10, pady=(10, 0))

        # Centered math challenge elements
        self.task_label = Label(self.math_frame, text="", font=("Helvetica", 24))
        self.task_label.grid(row=5, column=10, columnspan=10, pady=20)

        # Shared entry field
        self.task_entry = Entry(self.math_frame, font=("Helvetica", 18), width=10, justify='center')
        self.task_entry.grid(row=10, column=12, columnspan=6, pady=10)

        # Shared feedback label
        self.task_feedback = Label(self.math_frame, text="", font=("Helvetica", 16), fg="red")
        self.task_feedback.grid(row=12, column=10, columnspan=10)

        self.submit_button = Button(self.math_frame, text="Submit", font=("Helvetica", 16), command=self.check_math_answer)
        self.submit_button.grid(row=14, column=12, columnspan=6, pady=10)

    def setup_stroop_screen(self):
        # New dedicated screen for the Stroop test with color buttons
        self.stroop_frame.grid(row=0, column=0, rowspan=30, columnspan=30, sticky="nsew")
        self.stroop_frame.grid_remove()
        
        for i in range(30):  
            self.stroop_frame.columnconfigure(i, weight=1)
            self.stroop_frame.rowconfigure(i, weight=1)
        
        # Instruction label
        instruction_text = "Name the COLOR of the text, not the word itself."
        self.stroop_instruction = Label(self.stroop_frame, text=instruction_text, font=("Helvetica", 16))
        self.stroop_instruction.grid(row=2, column=5, columnspan=20, pady=10)
        
        # Stroop test title
        self.stroop_title = Label(self.stroop_frame, text="Stroop Color Test", font=("Helvetica", 24, "bold"))
        self.stroop_title.grid(row=4, column=5, columnspan=20, pady=10)
        
        # Stroop word display (large)
        self.stroop_word = Label(self.stroop_frame, text="", font=("Helvetica", 72, "bold"))
        self.stroop_word.grid(row=8, column=5, columnspan=20, pady=30)
        
        # Color buttons frame
        color_frame = Frame(self.stroop_frame)
        color_frame.grid(row=15, column=5, columnspan=20, pady=20)
        
        # Create color buttons
        self.color_buttons = {}
        colors = ["red", "blue", "green", "yellow", "purple", "orange", "black"]
        color_names = ["Red", "Blue", "Green", "Yellow", "Purple", "Orange", "Black"]
        
        for i, (color, name) in enumerate(zip(colors, color_names)):
            btn = Button(color_frame, text=name, bg=color, 
                      width=8, height=2, font=("Helvetica", 12),
                      command=lambda c=color: self.check_stroop_answer(c))
            
            # Make text white for dark backgrounds
            if color in ["blue", "purple", "black"]:
                btn.config(fg="white")
                
            btn.grid(row=0, column=i, padx=5)
            self.color_buttons[color] = btn
        
        # Feedback label
        self.stroop_feedback = Label(self.stroop_frame, text="", font=("Helvetica", 16))
        self.stroop_feedback.grid(row=18, column=5, columnspan=20, pady=10)
        
        # Timer for Stroop test
        self.stroop_timer_label = Label(self.stroop_frame, text="Time: 10", font=("Helvetica", 16))
        self.stroop_timer_label.grid(row=1, column=28, columnspan=2, pady=10, padx=10, sticky="ne")


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
            self.choices_enabled = False
            self.stay_button.config(bg="#cccccc")
            self.switch_button.config(bg="#cccccc")
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

    def return_to_problem(self):
        self.stroop_frame.grid_remove()
        self.problem_frame.grid()
        self.choices_enabled = True
        self.switch_button.config(bg="#f291de")
        self.stay_button.config(bg="#8afcfd")
        self.challenge_button.config(state=DISABLED)

    def show_math_challenge(self):
        self.problem_frame.grid_remove()
        task_type = random.choice(["math", "stroop"])
        self.current_task_type = task_type

        if task_type == "math":
            self.math_frame.grid()
            self.task_entry.delete(0, END)
            self.task_feedback.config(text="")
            self.task_type_label.config(text="Math Task", fg="blue")
            problem = generate_random_math_problem()
            self.current_math_answer = problem["answer"]
            self.task_label.config(text=problem["question"], fg="black")
        else:
            self.stroop_frame.grid()
            self.stroop_feedback.config(text="")
            stroop = random.choice(self.stroop_tasks)
            self.current_stroop_answer = stroop["correct"]
            self.stroop_word.config(text=stroop["word"], fg=stroop["color"])
            self.start_stroop_timer()


    def check_math_answer(self):
        user_input = self.task_entry.get().strip()

        if self.current_task_type == "math":
            try:
                entered = int(user_input)
                if entered == self.current_math_answer:
                    self.complete_challenge()
                else:
                    self.task_feedback.config(text="Incorrect. Try again.")
                    self.task_entry.delete(0, END)
            except ValueError:
                self.task_feedback.config(text="Enter a valid number.")
                self.task_entry.delete(0, END)
        else:
            if user_input.lower() == self.current_stroop_answer:
                self.complete_challenge()
            else:
                self.task_feedback.config(text="Stroop mismatch. Try again.")
                self.task_entry.delete(0, END)

    def start_stroop_timer(self):
        self.stroop_time_left = 10
        self.update_stroop_timer()

    def update_stroop_timer(self):
        self.stroop_timer_label.config(text=f"Time: {self.stroop_time_left}")
        if self.stroop_time_left <= 0:
            self.stroop_feedback.config(text="Too slow!")
            self.root.after(1000, self.return_to_problem)
        else:
            self.stroop_time_left -= 1
            self.root.after(1000, self.update_stroop_timer)
    def check_stroop_answer(self, selected_color):
        if selected_color == self.current_stroop_answer:
            self.return_to_problem()
        else:
            self.stroop_feedback.config(text="Wrong color. Try again.")

    def complete_challenge(self):
        self.math_frame.grid_remove()
        self.problem_frame.grid()
        self.choices_enabled = True
        self.stay_button.config(bg="#8afcfd")
        self.switch_button.config(bg="#f291de")
        #self.switch_button.config(state=NORMAL)
        #self.stay_button.config(state=NORMAL)
        self.challenge_button.config(state=DISABLED)

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