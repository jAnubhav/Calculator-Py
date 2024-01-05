from tkinter import Tk, PhotoImage, Frame, Label, Button
from json import load

class Calc(Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Calc")
        icon = PhotoImage(file="icon.png")
        self.iconphoto(False, icon)
        self.config(bg=Calc.colors["bg"], padx=5, pady=5)
        self.resizable(False, False)

        cons, np_cons = list(), list()

        for i in range(2):
            cons.append(PackFrame(self, pad=5))
            cons[i] = PackFrame(cons[i], pad=10)

        self.label = Label(cons[0], text="0", width=21, bg=Calc.colors["calc"], fg=Calc.colors["white"], font=("Bahnscrift", 16, "bold"), anchor="e")
        self.label.pack()

        for i in range(3):
            np_cons.append(GridFrame(cons[1], row=i//2, column=i%2, columnspan=i//2+1))

        for i, e in enumerate("789456123.0"):
            HoverButton(self, np_cons[0], row=i//3, column=i%3, char=e, bg=Calc.colors["numbers"], activebg=Calc.colors["numbers-dark"])

        for i, e in enumerate("/*-+"):
            HoverButton(self, np_cons[1], row=i, column=0, char=e, bg=Calc.colors["operators"], activebg=Calc.colors["operators-dark"])

        for i, e in enumerate(["AC", "DEL"]):
            HoverButton(self, np_cons[2], row=0, column=i, char=e, bg=Calc.colors["clearings"], activebg=Calc.colors["clearings-dark"], fg=Calc.colors["white"], width=10)

        HoverButton(self, np_cons[0], row=3, column=2, char="=", bg=Calc.colors["equals"], activebg=Calc.colors["equals-dark"])

    @staticmethod
    def checkOperator(char:str) -> bool:
        return char in "+-*/"
    
    def getText(self) -> str:
        return self.label["text"]
    
    def newText(self, text:str) -> None:
        self.label["text"] = text

    def addText(self, text:str) -> None:
        self.label["text"] += text

    def replaceChar(self, char:str="") -> None:
        self.newText(self.getText()[:-1:] + char)
    
    def delText(self) -> None:
        self.newText("0") if (len(self.getText()) == 0) else self.replaceChar()

    def findResult(self) -> None:
        try:
            self.newText(str(round(eval(self.getText()), 6)))
        except:
            self.newText("Error")

    def addinLabel(self, char:str) -> None:
        if (char == "AC"): self.newText("0")
        elif (char == "DEL"): self.delText()
        elif (char == "="): self.findResult()
        elif (self.getText() in ["0", "Error"]):
            if (not(Calc.checkOperator(char))): self.newText(char)
        elif (Calc.checkOperator(char) and Calc.checkOperator(self.getText()[-1])): self.replaceChar(char)
        else: self.addText(char)

    with open("colors.json", "r") as f:
        colors = load(f)

class PackFrame(Frame):
    def __init__(self, master:Tk | Frame, pad:int) -> None:
        super().__init__(master=master, bg=Calc.colors["calc"])
        self.pack(padx=pad, pady=pad)
    
class GridFrame(Frame):
    def __init__(self, master:Frame, row:int, column:int, columnspan:int) -> None:
        super().__init__(master=master, bg=Calc.colors["calc"])
        self.grid(row=row, column=column, columnspan=columnspan)

class HoverButton(Button):
    def __init__(self, parent, master:Frame, row:int, column:int, char:str, bg:str, activebg:str, fg="black", width=4) -> None:
        super().__init__(master=master, text=char, width=width, bg=bg, fg=fg, activebackground=activebg, font=("Bahnscrift", 14, "bold"), relief="flat", bd=0, cursor="hand2", command=lambda: parent.addinLabel(char))
        self.defaultBg = self["bg"]
        self.bind("<Enter>", self.onEnter)
        self.bind("<Leave>", self.onLeave)
        self.grid(row=row, column=column, padx=5, pady=5, ipadx=2, ipady=2)

    def onEnter(self, _) -> None:
        self.config(bg=self["activebackground"])
    
    def onLeave(self, _)-> None:
        self.config(bg=self.defaultBg)

if __name__ == "__main__":
    app = Calc()
    app.mainloop()