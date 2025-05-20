# page-replacement-algorithm
#Name: Ushijima, Natsuki B.
#Section: BSCS-3B
#Subject: Operating System

from tkinter import Tk, Button
from random import randrange

# Constants
FRAME_NUMBER = 4  # Number of memory frames
REFERENCE_CHAIN_LENGTH = 13  # Number of page requests

# FIFO (First-In, First-Out) algorithm implementation
def FIFO():
    current_memory_state = []       # List of currently loaded pages
    pageArrivingOrder = []          # Tracks the order pages arrived (for FIFO replacement)
    global buttons
    for i in range(1, REFERENCE_CHAIN_LENGTH + 1):
        # Update memory display before inserting a new page
        for j in range(len(current_memory_state)):
            buttons[j + 1][i].config(text=current_memory_state[j])
        
        # Page not in memory → Page fault
        if buttons[0][i]['text'] not in current_memory_state:
            newPage = buttons[0][i]['text']
            if len(current_memory_state) < FRAME_NUMBER:
                # Memory has space → Add page
                pageArrivingOrder.append(newPage)
                current_memory_state.append(newPage)
                buttons[len(current_memory_state)][i].config(text=newPage)
            else:
                # Memory full → Replace oldest page
                index = current_memory_state.index(pageArrivingOrder.pop(0))
                pageArrivingOrder.append(newPage)
                current_memory_state[index] = newPage
                buttons[index + 1][i].config(text=newPage)

# LRU (Least Recently Used) algorithm implementation
def LRU():
    current_memory_state = []       # Memory frames
    pageArrivingOrder = []          # Tracks last used order
    global buttons
    for i in range(1, REFERENCE_CHAIN_LENGTH + 1):
        for j in range(len(current_memory_state)):
            buttons[j + 1][i].config(text=current_memory_state[j])
        
        newPage = buttons[0][i]['text']
        if newPage not in current_memory_state:
            if len(current_memory_state) < FRAME_NUMBER:
                # Space available → Add page
                pageArrivingOrder.append(newPage)
                current_memory_state.append(newPage)
                buttons[len(current_memory_state)][i].config(text=newPage)
            else:
                # Replace least recently used page
                index = current_memory_state.index(pageArrivingOrder.pop(0))
                pageArrivingOrder.append(newPage)
                current_memory_state[index] = newPage
                buttons[index + 1][i].config(text=newPage)
        else:
            # Page hit → Move page to end of usage list
            pageArrivingOrder.remove(newPage)
            pageArrivingOrder.append(newPage)

# OPT (Optimal) algorithm implementation
def OPTIMAL():
    global buttons
    current_memory_state = []       # Memory frames
    referenceChain = [buttons[0][i]['text'] for i in range(1, REFERENCE_CHAIN_LENGTH + 1)]
    
    for i in range(1, REFERENCE_CHAIN_LENGTH + 1):
        for j in range(len(current_memory_state)):
            buttons[j + 1][i].config(text=current_memory_state[j])
        
        currentPage = buttons[0][i]['text']
        if currentPage not in current_memory_state:
            if len(current_memory_state) < FRAME_NUMBER:
                # Add page to memory
                current_memory_state.append(currentPage)
                buttons[len(current_memory_state)][i].config(text=currentPage)
            else:
                # Predict which page won't be used for longest time
                future_use = []
                not_used_again = []
                
                # Find order of future page uses
                for k in range(i + 1, REFERENCE_CHAIN_LENGTH + 1):
                    if (buttons[0][k]['text'] in current_memory_state and
                            buttons[0][k]['text'] not in future_use):
                        future_use.append(buttons[0][k]['text'])

                # Find pages not used again
                for page in current_memory_state:
                    if page not in future_use:
                        not_used_again.append(page)

                # Select replacement page
                if not_used_again:
                    replace = current_memory_state.index(not_used_again[0])
                else:
                    replace = current_memory_state.index(future_use[-1])
                
                current_memory_state[replace] = currentPage
                buttons[replace + 1][i].config(text=currentPage)

# RESET the grid and generate new reference string
def RESET():
    global buttons
    for i in range(1, REFERENCE_CHAIN_LENGTH + 1):
        # Random page numbers between 0–9
        buttons[0][i].config(text=randrange(10), bg="#f3f4f6")
        for j in range(1, FRAME_NUMBER + 1):
            buttons[j][i].config(text="", bg="#e0f2fe")

# GUI setup
if __name__ == "__main__":
    mywindow = Tk()
    mywindow.title("Page Replacement Algorithms")
    buttons = []

    # Create button grid (rows = frames, cols = reference positions)
    for row in range(FRAME_NUMBER + 1):
        button_row = []
        for col in range(REFERENCE_CHAIN_LENGTH + 1):
            button = Button(
                mywindow,
                borderwidth=1,
                width=8,
                height=2,
                bg="#e0f2fe",  # light blue
                fg="black",
                font=("Arial", 10, "bold")
            )
            button.grid(row=row, column=col)
            button_row.append(button)
        buttons.append(button_row)

    # Header cell
    buttons[0][0].config(text="Frame/Page", bg="#d1d5db")

    # Control buttons
    Button(mywindow, text="LRU", command=LRU, width=10, height=2,
           bg="#fde68a", fg="black", font=("Arial", 10, "bold")).grid(row=FRAME_NUMBER + 3, column=0)
    Button(mywindow, text="FIFO", command=FIFO, width=10, height=2,
           bg="#bbf7d0", fg="black", font=("Arial", 10, "bold")).grid(row=FRAME_NUMBER + 3, column=1)
    Button(mywindow, text="Optimal", command=OPTIMAL, width=10, height=2,
           bg="#bfdbfe", fg="black", font=("Arial", 10, "bold")).grid(row=FRAME_NUMBER + 3, column=2)
    Button(mywindow, text="Reset", command=RESET, width=10, height=2,
           bg="#fca5a5", fg="black", font=("Arial", 10, "bold")).grid(row=FRAME_NUMBER + 3, column=3)

    # Frame labels (leftmost column)
    for i in range(1, FRAME_NUMBER + 1):
        buttons[i][0].config(text=str(i), bg="#d1d5db")

    # Generate initial page references
    RESET()

    # Run GUI
    mywindow.mainloop()
