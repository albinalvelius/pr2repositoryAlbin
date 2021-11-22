import tkinter as tk
from tkinter.constants import ANCHOR
x = tk.Tk()
c = tk.Canvas(x, height=720, width=1280)
c.pack()

filename = tk.PhotoImage(file = "bowsimulator/bow1.png")
c.create_image(50, 50, image=filename)

x.mainloop()