import tkinter as tk
from PIL import Image, ImageTk

# Initialize counters for wins and ties
player1_wins = 0
player2_wins = 0
ties = 0

# Variable to track the starting player
starting_player = "X"

# Create the window
root = tk.Tk()
root.title("Tic Tac Toe made by LAMNAOUAR Ayoub")
root.geometry("460x460")  # Adjusted to accommodate borders
root.resizable(False, False)  # Make the window non-resizable

# Load the custom icon
icon_path = 'C:/Users/ayoub/Desktop/CST Bachelor\'s degree at WIT/semester 6/professional practice/professional-practice-codes/Validation_Programming/tictactoe.png'
icon_image = Image.open(icon_path)
icon_photo = ImageTk.PhotoImage(icon_image)
root.iconphoto(True, icon_photo)

# Size of each canvas cell
cell_size = 150  # Size of each cell
border_width = 4  # Width of the borders
total_size = cell_size + border_width

# Load and resize the images
def load_and_resize_image(image_path, size):
    image = Image.open(image_path)
    image = image.resize((int(size * 0.9), int(size * 0.9)), Image.LANCZOS)  # Resize to 90% of the cell size
    return image

# Load the images
x_image_path = 'C:/Users/ayoub/Desktop/CST Bachelor\'s degree at WIT/semester 6/professional practice/professional-practice-codes/Validation_Programming/x_image.png'
o_image_path = 'C:/Users/ayoub/Desktop/CST Bachelor\'s degree at WIT/semester 6/professional practice/professional-practice-codes/Validation_Programming/o_image.png'

x_image_orig = load_and_resize_image(x_image_path, cell_size)
o_image_orig = load_and_resize_image(o_image_path, cell_size)

# Initialize the current player (Player 1 starts with "X")
current_player = starting_player

# Initialize the board state
board = [["" for _ in range(3)] for _ in range(3)]

def check_winner():
    global player1_wins, player2_wins, ties

    # Check rows and columns
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != "":
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != "":
            return board[0][i]

    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] != "":
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != "":
        return board[0][2]

    # Check for tie
    if all(board[row][col] != "" for row in range(3) for col in range(3)):
        return "Tie"

    return None

def reset_board():
    global board, current_player
    for row in canvases:
        for canvas in row:
            canvas.delete("all")
    board = [["" for _ in range(3)] for _ in range(3)]
    current_player = starting_player

def display_results(winner):
    global starting_player
    
    results_frame = tk.Frame(root, bg="white")
    results_frame.grid(row=0, column=0, rowspan=3, columnspan=3, sticky="nsew")

    font_path = "SimHei"  # Use the Chinese-style font
    winner_text = f"Winner: Player {1 if winner == 'X' else 2} ({winner})" if winner != "Tie" else "It's a Tie!"
    winner_label = tk.Label(results_frame, text=winner_text, font=(font_path, 24, "bold"), fg="red", bg="white")
    winner_label.pack(pady=40)

    scores_label = tk.Label(results_frame, text=f"Scores\nPlayer 1 (X): {player1_wins}\nPlayer 2 (O): {player2_wins}\nTie: {ties}", font=(font_path, 18), fg="green", bg="white")
    scores_label.pack(pady=20)

    message_label = tk.Label(results_frame, text="Click anywhere to play again", font=(font_path, 12), bg="white")
    message_label.pack(pady=10)

    results_frame.bind("<Button-1>", lambda event: [results_frame.destroy(), reset_board()])

    # Switch starting player for the next round
    starting_player = "O" if starting_player == "X" else "X"

def animate_image(canvas, image, final_size, step, delay):
    current_size = int(final_size * step)
    resized_image = image.resize((current_size, current_size), Image.LANCZOS)
    tk_image = ImageTk.PhotoImage(resized_image)
    
    canvas.delete("drawn")
    canvas.create_image(cell_size/2, cell_size/2, image=tk_image, anchor=tk.CENTER, tags="drawn")
    canvas.image = tk_image  # Store reference to avoid garbage collection

    if step < 1.0:
        canvas.after(delay, animate_image, canvas, image, final_size, step + 0.2, delay)  # Increase step size for faster animation

# Create a function to handle canvas clicks
def on_click(event, row, col):
    global current_player, player1_wins, player2_wins, ties
    canvas = canvases[row][col]

    # Check if the cell is already occupied
    if not canvas.find_withtag("drawn"):
        # Select the image based on the current player
        image_orig = x_image_orig if current_player == "X" else o_image_orig
        
        # Animate the image
        animate_image(canvas, image_orig, int(cell_size * 0.9), 0.1, 20)  # Reduce delay for faster animation

        # Update the board state
        board[row][col] = current_player

        # Check for a winner
        winner = check_winner()
        if winner:
            if winner == "X":
                player1_wins += 1
                print(f"Player 1 (X) wins! Total wins: {player1_wins}")
            elif winner == "O":
                player2_wins += 1
                print(f"Player 2 (O) wins! Total wins: {player2_wins}")
            else:
                ties += 1
                print(f"It's a tie! Total ties: {ties}")
            display_results(winner)
            return

        # Switch player
        current_player = "O" if current_player == "X" else "X"

# Create the background canvas for the grid
background_canvas = tk.Canvas(root, width=3*total_size, height=3*total_size, bg="white", highlightthickness=0)
background_canvas.grid(row=0, column=0, rowspan=3, columnspan=3, sticky="nsew")

# Draw borders between the cells
border_color = "#8B4513"  # Woody color
border_width = 4

# Draw the borders between the cells
background_canvas.create_line(total_size, 0, total_size, 3*total_size, fill=border_color, width=border_width)  # Vertical line 1
background_canvas.create_line(2*total_size, 0, 2*total_size, 3*total_size, fill=border_color, width=border_width)  # Vertical line 2
background_canvas.create_line(0, total_size, 3*total_size, total_size, fill=border_color, width=border_width)  # Horizontal line 1
background_canvas.create_line(0, 2*total_size, 3*total_size, 2*total_size, fill=border_color, width=border_width)  # Horizontal line 2

# Create canvases for the 3x3 grid
canvases = []
for row in range(3):
    canvas_row = []
    for col in range(3):
        canvas = tk.Canvas(background_canvas, width=cell_size, height=cell_size, bg="white", highlightthickness=0)
        canvas.grid(row=row, column=col, padx=(0, border_width) if col < 2 else 0, pady=(0, border_width) if row < 2 else 0)
        canvas.bind("<Button-1>", lambda event, r=row, c=col: on_click(event, r, c))
        canvas_row.append(canvas)
    canvases.append(canvas_row)

# Configure the grid to expand proportionally
for i in range(3):
    root.grid_rowconfigure(i, weight=1)
    root.grid_columnconfigure(i, weight=1)

# Run the main loop
root.mainloop()
