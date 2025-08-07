from tkinter import *
from tkinter import ttk, Tk
import scrapper

# Call when using input to remore placeholder
def inputClick(*args):
    if ingredientInput.get() == "Example: beef,corn":
        ingredientInput.delete(0, 'end')

# Call when leaving input to regain focus
def inputLeave(*args):
    frame.focus()

def inputSubmit(*args):
    global recipeList
    global recipeIndex

    recipeIndex = 0

    urlList = scrapper.GetUrls(ingredientInput.get())
    recipeList = scrapper.GetRecipe(urlList)

    displayRecipe(recipeList, recipeIndex)

def displayRecipe(recipeList, recipeIndex):

    # FORMAT
    # URL
    # Recipe Name
    # Ingredients

    recipes.delete("1.0", "end")
    recipes.insert("1.0","URL: " + recipeList[recipeIndex][0] + "\n" +
                   "+----------------------------------------------------------+" + "\n" +
                   "Recipe: " + recipeList[recipeIndex][1] + "\n" +
                   "+----------------------------------------------------------+" + "\n" +
                   "Ingredients:" + "\n")
    
    for ingredient in recipeList[recipeIndex][2]:
        recipes.insert("end", "- " + ingredient + "\n")

def previousClick(*args):
    global recipeIndex
    
    if recipeIndex != 0:
        recipeIndex = recipeIndex - 1
        displayRecipe(recipeList, recipeIndex)
    
def nextClick(*args):
    global recipeIndex
    if (recipeIndex + 1) != len(recipeList):
        recipeIndex = recipeIndex + 1
        displayRecipe(recipeList, recipeIndex)


# Colors
frameColor = "#657153"
btnColor = "#8AAA79"
btnActiveColor="#7DA06A"
textBackground = "#D1D5DE"
inactiveBtn = "#B7B6C2"

root = Tk()
# root.geometry("504x537")
root.configure(bg=frameColor)
root.title("Recipe Generator")
s = ttk.Style()
s.configure('custom.TFrame', background=frameColor)
frame = ttk.Frame(root, style='custom.TFrame')
frame.grid(padx=10)
frame.columnconfigure(0, weight=1)
frame.columnconfigure(1, weight=0)
frame.columnconfigure(2, weight=1)
frame.columnconfigure(3, weight=0)
frame.columnconfigure(4, weight=1)

# Label for explaining program
Label(frame, text="Enter your ingredient list below in a ',' seperated list:", bg=frameColor).grid(column=1, row=0, columnspan=3)

# Setup ingredient input for user input
ingredientInput = Entry(frame, width=55, bg=textBackground)
ingredientInput.insert(0, 'Example: beef,corn')
ingredientInput.grid(column=1, row=2, pady=10, sticky="w")

# Bind cursor to functions above for user input
ingredientInput.bind("<Button-1>", inputClick)
ingredientInput.bind("<Leave>", inputLeave)

# Text area for displaying recipes
recipes = Text(frame, width=60, height=25, bg=textBackground)
recipes.grid(column=1, row=3, columnspan=3, pady=10)
# Previous and next btns to cycle through recipes

previous = Button(frame, width=15, text="Previous", command=previousClick, bg=btnColor, activebackground=btnActiveColor).grid(column=1, row=4, pady=10, sticky="w")
next = Button(frame, width=15, text="Next", command=nextClick, bg=btnColor, activebackground=btnActiveColor).grid(column=3, row=4, pady=10, sticky="e")

# Submit btn for entering ingredient list
submit = Button(frame, width=15, text="Get Recipe", command=inputSubmit, bg=btnColor, activebackground=btnActiveColor).grid(column=3, row=2, pady=10, sticky="e")

root.update()
root.mainloop()
