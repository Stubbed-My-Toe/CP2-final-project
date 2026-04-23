import tkinter as tk

root = tk.Tk()
root.title("Testing")
root.configure(background="orange")
root.minsize(250, 250)
root.maxsize(1000,1000)
#set the start size
root.geometry("300x300+700+100")
label = tk.Label(root, text="This is curently working!", font=("Times New Roman", 14, "bold"))
label.config(fg ="blue", background = "orange")

#image = tk.PhotoImage(file = "img\\image.png")
#tk.Label(root, image = image)

#stuff about button
root.count = 0
def add():
    root.count += 1
    num["text"] = root.count

btn = tk.Button(root, text="ADD", command=add)
btn.pack()
num = tk.Label(root, text = "0")
num.pack()
label.pack()
root.mainloop()