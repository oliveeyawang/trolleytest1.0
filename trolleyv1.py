from tkinter import *
import random
from PIL import Image, ImageTk
#repushing 10am changes
#10am-10:45am May 12, 2025 Olivia
#added immediate feedback intermediate slide

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
    def __init__(self, bottom_group, top_group, reward_type, red_path=False):
        
        self.bottom = bottom_group #the bottom track with a set group of people on it
        self.top = top_group #the right track with a set group of people on it 
        self.reward = reward_type # classifies which choice is "utilitarian" or "deontological"
        self.red_path = red_path  #if the path is particularly morally challenging/illogical
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
        self.current_track = "bottom"  # start on bottom track
        self.previous_track = None

        # timer variables
        self.timer_label = Label(self.root, text="Time: 60", font=("Helvetica", 16))
        self.timer_label.place(relx=0.95, rely=0.02, anchor="ne")  # this floats it top right

        
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
            TrackNode("5 people", "1 person", "utilitarian"), # Stay = deontological (kill 5), Switch = utilitarian (kill 1)
            TrackNode("a family member", "5 people", "deontological", red_path=True), # Stay = kill family, Switch = kill 5
            TrackNode("5 of your closest friends", "a baby", "deontological"), # Stay = kill friends, Switch = kill baby
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
        self.decision_frame = Frame(self.root)
        self.result_frame = Frame(self.root)
        self.timer_id = None


        # Setup all screens
        self.setup_start_screen()
        self.setup_problem_screen()
        self.setup_math_screen()
        self.setup_stroop_screen() 
        self.setup_decision_screen()
        self.setup_result_screen()

        self.show_start_screen()

    def setup_start_screen(self):
        for i in range(30):  
            self.start_frame.columnconfigure(i, weight=1)
            self.start_frame.rowconfigure(i, weight=1)

        self.start_frame.grid(row=0, column=0, rowspan=30, columnspan=30, sticky="nsew")

        # Centered title
        title_label = Label(self.start_frame, text="The Trolley Problem Quiz", font=("Helvetica", 36, "bold"))
        title_label.grid(row=6, column=5, columnspan=20, pady=20)

        # Load placeholder image
        img = Image.open("placeholder.jpg")
        img = img.resize((400, 250))  # Resize to fit your aesthetic despair
        self.placeholder_photo = ImageTk.PhotoImage(img)

        # Add to label
        self.placeholder_label = Label(self.start_frame, image=self.placeholder_photo)
        self.placeholder_label.grid(row=7, column=10, columnspan=10, pady=10)

        #instructions
        instructions = ("INSTRUCTIONS:\n"
                "You will face 7 trolley dilemmas.\n"
                "You will have 60 seconds to read each scenerio and make a decision.\n"
                "The catch: To make any kind of choice, you first must complete a little task.\n"
                "We WILL judge your morality! \n\n")
        instruction_label = Label(self.start_frame, text=instructions, font=("Helvetica", 20), wraplength=700, justify="center")
        instruction_label.grid(row=11, column=5, columnspan=20, pady=(10, 30))

        # Centered start button
        start_button = Label(self.start_frame, text="Begin the Test",
                     font=("Helvetica", 20), bg="#a0fc8d", fg="black",
                     padx=20, pady=10, cursor="hand2")
        start_button.grid(row=12, column=10, columnspan=10, pady=28)

        start_button.bind("<Button-1>", lambda e: self.start_game())
        start_button.bind("<Enter>", lambda e: start_button.config(bg="#90e37a"))
        start_button.bind("<Leave>", lambda e: start_button.config(bg="#a0fc8d"))


        # Centered exit button
        exit_button = Label(self.start_frame, text="Exit", font=("Helvetica", 16),
                    bg="#ff776d", fg="black", padx=20, pady=10, cursor="hand2")
        exit_button.grid(row=17, column=13, columnspan=4)

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


        # Centered problem description
        self.problem_label = Label(self.problem_frame, text="", font=("Helvetica", 18), 
                             wraplength=900, justify="center")
        self.problem_label.grid(row=5, column=5, columnspan=20, pady=30)

         # Track status indicator
        self.track_status = Label(self.problem_frame, text="", font=("Helvetica", 16, "italic"),
                                 fg="#666666")
        self.track_status.grid(row=7, column=5, columnspan=20)

        #task button
        self.challenge_button = Label(self.problem_frame, text="Complete Task First",
                              font=("Helvetica", 14), bg="#FFC107", fg="black",
                              padx=15, pady=8, cursor="hand2")
        self.challenge_button.grid(row=10, column=10, columnspan=10, pady=10)

        self.challenge_button.bind("<Button-1>", lambda e: self.show_math_challenge())
        self.challenge_button.bind("<Enter>", lambda e: self.challenge_button.config(bg="#e6ac06"))
        self.challenge_button.bind("<Leave>", lambda e: self.challenge_button.config(bg="#FFC107"))

        # Centered choice buttons
        # Stay Button
        self.stay_button = Label(self.problem_frame, text="Stay on Current Track", font=("Helvetica", 16),
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

    def disable_challenge_button(self):
        self.challenge_button.unbind("<Button-1>")
        self.challenge_button.unbind("<Enter>")
        self.challenge_button.unbind("<Leave>")
        self.challenge_button.config(bg="#cccccc", fg="#777777", cursor="arrow")

    def enable_challenge_button(self):
        self.challenge_button.bind("<Button-1>", lambda e: self.show_math_challenge())
        self.challenge_button.bind("<Enter>", lambda e: self.challenge_button.config(bg="#e6ac06"))
        self.challenge_button.bind("<Leave>", lambda e: self.challenge_button.config(bg="#FFC107"))
        self.challenge_button.config(bg="#FFC107", fg="black", cursor="hand2")
      
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
        self.timer_label.lift()


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

        self.submit_button = Label(self.math_frame, text="Submit",
                           font=("Helvetica", 16), bg="#FFC107", fg="black",
                           padx=15, pady=8, cursor="hand2")
        self.submit_button.grid(row=14, column=12, columnspan=6, pady=10)

        # Event bindings
        self.submit_button.bind("<Button-1>", lambda e: self.check_math_answer())
        self.submit_button.bind("<Enter>", lambda e: self.submit_button.config(bg="#e6ac06"))
        self.submit_button.bind("<Leave>", lambda e: self.submit_button.config(bg="#FFC107"))


    def setup_stroop_screen(self):
        # New dedicated screen for the Stroop test with color buttons
        self.stroop_frame.grid(row=0, column=0, rowspan=30, columnspan=30, sticky="nsew")
        self.stroop_frame.grid_remove()
        self.timer_label.lift()

        
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
            btn = Label(color_frame, text=name, bg=color, width=8, height=2,
                        font=("Helvetica", 12), cursor="hand2")

            # Fix text color for dark backgrounds
            if color in ["blue", "purple", "black","green"]:
                btn.config(fg="white")
            else:
                btn.config(fg="black")

            # Click binding
            btn.bind("<Button-1>", lambda e, c=color: self.check_stroop_answer(c))

            # Optional hover (if you want it to darken slightly)
            def on_enter(e, widget=btn):
                widget.config(relief="sunken")

            def on_leave(e, widget=btn):
                widget.config(relief="flat")

            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)

            btn.grid(row=0, column=i, padx=5)
            self.color_buttons[color] = btn

        
        # Feedback label
        self.stroop_feedback = Label(self.stroop_frame, text="", font=("Helvetica", 16))
        self.stroop_feedback.grid(row=18, column=5, columnspan=20, pady=10)


    #for robust user choice tracking
    def evaluate_moral_alignment(self, node, switched):
        # Determine which path the trolley ends up on after the decision
        final_track = self.current_track if not switched else ("top" if self.current_track == "bottom" else "bottom")
        killed_group = node.top if final_track == "top" else node.bottom

        # Base scoring
        if node.red_path:
            # remove from whichever philosophy point just got added
            if node.reward == "utilitarian" and switched:
                self.utilitarian_score -= 1
            elif node.reward == "deontological" and not switched:
                self.deontological_score -= 1
            self.conflicted_score += 1  # or keep as penalty bucket
        elif "family" in killed_group.lower() or "partner" in killed_group.lower() or "child" in killed_group.lower():
            self.conflicted_score += 1  # this is where we’d trigger the psycho track if we had it
        elif node.reward == "utilitarian" and switched:
            self.utilitarian_score += 1
        elif node.reward == "deontological" and not switched:
            self.deontological_score += 1
        else:
            self.conflicted_score += 1

        return killed_group

    #shows the user a screen containing the choice they just made
    def setup_decision_screen(self):
        self.decision_frame.grid(row=0, column=0, rowspan=30, columnspan=30, sticky="nsew")
        self.decision_frame.grid_remove()

        for i in range(30):
            self.decision_frame.columnconfigure(i, weight=1)
            self.decision_frame.rowconfigure(i, weight=1)

        self.decision_label = Label(self.decision_frame, text="", font=("Helvetica", 20), wraplength=900, justify="center")
        self.decision_label.grid(row=5, column=5, columnspan=20, pady=30)

        self.decision_image = Label(self.decision_frame)
        self.decision_image.grid(row=10, column=10, columnspan=10)


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
        self.timer_label.place_forget()



    def start_game(self):
        self.start_frame.grid_remove()
        self.problem_frame.grid()
        # Restart scores when game restarts
        self.timer_label.place(relx=0.95, rely=0.02, anchor="ne")
        self.utilitarian_score = 0
        self.deontological_score = 0
        self.conflicted_score = 0
        self.current_problem = 0
        self.current_track = "bottom"
        self.previous_track = None
        self.track_history = []
        self.load_problem()

    def load_problem(self):
        # Hide everything 
        self.start_frame.grid_remove()
        self.math_frame.grid_remove()
        self.stroop_frame.grid_remove()
        self.decision_frame.grid_remove()
        self.result_frame.grid_remove()

        if self.current_problem < len(self.track_nodes):
            #troubleshooting
            self.problem_frame.grid()
            self.problem_frame.tkraise()
            self.timer_label.place(relx=0.95, rely=0.02, anchor="ne")
            self.timer_label.lift()

            # TEST visibility
            # Load the track node
            node = self.track_nodes[self.current_problem]

            # Build description
            current_side_group = node.bottom if self.current_track == "bottom" else node.top
            other_side_group = node.top if self.current_track == "bottom" else node.bottom

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
            self.enable_challenge_button()

            self.start_timer()
        else:
            print("No more problems. Showing results.")
            self.problem_frame.grid_remove()
            self.show_results()


    def show_results(self):
        self.result_frame.grid()
        print("Result screen displayed")
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
            bottom_group = scenario.bottom
            top_group = scenario.top
            
            history_text = f"Scenario {i+1}: "
            history_text += f"Bottom track: {bottom_group}, Top track: {top_group}\n"
            history_text += f"Your choice: {'Switched' if history['switched'] else 'Stayed'} tracks\n"
            history_text += f"You killed: {history['killed']}\n\n"
            
            self.track_history_text.insert(END, history_text)
        
        # Show the result frame
        self.result_frame.grid()

    def start_timer(self):
        self.timer_id = None
        if self.timer_id is not None:
            self.root.after_cancel(self.timer_id)

        self.time_left = 60
        self.update_timer()

    def update_timer(self):
        if self.time_left <= 0:
            self.out_of_time()
        else:
            color = "red" if self.time_left <= 10 else "black"
            font = ("Helvetica", 18, "bold") if self.time_left <= 10 else ("Helvetica", 16)
        
        self.timer_label.config(text=f"Time: {self.time_left}", fg=color, font=font)
        
        self.time_left -= 1
        self.timer_id = self.root.after(1000, self.update_timer)

    #if user runs out of time on choice
    def out_of_time(self):
        self.stroop_frame.grid_remove()
        self.math_frame.grid_remove()
        self.problem_frame.grid_remove()

        # Treat as default "stay"
        node = self.track_nodes[self.current_problem]
        killed = node.bottom if self.current_track == "bottom" else node.top

        self.track_history.append({
            "switched": False,
            "killed": killed,
            "red_path": node.red_path
        })

        if node.reward == "utilitarian":
            self.deontological_score += 1
        else:
            self.utilitarian_score += 1

        self.show_decision_screen(False, killed)

    def make_choice(self, switch):
        if self.timer_id:
            self.root.after_cancel(self.timer_id)

        node = self.track_nodes[self.current_problem]
        
        # Track the history of choices
        # If user switched, flip the track
        if switch:
            self.previous_track = self.current_track
            self.current_track = "top" if self.current_track == "bottom" else "bottom"

        killed_group = self.evaluate_moral_alignment(node, switch)

        # Log the decision
        self.track_history.append({
            "switched": switch,
            "killed": killed_group,
            "red_path": node.red_path
        })

        print(f"Choice made: {'Switch' if switch else 'Stay'}")
        print(f"Killed: {killed_group}")
        print(f"Utilitarian: {self.utilitarian_score}, Deontological: {self.deontological_score}, Conflicted: {self.conflicted_score}")

        self.show_decision_screen(switch, killed_group)
        
    
    def show_decision_screen(self, switched, killed):
        self.problem_frame.grid_remove()
        self.math_frame.grid_remove()
        self.timer_label.place_forget()
        self.stroop_frame.grid_remove()
    
        message = f"You {'switched tracks' if switched else 'stayed on the current track'}.\n"
        message += f"You killed: {killed}"

        self.decision_label.config(text=message)

        # Show an image based on choice (use dummy for now)

        img = Image.open("placeholder.png")  # Replace with actual image logic
        img = img.resize((400, 250))
        photo = ImageTk.PhotoImage(img)

        self.decision_image.config(image=photo)
        self.decision_image.image = photo  # keep reference
        self.decision_frame.grid()

        self.continue_button = Label(self.decision_frame, text="Continue",
                             font=("Helvetica", 16), bg="#FFC107", fg="black",
                             padx=15, pady=8, cursor="hand2")
        self.continue_button.grid(row=15, column=13, columnspan=4, pady=(30, 0))

        self.continue_button.bind("<Button-1>", lambda e: self.next_problem())
        self.continue_button.bind("<Enter>", lambda e: self.continue_button.config(bg="#e6ac06"))
        self.continue_button.bind("<Leave>", lambda e: self.continue_button.config(bg="#FFC107"))
        

    def next_problem(self):
        #troubleshooting
        self.decision_frame.grid_remove()
        self.problem_frame.grid()
        self.problem_frame.tkraise()
        self.current_problem += 1
        self.load_problem()

    def return_to_problem(self):
        self.stroop_frame.grid_remove()
        self.problem_frame.grid()
        self.choices_enabled = True
        self.switch_button.config(bg="#f291de")
        self.stay_button.config(bg="#8afcfd")
        self.disable_challenge_button()

    def show_math_challenge(self):
        self.problem_frame.grid_remove()
        task_type = random.choice(["math", "stroop"])
        self.current_task_type = task_type

        if task_type == "math":
            self.math_frame.grid()
            self.task_entry.delete(0, END)
            self.task_entry.focus_set()
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
        self.disable_challenge_button()

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