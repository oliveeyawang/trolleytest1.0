from tkinter import *
import random
from PIL import Image, ImageTk
#9pm-10pm
#debugging utilitarian path / evaluate moral standpoint
#sort of still iffy

def generate_random_math_problem():
    # Choose between multiplication and addition
        operation = random.choice(["+", "×"])
    
        if operation == "+":
            # Find two numbers that add up to 50 or less
            a = random.randint(1, 49)
            b = random.randint(1, 50 - a) # Second number must add to 50 or less
            question = f"{a} + {b}?"
            answer = a + b  

        else:  # multiplication
            # Choose factors where product is 50 or less
            factors = [(x, y) for x in range(1, 11) for y in range(1, 11) if x * y <= 50]
            a, b = random.choice(factors) # pick one random pair
            question = f"{a} × {b}?"
            answer = a * b

        return {"question": question, "answer": answer}
class TrackNode: #each node represents each trolley problem presented to the user
    def __init__(self, bottom_group, top_group, reward_type, red_path=False):
        
        self.bottom = bottom_group #the bottom track with a set group of people on it
        self.top = top_group #the right track with a set group of people on it 
        self.reward = reward_type # classifies which choice is "utilitarian" or "deontological"
        self.red_path = red_path  #if the path is particularly morally challenging/illogical
        

class TrolleyGame(object): 
    def __init__(self, root):
        self.choices_enabled = False # Choice isn't imitially available
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
        self.timer_label = Label(self.root, text="Time:30", font=("Helvetica", 16), bg="white")
        self.timer_label.place(relx=0.95, rely=0.02, anchor="ne")  # this floats it top right

        # Grid to work with
        for i in range(30):  
            self.root.columnconfigure(i, weight=1)
            self.root.rowconfigure(i, weight=1)

        # Escape key exits fullscreen
        self.root.bind("<Escape>", lambda event: self.root.attributes('-fullscreen', False))

        # Store which problem we're on
        self.current_problem = 0

        # Define track nodes with the trolley problems
        # this flow needs a lot of work...because the philosophical classification of each scenerio depends 
        # on which track they're currently on and their past choices
        self.track_nodes = [
            TrackNode("5 people", "1 person", "utilitarian"), # Stay = deontological (kill 5), Switch = utilitarian (kill 1)
            TrackNode("a family member", "5 people", "utilitarian", red_path=True), # Stay = kill family, Switch = kill 5
            TrackNode("5 of your closest friends", "a baby", "deontological"), # Stay = kill friends, Switch = kill baby
            TrackNode("2 brilliant doctors", "another family member", "deontological", red_path=True),
            TrackNode("5 preschoolers", "an active shooter", "utilitarian", red_path=True),
            TrackNode("nothing", "a bomb, so that the train is destroyed/stopped (but you can see about 8-10 people in the trolley)", "deontological"),
            TrackNode("an assassin with a 75% chance of killing you and a couple innocent bystanders", "nothing however the assassin has exactly three bullets", "deontological"), #add some roll the dice thing
            TrackNode("you, your partner, and your child", "10 world leaders, 10 noble peace prize winners, 10 philanthropists, and 1 infant", "deontological", red_path=True),
        ]

        # preload decision feedback images (DFTop1–8, DFBottom1–8)
        self.decision_images = {}  # e.g. {"DFTop1": PhotoImage, "DFBottom1": PhotoImage}
        self.flow_images = {}
        self.images = {}  
        self.images["Title"] = ImageTk.PhotoImage(Image.open("Title.jpg"))
        for i in range(1, 9):
            for prefix in ["DFTop", "DFBottom"]:
                key = f"{prefix}{i}"
                try:
                    img = Image.open(f"{key}.jpg")
                    self.decision_images[key] = ImageTk.PhotoImage(img)
                except FileNotFoundError:
                    print(f"Warning: Missing decision image {key}.jpg")

        # Special outcomes for Scenario 7 (Assassin)
        for name in ["DFTop7Die", "DFTop7Live"]:
            try:
                img = Image.open(f"{name}.jpg")
                self.decision_images[name] = ImageTk.PhotoImage(img)
            except FileNotFoundError:
                print(f"Warning: Missing special image {name}.jpg")

        # Load track flow images (SFTop2–8, SFBottom2–8)
        for i in range(1, 9):
            for prefix in ["SFTop", "SFBottom"]:
                key = f"{prefix}{i}"
                try:
                    img = Image.open(f"{key}.jpg")
                    self.flow_images[key] = ImageTk.PhotoImage(img)
                except FileNotFoundError:
                    print(f"Warning: Missing flow image {key}.jpg")
    
        # Stroop Task Test
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
        self.start_frame = Frame(self.root, bg="white")
        self.problem_frame = Frame(self.root, bg="white")
        self.math_frame = Frame(self.root, bg="white")
        self.stroop_frame = Frame(self.root, bg="white")
        self.decision_frame = Frame(self.root, bg="white")
        self.result_frame = Frame(self.root, bg="white")
        self.timer_id = None


        # Setup all screens
        self.setup_start_screen()
        self.setup_problem_screen()
        self.setup_math_screen()
        self.setup_stroop_screen() 
        self.setup_decision_screen()
        self.setup_result_screen()

        self.show_start_screen()

    def show_frame(self, frame):
        for f in [self.start_frame, self.problem_frame, self.math_frame,
                self.stroop_frame, self.decision_frame, self.result_frame]:
            f.grid_remove() # Hide other frames
        frame.grid(row=0, column=0, rowspan=30, columnspan=30, sticky="nsew")
        frame.tkraise() # Bring frame to the front
        
    def update_button_states(self, active):
        if active:
            self.stay_button.config(bg="black", fg="white", cursor="hand2")
            self.switch_button.config(bg="#3478f6", fg="white", cursor="hand2")
        else: # Makes inactive buttons look inactive
            self.stay_button.config(bg="#cccccc", fg="#777777", cursor="arrow")
            self.switch_button.config(bg="#cccccc", fg="#777777", cursor="arrow")

    def setup_start_screen(self):
        # Screen setup
        for i in range(30):  
            self.start_frame.columnconfigure(i, weight=1)
            self.start_frame.rowconfigure(i, weight=1)

        self.start_frame.grid(row=0, column=0, rowspan=30, columnspan=30, sticky="nsew")

        # Load Title image
        self.Title_photo = self.images["Title"]

        # Add to label
        self.Title_label = Label(self.start_frame, image=self.Title_photo, bg="white")
        self.Title_label.grid(row=7, column=10, columnspan=10, pady=10)

        #instructions
        instructions = ("INSTRUCTIONS:\n"
                "You will face up to 8 trolley problems.\n"
                "You will have 30 seconds to read each scenerio and make a decision.\n"
                "The catch: To make any kind of choice, you first must complete a little task.\n"
                "We WILL judge your morality! \n")
        instruction_label = Label(self.start_frame, text=instructions, font=("Helvetica", 20), bg="white", wraplength=700, justify="center")
        instruction_label.grid(row=8, column=5, columnspan=20, pady=(10, 30))

        # Centered start button
        start_button = Label(self.start_frame, text="Begin the Quiz",
                     font=("Helvetica", 20), bg="#a0fc8d", fg="black",
                     padx=20, pady=10, cursor="hand2")
        start_button.grid(row=9, column=10, columnspan=10, pady=28)

        start_button.bind("<Button-1>", lambda e: self.start_game())
        start_button.bind("<Enter>", lambda e: start_button.config(bg="#90e37a"))
        start_button.bind("<Leave>", lambda e: start_button.config(bg="#a0fc8d"))


        # Centered exit button
        exit_button = Label(self.start_frame, text="Exit", font=("Helvetica", 16),
                    bg="#ff776d", fg="black", padx=20, pady=10, cursor="hand2")
        exit_button.grid(row=10, column=13, columnspan=4)

        exit_button.bind("<Button-1>", lambda e: self.root.attributes('-fullscreen', False))
        exit_button.bind("<Enter>", lambda e: exit_button.config(bg="#e4665d"))
        exit_button.bind("<Leave>", lambda e: exit_button.config(bg="#ff776d"))

    def setup_problem_screen(self):
        self.problem_frame.grid(row=0, column=0, rowspan=30, columnspan=30, sticky="nsew")
        self.problem_frame.grid_remove()  # Hide it first
        # Feedback for user
        self.feedback_label = Label(self.problem_frame, text="", font=("Helvetica", 14), fg="red", bg="white")
        self.feedback_label.grid(row=20, column=10, columnspan=10)
        self.problem_illustration = Label(self.problem_frame, bg="white")
        self.problem_illustration.grid(row=8, column=10, columnspan=10, pady=(10, 20))

        for i in range(30):  
            self.problem_frame.columnconfigure(i, weight=1)
            self.problem_frame.rowconfigure(i, weight=1)


        # Centered problem description
        self.problem_label = Label(self.problem_frame, text="", font=("Helvetica", 18), bg="white",
                             wraplength=900, justify="center")
        self.problem_label.grid(row=5, column=5, columnspan=20, pady=30)

         # Track status indicator
        self.track_status = Label(self.problem_frame, text="", font=("Helvetica", 16, "italic"), bg="white",
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
                         fg="#777777", bg="#cccccc", padx=15, pady=8, cursor="arrow")
        self.stay_button.grid(row=15, column=7, columnspan=6, pady=20)

        self.stay_button.bind("<Button-1>", self.handle_stay_click)
        self.stay_button.bind("<Enter>", lambda e: self.stay_button.config(bg="#444444") if self.choices_enabled else None)
        self.stay_button.bind("<Leave>", lambda e: self.stay_button.config(bg="black") if self.choices_enabled else self.stay_button.config(bg="#cccccc"))

        # Switch Button
        self.switch_button = Label(self.problem_frame, text="Switch Tracks", font=("Helvetica", 16),
                            fg="#777777", bg="#cccccc", padx=15, pady=8, cursor="arrow")
        self.switch_button.grid(row=15, column=17, columnspan=6, pady=20)

        self.switch_button.bind("<Button-1>", self.handle_switch_click)
        self.switch_button.bind("<Enter>", lambda e: self.switch_button.config(bg="#245fc2") if self.choices_enabled else None)
        self.switch_button.bind("<Leave>", lambda e: self.switch_button.config(bg="#3478f6") if self.choices_enabled else self.switch_button.config(bg="#cccccc"))

    def handle_stay_click(self, event=None):
            print("Stay clicked") #debugging
            self.fake_button_click(False)

    def handle_switch_click(self, event=None):
            print("Switch clicked") # debugging
            self.fake_button_click(True)

    def disable_challenge_button(self):
        # Remove interactivity
        self.challenge_button.unbind("<Button-1>")
        self.challenge_button.unbind("<Enter>")
        self.challenge_button.unbind("<Leave>")
        self.challenge_button.config(bg="#cccccc", fg="#777777", cursor="arrow")

    def enable_challenge_button(self):
        # Enable interactivity
        self.challenge_button.bind("<Button-1>", lambda e: self.show_math_challenge())
        self.challenge_button.bind("<Enter>", lambda e: self.challenge_button.config(bg="#e6ac06"))
        self.challenge_button.bind("<Leave>", lambda e: self.challenge_button.config(bg="#FFC107"))
        self.challenge_button.config(bg="#FFC107", fg="black", cursor="hand2")
      
    def fake_button_click(self, switch): # Switch is boolean
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

        # Grid
        for i in range(30):  
            self.math_frame.columnconfigure(i, weight=1)
            self.math_frame.rowconfigure(i, weight=1)

        # Task labels
        self.task_type_label = Label(self.math_frame, text="", font=("Helvetica", 20, "italic"))
        self.task_type_label.grid(row=3, column=10, columnspan=10, pady=(10, 0))

        # Centered math challenge elements
        self.task_label = Label(self.math_frame, text="", font=("Helvetica", 24), bg="white", fg="black")
        self.task_label.grid(row=5, column=10, columnspan=10, pady=20)

        # Tasks appear in same position
        self.task_entry = Entry(self.math_frame, font=("Helvetica", 18), width=10, justify='center')
        self.task_entry.grid(row=10, column=12, columnspan=6, pady=10)

        # Shared feedback label
        self.task_feedback = Label(self.math_frame, text="", font=("Helvetica", 16), fg="red")
        self.task_feedback.grid(row=12, column=10, columnspan=10)

        self.submit_button = Label(self.math_frame, text="Unlock Choice",
            font=("Helvetica", 16), bg="#FFC107", fg="black", padx=15, pady=8, cursor="hand2")
        self.submit_button.grid(row=14, column=12, columnspan=6, pady=10)

        # Check answer after button is pressed
        self.submit_button.bind("<Button-1>", lambda e: self.check_math_answer())
        self.submit_button.bind("<Enter>", lambda e: self.submit_button.config(bg="#e6ac06"))
        self.submit_button.bind("<Leave>", lambda e: self.submit_button.config(bg="#FFC107"))


    def setup_stroop_screen(self):
        # New dedicated screen for the Stroop test with color buttons
        self.stroop_frame.grid(row=0, column=0, rowspan=30, columnspan=30, sticky="nsew")
        self.stroop_frame.config(bg="white")
        self.stroop_frame.grid_remove()
        self.timer_label.lift()

        
        for i in range(30):  
            self.stroop_frame.columnconfigure(i, weight=1)
            self.stroop_frame.rowconfigure(i, weight=1)
        
        # Instruction label
        instruction_text = "Name the COLOR of the text, not the word itself."
        self.stroop_instruction = Label(self.stroop_frame, text=instruction_text, font=("Helvetica", 16), bg="white")
        self.stroop_instruction.grid(row=2, column=5, columnspan=20, pady=10)
        
        # Stroop test title
        self.stroop_title = Label(self.stroop_frame, text="Stroop Color Test", font=("Helvetica", 24, "bold"), bg="white")
        self.stroop_title.grid(row=4, column=5, columnspan=20, pady=10)
        
        # Stroop word display
        self.stroop_word = Label(self.stroop_frame, text="", font=("Helvetica", 72, "bold"), bg="white")
        self.stroop_word.grid(row=8, column=5, columnspan=20, pady=30)
        
        # Color buttons frame
        color_frame = Frame(self.stroop_frame, bg="white")
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
            # Hover effect
            def on_enter(e, widget=btn):
                widget.config(relief="sunken")

            def on_leave(e, widget=btn):
                widget.config(relief="flat")

            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)

            btn.grid(row=0, column=i, padx=5)
            self.color_buttons[color] = btn
        
        # Feedback label
        self.stroop_feedback = Label(self.stroop_frame, text="", font=("Helvetica", 16), bg="white")
        self.stroop_feedback.grid(row=18, column=5, columnspan=20, pady=10)


    #for robust user choice tracking
    def evaluate_moral_alignment(self, node, switched):
        # Determine which path the trolley ends up on after the decision
        final_track = self.current_track if not switched else ("top" if self.current_track == "bottom" else "bottom")
        killed_group = node.top if final_track == "top" else node.bottom

        def count_people(desc):
            if "nothing" in desc:
                return 0
            elif "you, your partner, and your child" in desc:
                return 3
            elif "world leaders" in desc or "Nobel" in desc or "philanthropists" in desc:
                return 31
            elif "assassin" in desc:
                return 1
            elif any(s in desc for s in ["doctors", "preschoolers", "friends"]):
                digits = [int(s) for s in desc.split() if s.isdigit()]
                return sum(digits) if digits else 5
            elif "bomb" in desc:
                return 8
            else:
                digits = [int(s) for s in desc.split() if s.isdigit()]
                return sum(digits) if digits else 1
        # Use these strings for moral evaluation
        killed_desc = node.top if final_track == "top" else node.bottom
        saved_desc = node.bottom if final_track == "top" else node.top
            
        killed_count = count_people(killed_desc)
        saved_count = count_people(saved_desc)

        if killed_count < saved_count:
            current_choice_type = "utilitarian"
        elif killed_count > saved_count:
            current_choice_type = "deontological"
        else:
            current_choice_type = "conflicted"
       


        # First scenario: no history, so we use this to set their initial alignment
        if self.last_choice_type is None:
            # First decision
            self.increment_moral_score(current_choice_type)
            self.last_choice_type = current_choice_type
        elif self.last_choice_type == current_choice_type:
            # Still consistent
            self.increment_moral_score(current_choice_type)
            self.last_choice_type = current_choice_type
        else:
            self.conflicted_score += 1

        print(f"[EVAL] Scenario {self.current_problem + 1}: {'Switched' if switched else 'Stayed'}")
        print(f"[EVAL] Type: {current_choice_type}, Previous: {self.last_choice_type}")
        print(f"[EVAL] U:{self.utilitarian_score}, D:{self.deontological_score}, C:{self.conflicted_score}")
        

        return killed_group, final_track

    
    def increment_moral_score(self, moral_type):
        if moral_type == "utilitarian": # Adds to utilitarianism
            self.utilitarian_score += 1
        elif moral_type == "deontological": # Adds to deontological
            self.deontological_score += 1
        else:
            self.conflicted_score += 1

    def decrement_moral_score(self, moral_type):
        if moral_type == "utilitarian" and self.utilitarian_score > 0:
            self.utilitarian_score -= 1
        elif moral_type == "deontological" and self.deontological_score > 0:
            self.deontological_score -= 1

    #shows the user a screen containing the choice they just made
    def setup_decision_screen(self):
        self.decision_frame.grid(row=0, column=0, rowspan=30, columnspan=30, sticky="nsew")
        self.decision_frame.grid_remove()

        for i in range(30):
            self.decision_frame.columnconfigure(i, weight=1)
            self.decision_frame.rowconfigure(i, weight=1)

        self.decision_label = Label(self.decision_frame, text="", font=("Helvetica", 20), bg="white", wraplength=900, justify="center")
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


        # Track history is visible
        self.track_history_label = Label(self.result_frame, text="Track Paths Taken:", font=("Helvetica", 14))
        self.track_history_label.grid(row=12, column=10, columnspan=10, pady=(20, 5))
        
        self.track_history_text = Text(self.result_frame, height=8, width=60, font=("Helvetica", 12))
        self.track_history_text.grid(row=13, column=10, columnspan=10)


        # Restart Label
        restart_label = Label(self.result_frame, text="Play Again", font=("Helvetica", 16),
                            bg="#a0fc8d", fg="black", padx=20, pady=10, cursor="hand2")
        restart_label.grid(row=15, column=13, columnspan=4, pady=10)
        restart_label.bind("<Button-1>", lambda e: self.restart_game())
        restart_label.bind("<Enter>", lambda e: restart_label.config(bg="#90e37a"))
        restart_label.bind("<Leave>", lambda e: restart_label.config(bg="#a0fc8d"))

        # Exit Label
        exit_label = Label(self.result_frame, text="Exit", font=("Helvetica", 16),
                   bg="#ff776d", fg="black", padx=20, pady=10, cursor="hand2")
        exit_label.grid(row=16, column=13, columnspan=4)
        exit_label.bind("<Button-1>", lambda e: self.root.quit())
        exit_label.bind("<Enter>", lambda e: exit_label.config(bg="#e4665d"))
        exit_label.bind("<Leave>", lambda e: exit_label.config(bg="#ff776d"))

    def show_start_screen(self):
        # Removes screens not needed
        self.problem_frame.grid_remove()
        self.math_frame.grid_remove()
        self.result_frame.grid_remove()
        self.start_frame.grid()
        self.timer_label.place_forget()


    def start_game(self):
        self.show_frame(self.problem_frame)
        # Restart scores when game restarts
        self.timer_label.place(relx=0.95, rely=0.02, anchor="ne")
        self.utilitarian_score = 0
        self.deontological_score = 0
        self.conflicted_score = 0
        self.current_problem = 0
        self.last_choice_type = None 
        self.current_track = "bottom"
        self.previous_track = None
        self.track_history = []
        self.load_problem()
        self.choices_enabled = False
        self.update_button_states(active=False)

    def load_problem(self):
        # Checks if there are still more problems to present
        if self.current_problem < len(self.track_nodes):
            #troubleshooting
            self.show_frame(self.problem_frame)
            self.timer_label.place(relx=0.95, rely=0.02, anchor="ne")
            self.timer_label.lift()

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
            # Get the flow-specific image from cache
            scenario_index = self.current_problem + 1
            image_key = f"SFTop{scenario_index}" if self.current_track == "top" else f"SFBottom{scenario_index}"
            image = self.flow_images.get(image_key)

            if image:
                self.problem_illustration.config(image=image)
                self.problem_illustration.image = image
                self.problem_illustration.update_idletasks() 
            else:
                print(f"Missing flow image: {image_key}")
                self.problem_illustration.config(image=None)

            self.track_status.config(text=f"You're currently on {self.current_track.upper()} track")

            self.choices_enabled = False
            self.update_button_states(active=False)
            self.enable_challenge_button()
            self.start_timer()

        else:
            print("No more problems. Showing results.")
            self.show_results()
            

    def show_results(self):
        # Stop timer from previous question
        if self.timer_id is not None:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None
         # Hide all other frames so nothing responds
        self.problem_frame.grid_remove()
        self.math_frame.grid_remove()
        self.stroop_frame.grid_remove()
        self.decision_frame.grid_remove()
        self.start_frame.grid_remove()

        self.result_frame.grid()
        self.result_frame.tkraise()

        print("Result screen displayed")

        #scan for if trolley exploded
        trolley_exploded = any(h.get("trolley_exploded", False) for h in self.track_history)

        # Scan for train_continues flag
        train_disaster = any(h.get("train_continues", False) for h in self.track_history)

        # Build summary text
        summary = f"Congratulations! You've completed all dilemmas. We've concluded you have questionable morals!\n\n"
        summary += f"Utilitarian choices: {self.utilitarian_score}\n"
        summary += f"Deontological choices: {self.deontological_score}\n"
        summary += f"Conflicted decisions: {self.conflicted_score}\n"

        if any(h.get("trolley_destroyed", False) for h in self.track_history):
            summary += (
            "\n\nAfter you exploded the trolley, everyone onboard — approximately 8 to 10 people — died in the explosion.\n"
            "However, the trolley could no longer harm anyone else remaining on the tracks.\n"
            )

        if trolley_exploded:
            summary += (
                "You prevented all remaining scenarios, saving:\n"
                "- Yourself, your partner, and your child\n"
                "- 10 world leaders, 10 Nobel Peace Prize winners, 10 philanthropists, and 1 infant\n"
                "- An assassin with three bullets (who may still try to kill you and your family — good luck!)"
            )

        if train_disaster:
            summary += (
                "\n\nAfter you died trying to spare the assassin, "
                "the trolley continued down the top track and killed over 30 people, including 10 world leaders, "
                "10 Nobel Peace Prize winners, 10 philanthropists, and 1 infant. Nice going."
            )

        elif self.utilitarian_score > self.deontological_score:
            summary += "\n\nYou lean utilitarian – you prioritize the greater good over individual rights."
        elif self.deontological_score > self.utilitarian_score:
            summary += "\n\nYou lean deontological – you respect moral duties over outcomes."
        else:
            summary += "\n\nYou're morally conflicted – or indecisive!"

        # Update result text and progress bar
        self.result_label.config(text=summary, bg="white", fg="black")
        self.progress_label.config(bg="white", fg="black")
        self.progress_canvas.config(bg="white", highlightbackground="black")

        self.track_history_label.config(bg="white", fg="black")
        self.track_history_text.config(bg="white", fg="black", insertbackground="black")  # insertbackground makes the cursor visible

        self.update_progress_bar()
        
        # Fill in the track history with user decisions
        self.track_history_text.delete(1.0, END)
        for i, history in enumerate(self.track_history):
            scenario = self.track_nodes[i]
            bottom_group = scenario.bottom
            top_group = scenario.top

            # Text structure
            if history.get("trolley_exploded"):
                history_text = (
                    f"Scenario {i+1}: The trolley was destroyed before reaching either track.\n"
                    "No one on the tracks was killed.\n"
                    "Casualties: everyone onboard the trolley (estimated 8–10 people).\n\n"
                )
            else:
                history_text = f"Scenario {i+1}: "
                history_text += f"Bottom track: {bottom_group}, Top track: {top_group}\n"
                history_text += f"Your choice: {'Switched' if history['switched'] else 'Stayed'} tracks\n"
                history_text += f"You killed: {history['killed']}\n\n"
            
            self.track_history_text.insert(END, history_text)


    def start_timer(self):
        if self.timer_id is not None:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None  

        self.time_left = 30
        self.update_timer()

    def update_timer(self):
        if self.current_problem >= len(self.track_nodes):
            return #removes timer if all problems are done
        
        if self.time_left <= 0:
            self.timer_label.config(text="Time: 0", fg="red", bg="white", font=("Helvetica", 18, "bold"))
            self.root.after(100, self.out_of_time)
            # Delay execution of out_of_time to allow UI update
            
            
        else: # Changer timer color when countdown from 10
            color = "red" if self.time_left <= 10 else "black"
            font = ("Helvetica", 18, "bold") if self.time_left <= 10 else ("Helvetica", 16)
            self.timer_label.config(text=f"Time: {self.time_left}", fg=color, bg="white", font=font)
            self.time_left -= 1
            self.timer_id = self.root.after(1000, self.update_timer)

    #if user runs out of time on choice
    def out_of_time(self):
        #Stops timer when time runs out
        if self.timer_id is not None:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None
        # Stops timer from resetting if all problems are done
        if self.current_problem >= len(self.track_nodes):
            return
    
        self.stroop_frame.grid_remove()
        self.math_frame.grid_remove()
        self.problem_frame.grid_remove()

        # Treat as default "stay"
        node = self.track_nodes[self.current_problem]

        killed_group, final_track = self.evaluate_moral_alignment(node, switched=False)

        self.track_history.append({
            "switched": False,
            "killed": killed_group,
            "red_path": node.red_path
        })

        self.show_decision_screen(False, killed_group, self.current_track)

    def make_choice(self, switch):
        if self.current_problem >= len(self.track_nodes):
            print("No more problems left. Ignoring choice.")
            return
        if self.timer_id:
            self.root.after_cancel(self.timer_id)

        node = self.track_nodes[self.current_problem]

        trolley_gone = any(h.get("trolley_destroyed", False) for h in self.track_history)

        if trolley_gone:
            killed_group = "nothing (the trolley was already destroyed)"
            final_track = self.current_track if not switch else (
                "top" if self.current_track == "bottom" else "bottom"
            )

            # still update moral score for trying to do something
            current_choice_type = "utilitarian" if switch else "deontological"
            self.increment_moral_score(current_choice_type)
    
            # Skip standard evaluation and jump to decision screen
            self.show_decision_screen(switch, killed_group, final_track)
            return



        # Evaluate choice BEFORE changing current track
        killed_group, final_track = self.evaluate_moral_alignment(node, switch)
        
        # Track the history of choices
        # update current/previous track
        if switch:
            self.previous_track = self.current_track
            self.current_track = "top" if self.current_track == "bottom" else "bottom"


        # Log the decision
        self.track_history.append({
            "switched": switch,
            "killed": killed_group,
            "red_path": node.red_path
        })

        print(f"Choice made: {'Switch' if switch else 'Stay'}")
        print(f"Killed: {killed_group}")
        print(f"Utilitarian: {self.utilitarian_score}, Deontological: {self.deontological_score}, Conflicted: {self.conflicted_score}")
        
        self.show_decision_screen(switch, killed_group, final_track)
         
    def show_decision_screen(self, switched, killed, final_track):
        # Hide other screens
        self.problem_frame.grid_remove()
        self.math_frame.grid_remove()
        self.timer_label.place_forget()
        self.stroop_frame.grid_remove()
    
        message = f"You {'switched tracks' if switched else 'stayed on the current track'}.\n"
        message += f"You killed: {killed}"
        self.decision_label.config(text=message)

        if self.current_problem == 5:
            node = self.track_nodes[self.current_problem]
            if killed == node.top:
                # The user switched to blow up the trolley
                self.show_bomb_ending()
                return

        # Scenario 7: Special handling if user kills the assassin (bottom group)
        if self.current_problem == 6:
            node = self.track_nodes[self.current_problem]
            if killed == node.bottom:
                # They killed the assassin
                image_key = "DFBottom7"

            elif killed == node.top:
                # They spared the assassin – go to dice roll
                self.handle_assassin_dice_roll()
                return
            else:
                image_key = f"DF{final_track.capitalize()}{self.current_problem + 1}"
        else:
            image_key = f"DF{final_track.capitalize()}{self.current_problem + 1}"

        # Figure out which image to show
        print(f"Image key requested: {image_key}")
        photo = self.decision_images.get(image_key)
        if photo:
            self.decision_frame.grid()
            self.decision_frame.tkraise() 
            self.decision_image.config(image=photo)
            self.decision_image.image = photo
            self.decision_image.update_idletasks()

        #next problem button
        if not (self.current_problem == 6 and killed == self.track_nodes[self.current_problem].top):
            self.continue_button = Label(self.decision_frame, text="Next Problem",
                font=("Helvetica", 16), bg="#7C83FD", fg="white",
                padx=15, pady=8, cursor="hand2")
            self.continue_button.grid(row=15, column=13, columnspan=4, pady=(30, 0))

            self.continue_button.bind("<Button-1>", lambda e: self.next_problem())
            self.continue_button.bind("<Enter>", lambda e: self.continue_button.config(bg="#5C62CC"))
            self.continue_button.bind("<Leave>", lambda e: self.continue_button.config(bg="#7C83FD"))

            # If we are currently on the LAST problem
            self.continue_button.config(
                text="Next Problem" if self.current_problem < len(self.track_nodes) - 1 else "See Results"
            )

    def next_problem(self):
        self.current_problem += 1
        if self.current_problem >= len(self.track_nodes):
            self.show_results() # Show results if no problems left
        else:
            self.show_frame(self.problem_frame)
            self.load_problem() # Show scenario and reset buttons and timer

    def return_to_problem(self):
        self.show_frame(self.problem_frame)
        self.choices_enabled = True
        self.update_button_states(active=True) # Sets buttons to active
        self.disable_challenge_button() # Disable task once it's done

        self.timer_label.place(relx=0.95, rely=0.02, anchor="ne")
        self.timer_label.lift() # sets it above other widgets

        # Refresh the frame
        self.problem_illustration.update_idletasks()
        self.problem_label.update_idletasks()
        self.problem_frame.update_idletasks()

    def show_math_challenge(self):
        #removes all frames
        self.problem_frame.grid_remove()
        self.stroop_frame.grid_remove()
        self.math_frame.grid()

        #randomly picks math question or stroop test for user
        task_type = random.choice(["math", "stroop"])
        self.current_task_type = task_type

        if task_type == "math": # Show math problem if chosen
            self.show_frame(self.math_frame)

            self.task_entry.delete(0, END)

            self.task_entry.focus_set()
            self.task_feedback.config(text="", fg="red", bg="white")
            self.task_type_label.config(text="Math Task", fg="blue", bg="white")

            problem = generate_random_math_problem()

            self.current_math_answer = problem["answer"]
            self.task_label.config(text=problem["question"], fg="black", bg="white")
            
            self.task_label.update_idletasks()
        else: # Stroop frame if stroop task is chosen
            self.show_frame(self.stroop_frame)

            self.stroop_feedback.config(text="",fg="red", bg="white")
            stroop = random.choice(self.stroop_tasks)
            self.current_stroop_answer = stroop["correct"]
            self.stroop_word.config(text=stroop["word"], fg=stroop["color"], bg="white")

        #puts timer back on top
        self.timer_label.place(relx=0.95, rely=0.02, anchor="ne")
        self.timer_label.lift()

    def check_math_answer(self):
        user_input = self.task_entry.get().strip()

        if self.current_task_type == "math":
            try:
                entered = int(user_input)
                if entered == self.current_math_answer:
                    self.complete_challenge() # Mark task as done if user answer matches actual answer
                else:
                    self.task_feedback.config(text="Incorrect. Try again.") 
                    self.task_feedback.config(bg="white", fg="red")
                    self.task_entry.delete(0, END) # Clears answer to allow retry
            except ValueError:
                self.task_feedback.config(text="Enter a valid number.")
                self.task_entry.delete(0, END) # Feedback if they type something other than a number
        else:
            if user_input.lower() == self.current_stroop_answer:
                self.complete_challenge() # Mark task as done if user answer matches actual answer
            else:
                self.task_feedback.config(text="Incorrect. Try again.")
                self.task_entry.delete(0, END) # Clears fields so user can retry


    def check_stroop_answer(self, selected_color):
        if selected_color == self.current_stroop_answer:
            self.return_to_problem()
        else:
            self.stroop_feedback.config(text="Wrong color. Try again.") #Feedback if answer is wrong

    def complete_challenge(self):
        # Return to problem after task
        self.math_frame.grid_remove()
        self.problem_frame.grid()
        self.choices_enabled = True

        #enable buttons
        self.choices_enabled = True
        self.update_button_states(active=True)

        #disable task button
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
        # Go back to start screen
        self.result_frame.grid_remove()
        self.current_problem = 0
        self.utilitarian_score = 0
        self.deontological_score = 0
        self.conflicted_score = 0
        self.track_history = []
        self.current_track = "bottom"
        self.previous_track = None
        self.last_choice_type = None
        if hasattr(self, 'continue_button') and self.continue_button.winfo_exists():
            self.continue_button.destroy()

        self.choices_enabled = False
        self.update_button_states(active=False)

        self.show_start_screen()
        self.root.update_idletasks()

    def show_bomb_ending(self):
        self.problem_frame.grid_remove()
        self.math_frame.grid_remove()
        self.stroop_frame.grid_remove()
        self.timer_label.place_forget()
        self.decision_frame.grid()
        self.decision_frame.tkraise()
        self.current_track = None  

        image_key = "DFTop6"  
        image = self.decision_images.get(image_key)

        if image:
            self.decision_image.config(image=image)
            self.decision_image.image = image
            self.decision_image.update_idletasks()
            self.decision_image.config(text="")  # Clear any fallback text
        else:
            print(f"Warning: DFTop6 image not found.")
            self.decision_image.config(text="The trolley exploded", font=("Helvetica", 24), bg="white")

        self.decision_label.config(
            text="You chose to switch tracks and destroy the trolley.\n\nNo one on the tracks was harmed.\n"
                "Everyone inside the trolley perished.",
            font=("Helvetica", 20), bg="white"
        )

        # add to score
        self.utilitarian_score += 1

        # Log this decision
        self.track_history.append({
            "switched": True,
            "killed": "everyone inside the trolley (estimated 8-10 people)",
            "red_path": True,
            "trolley_exploded": True,
            "trolley_destroyed": True
        })

        # Button now ends the game, not proceeds to the next scenario
        self.continue_button = Label(self.decision_frame, text="See Results",
            font=("Helvetica", 16), bg="#FF5252", fg="white",
            padx=15, pady=8, cursor="hand2")
        self.continue_button.grid(row=15, column=13, columnspan=4, pady=(30, 0))
        self.continue_button.bind("<Button-1>", lambda e: self.show_results())  # Go directly to final screen



    def handle_assassin_dice_roll(self):
        import random
        died = random.random() < 0.75  # 75% chance of death

        self.problem_frame.grid_remove()
        self.math_frame.grid_remove()
        self.stroop_frame.grid_remove()
        self.timer_label.place_forget()
        self.decision_frame.grid()
        self.decision_frame.tkraise()

        die_img = self.decision_images.get("DFTop7Die")
        live_img = self.decision_images.get("DFTop7Live")

        if not die_img or not live_img:
            print("Missing images for assassin animation.")
            self.decision_image.config(text="MISSING IMAGE", font=("Helvetica", 20))
            return
        
        def final_result():
            if died: 
                self.decision_image.config(image=die_img)
                self.decision_image.image = die_img
                self.track_history.append({
                    "switched": True,
                    "killed": "you, your partner, and your child",
                    "red_path": self.track_nodes[self.current_problem].red_path,
                    "train_continues": True  # we'll use this later
                })

                # Sad Game Over button
                self.continue_button = Label(
                    self.decision_frame, text="Face the Consequences",
                    font=("Helvetica", 16), bg="#FF5252", fg="white",
                    padx=15, pady=8, cursor="hand2"
                )
                self.continue_button.grid(row=15, column=13, columnspan=4, pady=(30, 0))
                self.continue_button.bind("<Button-1>", lambda e: self.show_results())
                #self.continue_button.bind("<Enter>", lambda e: self.continue_button.config(bg="#D32F2F"))
                #self.continue_button.bind("<Leave>", lambda e: self.continue_button.config(bg="#FF5252"))
                # Run flip animation, then show death result + button
            else:
                self.decision_image.config(image=live_img)
                self.decision_image.image = live_img
                self.track_history.append({
                    "switched": True,
                    "killed": "nothing (you miraculously survived)", # Mark that user survived
                    "red_path": self.track_nodes[self.current_problem].red_path
                })

                self.continue_button = Label(self.decision_frame, text="Next Problem",
                    font=("Helvetica", 16), bg="#7C83FD", fg="white",
                    padx=15, pady=8, cursor="hand2"
                )
                self.continue_button.grid(row=15, column=13, columnspan=4, pady=(30, 0))
                # Sets up the next problem
                self.continue_button.bind("<Button-1>", lambda e: self.next_problem())
                #self.continue_button.bind("<Enter>", lambda e: self.continue_button.config(bg="#5C62CC"))
                #self.continue_button.bind("<Leave>", lambda e: self.continue_button.config(bg="#7C83FD"))


        def flip_animation():
            imgs = [live_img, die_img]
            i = 0

            def next_frame():
                nonlocal i
                self.decision_image.config(image=imgs[i % 2])
                i += 1
                if i < 10:
                    self.root.after(100, next_frame)
                else:
                    final_result()

            next_frame()

        # Run flip animation before results
        flip_animation()
        
        
if __name__ == "__main__":
    root = Tk()
    game = TrolleyGame(root)
    root.mainloop()