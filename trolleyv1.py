from tkinter import*

root = Tk()
root.title("The Trolley Problem")
root.attributes('-fullscreen', True)

for i in range(20):  
    root.columnconfigure(i, weight=1)
    root.rowconfigure(i, weight=1)

def hide():
    start_button.grid_forget()

title_label = Label(root, text = "Hello World!", font = ("Helvetica", 24))
title_label.grid(row=2, column=7)

start_button= Button(root, text = "Click Me!", font = ("Helvetica", 20), command=hide)
start_button.grid(row=8, column=5)

exit_button = Button(root, text="Exit Fullscreen", font=("Helvetica", 16), command=lambda: root.attributes('-fullscreen', False))
exit_button.grid(row=25, column=7)

# Allow Escape key to exit fullscreen
root.bind("<Escape>", lambda event: root.attributes('-fullscreen', False))

root.mainloop()
