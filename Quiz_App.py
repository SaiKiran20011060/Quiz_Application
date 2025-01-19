import tkinter
from tkinter import *
import random

questions = [
    "r = lambda q: q * 2\ns = lambda q: q * 3\nx = 2\nx = r(x)\nx = s(x)\nx = r(x)\nprint x",
    "a = True\nb = False\nc = False\n\nif a or b and c:\n    print \"Dr.SUKHVIR KAUR MAM\"\nelse:\n    print \"Dr.Sukhvir Kaur mam\"",
    "count = 1\n\ndef doThis():\n    global count\n    for i in (1, 2, 3):\n        count += 1\ndoThis()\nprint count",
    "Which of The Following is must to Execute a Python Code?",
    "from random import randrange\nL = list()\nfor x in range(5):\n    L.append(randrange(0, 100, 2)-10)\n\n# Choose which of outputs below are valid for this code.\n\nprint(L)",
    "The output of executing string.ascii_letters can also be achieved by:",
    "If a=(1,2,3,4), a[1:-1] is _________",
    "Which of the following statements create a dictionary?",
    "Which module in the python standard library parses options received from the command line?",
    "To Declare a Global variable in python we use the keyword?",
]

answers_choice = [
    ["A) 23", "B) 24", "C) 25", "D) 32"],
    ["A) Dr.Sukhvir Kaur mam", "B) Dr.SUKHVIR KAUR MAM", "C) Syntax Error", "D) Both A and B"],
    ["A) 2", "B) 3", "C) 4", "D) 5"],
    ["A) TURBO C", "B) Py Interpreter", "C) Notepad", "D) IDE"],
    ["A) [-8, 88, 8, 58, 0]", "B) [-8, 81, 18, 46, 0]", "C) [-7, 88, 8, 58, 0]", "D) [-8, 88, 94, 58, 0]"],
    ["A) string.ascii_lowercase_string.digits", "B) string.ascii_lowercase+string.ascii_uppercase", "C) string.letters", "D) string.lowercase_string.uppercase"],
    ["A) Error, tuple slicing doesn’t exist", "B) [2,3]", "C) (2,3,4)", "D) (2,3)"],
    ["A) d = {}", "B) d = {“john”:40, “peter”:45}", "C) d = {40:”john”, 45:”peter”}", "D) All of the mentioned"],
    ["A) main", "B) os", "C) getarg", "D) getopt"],
    ["A) all", "B) var", "C) let", "D) global"],
]

answers = [1, 1, 2, 1, 3, 1, 3, 3, 0, 3]
user_answer = []
indexes = []

def gen():
    global indexes
    while len(indexes) < 10:
        x = random.randint(0, 9)
        if x not in indexes:
            indexes.append(x)

def showresult(score):
    lblQuestion.destroy()
    r1.destroy()
    r2.destroy()
    r3.destroy()
    r4.destroy()
    
    labelresulttext = Label(
        root,
        font=("Consolas", 20),
        background="#1A1A1D",
        fg="#FACA2F"
    )
    labelresulttext.pack(pady=(200, 30))
    
    labelresult1text = Label(
        root,
        font=("Consolas", 20),
        background="#1A1A1D",
        fg="#FACA2F"
    )
    labelresult1text.pack(pady=(30, 0))
    
    labelresult2text = Label(
        root,
        font=("Consolas", 20),
        background="#1A1A1D",
        fg="#FACA2F"
    )
    labelresult2text.pack()
    
    if score == 30:
        labelresulttext.configure(text="YOU ARE OUTSTANDING")
    elif score >= 24:
        labelresulttext.configure(text="You Are Excellent !!")
    elif 13 <= score < 24:
        labelresulttext.configure(text="You Can Be Better !!")
    else:
        labelresulttext.configure(text="You Should Work Hard !!")
    
    labelresult1text.configure(text="Your Score out of 30:")
    labelresult2text.configure(text=score)
    print("score =", score)

def calc():
    global indexes, user_answer, answers
    x = 0
    score = 0
    for i in indexes:
        if user_answer[x] == answers[i]:
            score += 3
        x += 1
    print(score)
    showresult(score)

ques = 1
def selected():
    global radiovar, user_answer
    global lblQuestion, r1, r2, r3, r4
    global ques
    x = radiovar.get()
    user_answer.append(x)
    radiovar.set(-1)
    
    if ques < 10:
        lblQuestion.config(text=questions[indexes[ques]])
        r1['text'] = answers_choice[indexes[ques]][0]
        r2['text'] = answers_choice[indexes[ques]][1]
        r3['text'] = answers_choice[indexes[ques]][2]
        r4['text'] = answers_choice[indexes[ques]][3]
        ques += 1
    else:
        print(indexes)
        print(user_answer)
        calc()

def startquiz():
    global lblQuestion, r1, r2, r3, r4
    lblQuestion = Label(
        root,
        text=questions[indexes[0]],
        font=("Consolas", 16),
        width=500,
        justify="left",
        wraplength=400,
        background="#1A1A1D",
        fg="#C3073F",
    )
    lblQuestion.pack(pady=(50, 30))

    global radiovar
    radiovar = IntVar()
    radiovar.set(-1)

    r1 = Radiobutton(
        root,
        text=answers_choice[indexes[0]][0],
        font=("Times", 12),
        value=0,
        variable=radiovar,
        command=selected,
        background="#1A1A1D",
        fg="white",
    )
    r1.pack(pady=5)

    r2 = Radiobutton(
        root,
        text=answers_choice[indexes[0]][1],
        font=("Times", 12),
        value=1,
        variable=radiovar,
        command=selected,
        background="#1A1A1D",
        fg="white",
    )
    r2.pack(pady=5)

    r3 = Radiobutton(
        root,
        text=answers_choice[indexes[0]][2],
        font=("Times", 12),
        value=2,
        variable=radiovar,
        command=selected,
        background="#1A1A1D",
        fg="white",
        justify="left",
    )
    r3.pack(pady=5)

    r4 = Radiobutton(
        root,
        text=answers_choice[indexes[0]][3],
        font=("Times", 12),
        value=3,
        variable=radiovar,
        command=selected,
        background="#1A1A1D",
        fg="white",
        justify="left",
    )
    r4.pack(pady=5)

def startIspressed():
    labeltext.destroy()
    lblInstruction.destroy()
    lblInstruction1.destroy()
    lblRules.destroy()
    btnStart.destroy()
    gen()
    startquiz()

root = tkinter.Tk()
root.title("Quizrocks")
root.geometry("700x600")
root.config(background="#1A1A1D")
root.resizable(0, 0)

labeltext = Label(
    root,
    text="QUIZ",
    font=("Comic sans MS", 40, "bold"),
    background="#1A1A1D",
    fg="#C3073F"
)
labeltext.pack(pady=(0, 50))

btnStart = Button(
    root,
    text="START",
    relief=FLAT,
    font=("Fraktur Font", 15, "bold"),
    border=0,
    bg="#6F2232",
    fg="white",
    command=startIspressed,
)
btnStart.pack(pady=80)

lblInstruction = Label(
    root,
    text="Read The Rule and know about The Quiz.\n",
    background="#1A1A1D",
    fg="#C3073F",
    font=("Consolas", 14),
    justify="center",
)
lblInstruction.pack(pady=(10, 30))

lblRules = Label(
    root,
    text="There are 10 Questions.\nMust and should attempt every Question.\nNo negative marks\nOnly one answer for one question\nJust click one option to attempt the question.",
    width=100,
    font=("Times", 14),
    background="#4E4E50",
    foreground="#FACA2F",
)
lblRules.pack()

lblInstruction1 = Label(
    root,
    text="Click Start once you read the Rules !!\n",
    background="#1A1A1D",
    fg="#C3073F",
    font=("Consolas", 14),
    justify="center",
)
lblInstruction1.pack(pady=(10, 30))

root.mainloop()