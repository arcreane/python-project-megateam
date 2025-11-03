from tkinter import *

fenetre = Tk()
fenetre.title("ATC")
fenetre.configure(bg="black")

fenetre.attributes("-fullscreen", True)


fenetre.bind("<Escape>", lambda e: fenetre.attributes("-fullscreen", False))

label = Label(fenetre, text="Hello World", bg="black", fg="white", font=("Arial", 24))
label.pack(expand=True)

fenetre.mainloop()