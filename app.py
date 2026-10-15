import tkinter as tk
from tkinter import *
from tkinter import ttk
import mathgenerator as mg
import random
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# initalize arrays and values 
random_title, random_num, random_problem, problem, text_problem, text_solution, rounded_solution = "", 0, 0, "", "", "", 0
alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
trig = ["sin", "cos", "tan", "csc", "cot", "sec"]
numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "."]
operations = ["-", "+", "*", "/", "cdot"]
special_characters = [",", " "]

"""
notes:
use enum for random_problem stuff
if code can self-document, don't comment about it
make sure you're clear about global variable changes 
"""

"""
Function: generate_problem()
Description: generates a random problem using the mathgenerator library
Returns a random problem's title, number, problem, and solution
"""
def generate_problem():
    random_problem = random.randint(0, len(calculus_problems) - 1)
    random_title = calculus_names[random_problem]
    problem, solution = calculus_problems[random_problem]()

    # for debugging
    print(problem, " SOMETHING ", solution)

    return random_title, random_problem, problem, solution

"""
Function: new_problem()
Description: generates a new problem and edits labels to reflect the newly 
    generated problem. Sets values afterwards for the user checking answers
"""
def new_problem(event=None):
    random_title, random_problem_value, problem, new_solution = generate_problem()    

    # for debugging purposes
    print(new_solution)

    label_title.config(text=random_title)
    if not disabled.get(): 
        label_solution.config(text=new_solution[1:-1])
    graph_problem(problem_wx, problem)
    solution.set(new_solution)
    random_problem.set(random_problem_value)
    correct_or_not.config(text="Press 'Check Solution'")

"""
Function: process_text()
Description: Goes through user input to properly display on canvas and so 
    program can match user input with raw solution answer.
Returns: processed string to display on the canvas + compare with solution string 
"""
def process_text(tmptxt):
    # if text doesn't exist, return empty string
    if not tmptxt:
        return ""

    # if text doesn't have space at the end, add one so input processing works
    if tmptxt[-1] != " ":
        tmptxt += " "

    # initalize empty string that will contain final processed string 
    new_text = ""

    # for debugging
    print(tmptxt)

    # set a separate string variable to be tmptxt since strings being iterated through 
    # are immutable
    updated_text = tmptxt

    # set loop so updated_text and tmptxt can match if offset
    loop = 0

    # for loop that goes through each char and evaluates what to do depending on what character is found.
    # updated text is slowly split each iteration until it has reached the end, and is why its called updated_text.
    for char in tmptxt:
        # for debugging purposes
        print("\n--- LOOP")
        
        # if the character is a space and is the only string left, stop looping
        if char == " " and len(tmptxt) == 1:
            break
        # if the updated text is offset from the temptext in the loop, continue to the next character until 
        # either tmptxt reached the end or has caught back up with updated_text  
        if len(updated_text) != len(tmptxt[loop:]):
            # for debugging purposes
            print("--- SKIP")
            print("tmp:" + tmptxt)
            print("updated: " + updated_text)
            print("new: " + new_text)

            loop += 1
            continue

        # for debugging purposes
        print(char)

        # for arithmetic operations
        if char in operations:
            # for debugging purposes
            print("--- Operation 1")
            new_text += char
            if random_problem.get() == 3 and char == "-" and len(updated_text) > 2 and updated_text[1] == "(":
                new_text += " "
            updated_text = updated_text[1:]

        # for showing the dot multiplication symbol
        elif updated_text[:4] == "cdot":
            # for debugging purposes
            print("--- Operation 2")
            new_text += " \\cdot"
            updated_text = updated_text[4:]

        # for  whole number coefficients    
        elif char in numbers:
            # for debugging purposes
            print("--- Whole Numbers")

            # set length of number to be 0
            length = 0

            # loop through updated_text until a non number character has been found
            for number in updated_text:
                if number not in numbers:
                    break
                new_text += number
                length += 1
            updated_text = updated_text[length:]
        
        # for fractional coefficients and coordinates (for stationary points a.k.a where dx = 0)
        elif char == "(":
            # for debugging purposes
            print("--- Fractions") 

            # track opening parenthesis 
            open = updated_text.find("(")

            # counter to keep track of how far into the string and how many parenthesis have been encountered
            counter = 0
            open_parenthesis_stack = 0

            # if no close parenthesis exists, return 
            if updated_text.find(")") == -1:
                return "ERROR: NO PARENTHESIS"

            # iterate through the string until the right closing parenthesis has been found
            while True:
                if updated_text[counter+1] == ")":
                    if open_parenthesis_stack == 0:
                        break
                    else:
                        open_parenthesis_stack -= 1
                elif updated_text[counter+1] == "(":
                    open_parenthesis_stack += 1
                counter += 1

            # track division symbol and close symbol  
            divison_symbol = updated_text.find("/")
            close = counter + 1

            # if division symbol exists, process the numerator and denominator
            if divison_symbol != -1:
                number1 = updated_text[open+1:divison_symbol]
                number2 = updated_text[divison_symbol+1:close]

                # if there is a square root, format new string to have square root
                if (number1.find("sqrt") != -1):
                    if (number1.find("sqrt") == 0):
                        number1 = "\\sqrt{" + number1[number1.find("(")+1:number1.find(")")] + "}"
                    else:
                        number1 = number1[0:number1.find("s")].strip() + " \\sqrt{" + number1[number1.find("(")+1:number1.find(")")] + "}"
                    #number2 = number2[:-2]
                elif (number2.find("sqrt") != -1):
                    if (number2.find("sqrt") == 0):
                        number2 = "\\sqrt{" + number2[number2.find("(")+1:number2.find(")")] + "}"
                    else:
                        number2 = number2[0:number2.find("s")].strip() + " \\sqrt{" + number2[number2.find("(")+1:number2.find(")")] + "}"

                new_text += "\\frac{" + number1 + "}" + "{" + number2 + "}"
            # if there is no division symbol, add whatever is inside of the parenthesis into the new string
            else:
                new_text += updated_text[open+1:close]

            # update the text to remove anything in the parenthesis
            updated_text = updated_text[close+1:]
        
        # for trig functions
        elif updated_text[0:3] in trig:
            # for debugging purposes
            print("--- Trig")
            
            # a series of if statements to determine what trig function was found
            if updated_text[0] == "s":
                if updated_text[1] == "i":
                    new_text += "\\sin"
                else:
                    new_text += "\\sec"
            elif updated_text[0] == "c":
                if updated_text[2] == "s":
                    new_text += "\\cos"                    
                elif updated_text[2] == "c":
                    new_text += "\\csc"
                else:
                    new_text += "\\cot"
            else:
                new_text += "\\tan"

            # remove trig function from updated text
            updated_text = updated_text[3:]

            # if trig function has exponent, add exponent to the string
            if updated_text[0] == "^":
                new_text += "^{{" + updated_text[1:updated_text.find(" ")] + "}}"

            # update text to remove trig function from processing
            updated_text = updated_text[updated_text.find(" ")+1:]

            # for debugging purposes
            print("TEMP" + tmptxt + "TEMP")
            print(new_text)

        # for variables 
        elif char in alphabet:
            # for debugging purposes
            print("--- Variable")
            print(tmptxt)
            
            # if variable has an exponent attached to it, add it to the new string
            if updated_text[1] == "^":
                new_text += updated_text[0] + "^{" + updated_text[2:updated_text.find(" ")] + "}"
                updated_text = updated_text[updated_text.find(" "):]
            # otherwise, add the variable to the new string
            else:
                new_text += updated_text[0]
                updated_text = updated_text[1:]

            # for debugging purposes
            print(updated_text)
        
        # if the character is a space and so is the updated text, break
        elif char == " " and updated_text == " ":
            break

        # if the character is a special character and there exists more text to process, add special character
        elif char in special_characters and updated_text[1]:
            new_text += special_characters[special_characters.index(char)]
            updated_text = updated_text[1:]

        # if character does not work at all, return an error
        else:
            # for debugging purposes
            print("NO GOOD")
            return "ERROR"

        # add 1 to the loop counter so we can track iteration progress
        loop += 1

    # if its a stationary point problem, wrap the final text in brackets
    if random_problem.get() == 3:
        new_text = "{" + new_text + "}"

    # for debugging purposes
    print(new_text)

    return new_text

"""
Function: check_solution()
Description: Checks the user's input if it is the correct answer or not
    Displays if it is correct or wrong depending on answer comparison
"""
def check_solution():
    # get user input and process text
    user_solution = "$" + process_text(user_entry.get()) + "$"
    
    # for debugging purposes
    print(user_solution)
    print(solution.get())

    # if the user inputted the correct solution, display that they got it right
    if user_solution == solution.get():
        correct_or_not.config(text="CORRECT")
    # otherwise, display that they got it wrong
    else:
        correct_or_not.config(text="WRONG")

"""
Function: toggle_solution()
Description: Toggle the solution for the user to see/not see
"""
def toggle_solution(event=None):

    # if solution is disabled, toggle state to False and show answer
    if (disabled.get()):
        # for debugging purposes
        print("disabled")
        
        label_solution.config(text=solution.get()[1:-1])
        label_solution.config(state=tk.NORMAL)
        label_solution.config(background="#FFFFFF")
        disabled.set(False)

    # otherwise, toggle state to True and hide answer
    else: 
        # for debugging purposes
        print("enabled")
        
        label_solution.config(text=" ")
        label_solution.config(state=tk.DISABLED)
        label_solution.config(background="#111111")
        disabled.set(True)

"""
Function: graph()
Description: graphs the user's input onto a canvas
"""
def graph(event=None):
    # Get the Entry Input
    tmptext = user_entry.get()

    tmptext = process_text(tmptext)

    if tmptext:  # Only process if there's text
        tmptext = "$" + tmptext + "$"
        # Clear any previous Syntax from the figure
        wx.clear()
        try:
            wx.text(0.1, 0.6, tmptext, fontsize=20)
        except:
            # If LaTeX rendering fails, show the raw text
            wx.text(0.2, 0.6, "Invalid LaTeX syntax", fontsize=16, color='red')
        canvas.draw()

"""
Function: graph_problem()
Description: graphs the randomly generated problem onto a canvas 
"""
def graph_problem(problem_wx, problem):
    # Get the Entry Input
    ptext = problem
    if ptext:  # Only process if there's text
        # Clear any previous Syntax from the figure
        problem_wx.clear()
        try:
            problem_wx.text(.1, .15, ptext, fontsize=15, wrap=True)
        except:
            # If LaTeX rendering fails, show the raw text
            problem_wx.text(0.2, 0.6, "Invalid LaTeX syntax", fontsize=16, color='red')
        problem_canvas.draw()


# initalize root and define root values
matplotlib.use('TkAgg')
root = tk.Tk()
root.title("MATH_HEAVEN")
root.geometry("1920x1080")
root.state('zoomed')
root.config(bg="#111111")

# initalize calculus arrays
calculus_problems = [mg.definite_integral, mg.power_rule_differentiation, mg.power_rule_integration, mg.stationary_points, mg.trig_differentiation]
calculus_names = ["integral", "power rule differentiation", "power rule integration", "stationary points", "trig differentiation"]

# generate an inital random problem and store values
random_title, random_problem_value, problem, generated_solution = generate_problem()
solution = tk.StringVar(value=generated_solution)
random_problem = tk.IntVar(value=random_problem_value)
disabled = tk.BooleanVar(value=True)

# create problem title 
calculus_title = tk.Label(root, text=calculus_names[random_problem.get()], font=("Arial", 14))
label_title = tk.Label(root, text=random_title, font=("Arial", 14))
label_title.pack(pady=20)

# create label for canvas
label = tk.Label(root, justify="center", anchor="center", font=("Arial", 10))
label.pack(pady=10)

# create canvas to show problem on and display problem
problem_figure = matplotlib.figure.Figure(figsize=(15, 1), dpi=100)
problem_wx = problem_figure.add_subplot(111)
problem_canvas = FigureCanvasTkAgg(problem_figure, master=label)
problem_canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
problem_canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=1)
problem_wx.get_xaxis().set_visible(False)
problem_wx.get_yaxis().set_visible(False)
graph_problem(problem_wx, problem)

# create label for solution displaying
label_solution = tk.Label(root, background="#111111", font=("Arial", 14), state=tk.DISABLED)
label_solution.pack(pady=20)

# create label to show user if they got the right answer or not
correct_or_not = tk.Label(root, justify="center", text="Press 'Check Solution' first to see answer", font=("Arial", 10))
correct_or_not.pack(pady=20)

# entry widget for user to input
user_entry = tk.Entry(root, width=30)
user_entry.insert(0, "Type your answer here")
user_entry.pack(pady=5)

# create a frame for problem canvas
frame = Frame(root)
frame.pack()

# create label inside of the frame
display_box = Label(frame)
display_box.pack()

# create canvas inside of the frame
figure = matplotlib.figure.Figure(figsize=(7, 2), dpi=100)
wx=figure.add_subplot(111)
canvas = FigureCanvasTkAgg(figure, master=display_box)
canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=1)
wx.get_xaxis().set_visible(False)
wx.get_yaxis().set_visible(False)

# bind graphing function with return key
root.bind('<Return>', graph)

# create buttons to check solution, get new problem, and view solution for current problem
check_solution_button = tk.Button(root, text="Check Solution", command=check_solution)
new_problem_button = tk.Button(root, text="Get New Problem", command=new_problem)
view_solution_button = tk.Button(root, text="Toggle viewing solution (Raw Data Form)", command=toggle_solution)
check_solution_button.pack(pady=10)
new_problem_button.pack(pady=10)
view_solution_button.pack(pady=10)

root.mainloop()