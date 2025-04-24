from tkinter import*

root = Tk()
root.title("The Trolley Problem")
root.attributes('-fullscreen', True)


my_label = Label(root, text = "Hello World!", font = ("Helvetica", 24))
#Pack(puts on top, packs below), Grid(Rows and columns), and Place(specify coordinates)

my_label.pack(pady=20)

my_button= Button(root, text = "Click Me!", font = ("Helvetica", 20))
my_button.pack(pady=20)


root.mainloop()
