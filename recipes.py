"""
This is recipe finder.
1. Enter a few different ingredients, such as: chicken, pasta, parsely.
2. It will search for food recipes that include all three ingredients.
3. Return the recipe.
API KEY: 7f88e49e59794017accb3bf033e53f07
"""
import tkinter as tk
import tkinter.font as font
import spoonacular as sp

api = sp.API("7f88e49e59794017accb3bf033e53f07")

# globally declare the expression variable
expression = ""


def askForIngredients():
    field1.configure(state='normal')
    field2.insert(0, 'Please type any ingredients you have!')


def foodJokes():
    field2.configure(state='normal')
    # response = api.get_a_random_food_joke()
    # data = response.json()
    # field2.insert(0, data['text'])
    field2.insert("end", "HAHA SO FUNNY")


def searchIngredients(ingredients):
    field2.configure(state='normal')

    # Get recipes ID for the ingredients
    ingResponse = api.search_recipes_by_ingredients(ingredients)
    ingData = ingResponse.json()
    recipeID = ingData[0]['id']

    # Search for the recipe for full ingredients
    fullResponse = api.get_recipe_information(recipeID)
    fullData = fullResponse.json()
    title = fullData["title"]

    # Get full ingredients
    ingredients = []
    for item in fullData['extendedIngredients']:
        ingredients.append(item['original'])
    finalIngredients = '\n'.join(ingredients)

    # Get instruction
    instResponse = api.get_analyzed_recipe_instructions(recipeID)
    instruction = instResponse.json()

    instructions = []
    try:
        steps = instruction[0].get('steps', "")
        for step in steps:
            inst = str(step['number']) + ' ' + step['step']
            instructions.append(inst)
        finalSteps = '\n'.join(instructions)

        final = title + "\n---------------------------------------------------------------\n" \
                + finalIngredients + "\n---------------------------------------------------------------\n" \
                + finalSteps
        print(final)
        field2.insert("end", final)
    except Exception:
        field2.insert("end", 'Sorry No recipe has found!')


# Function to evaluate the final expression
def enter():
    global expression
    expression = field1.get()

    # clear the showing field
    field2.delete(1.0, 'end')

    # execute function to search recipes
    searchIngredients(expression)


def clear():
    field1.delete(0, 'end')
    field2.delete(1.0, 'end')


# Driver code
if __name__ == "__main__":
    # create a GUI window
    master = tk.Tk()

    s = tk.StringVar()

    field1 = tk.Entry(master, textvariable=s)
    field1.config({"background": "LightBlue1", "disabledbackground": "LightSkyBlue1"})
    field2 = tk.Text(master, wrap="word", height=30, width=30)
    field2.config({"background": "Ivory"})

    field1.place(x=20, y=20, width=660, height=40)
    field2.place(x=20, y=80, width=660, height=500)

    field1.configure(state='disabled')
    field2.configure(state='disabled')

    # set font
    myFont = font.Font(family='Verdana', size=9, weight='bold')

    # set text message for cavas
    text = "Welcome to Recipe Finder!\n" \
           + "Instruction: Click the colored button,\n" \
           + "Type either sentence or words\n" \
           + "into the light blue box."

    canvas = tk.Canvas(master, width=250, height=100, bg='DodgerBlue4')
    canvas.pack()
    canvas.place(x=700, y=40)
    canvas.create_text(125, 50, fill="white", font=myFont, text=text)

    # set the background colour of GUI window
    master.configure(background="lemon chiffon")

    # set the title of GUI window
    master.title("Recipe Finder")

    # set the configuration of GUI window
    master.geometry("970x600")

    # Buttons
    button1 = tk.Button(master, text=' Click for some food jokes! ', fg='black', bg='salmon',
                        command=foodJokes, height=5, width=30)
    button1.place(x=700, y=200)
    button1['font'] = myFont

    button2 = tk.Button(master, text=' Type the ingredients you have! ', fg='black', bg='orange',
                        command=askForIngredients, height=5, width=30)
    button2.place(x=700, y=300)
    button2['font'] = myFont

    Clear = tk.Button(master, text=' CLEAR ', fg='black', bg='white',
                      command=clear, height=5, width=30)
    Clear.place(x=700, y=400)
    Clear['font'] = myFont

    Enter = tk.Button(master, text=' ENTER ', fg='black', bg='white',
                      command=enter, height=5, width=30)
    Enter.place(x=700, y=500)
    Enter['font'] = myFont

# start the GUI
master.mainloop()
print(expression)
