import tkinter as tk
from PIL import Image, ImageTk

class TicTacToe:
    #initialize the game
    def __init__(self, root):
        #initialize counters for wins and ties
        self.player1_wins = 0
        self.player2_wins = 0
        self.ties = 0
        #variable to track the starting player
        self.starting_player = "X"
        #initialize the current player (Player 1 starts with "X")
        self.current_player = self.starting_player
        #initialize the board state
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.canvases = []

        #create the window
        self.root = root
        self.root.title("Tic Tac Toe made by LAMNAOUAR Ayoub")
        self.root.geometry("460x460")  #adjusted to accommodate borders
        self.root.resizable(False, False)  #make the window non-resizable

        #load the custom icon
        icon_path = 'C:/Users/ayoub/Desktop/CST Bachelor\'s degree at WIT/semester 6/professional practice/professional-practice-codes/Validation_Programming/tictactoe.png'
        icon_image = Image.open(icon_path)
        icon_photo = ImageTk.PhotoImage(icon_image)
        self.root.iconphoto(True, icon_photo)

        #size of each canvas cell
        self.cell_size = 150  #size of each cell
        self.border_width = 4  #width of the borders
        self.total_size = self.cell_size + self.border_width

        #load and resize the images
        x_image_path = 'C:/Users/ayoub/Desktop/CST Bachelor\'s degree at WIT/semester 6/professional practice/professional-practice-codes/Validation_Programming/x_image.png'
        o_image_path = 'C:/Users/ayoub/Desktop/CST Bachelor\'s degree at WIT/semester 6/professional practice/professional-practice-codes/Validation_Programming/o_image.png'
        self.x_image_orig = self.load_and_resize_image(x_image_path, self.cell_size)
        self.o_image_orig = self.load_and_resize_image(o_image_path, self.cell_size)

        #create the background canvas for the grid
        self.background_canvas = tk.Canvas(self.root, width=3*self.total_size, height=3*self.total_size, bg="white", highlightthickness=0)
        self.background_canvas.grid(row=0, column=0, rowspan=3, columnspan=3, sticky="nsew")
        #draw borders between the cells
        self.draw_borders()
        #create canvases for the 3x3 grid
        self.create_grid()

        #configure the grid to expand proportionally
        for i in range(3):
            self.root.grid_rowconfigure(i, weight=1)
            self.root.grid_columnconfigure(i, weight=1)

    #load and resize the images
    def load_and_resize_image(self, image_path, size):
        image = Image.open(image_path)
        image = image.resize((int(size * 0.9), int(size * 0.9)), Image.LANCZOS)  #resize to 90% of the cell size
        return image

    #draw borders between the cells
    def draw_borders(self):
        border_color = "#8B4513"  #woody color
        border_width = 4
        self.background_canvas.create_line(self.total_size, 0, self.total_size, 3*self.total_size, fill=border_color, width=border_width)  #vertical line 1
        self.background_canvas.create_line(2*self.total_size, 0, 2*self.total_size, 3*self.total_size, fill=border_color, width=border_width)  #vertical line 2
        self.background_canvas.create_line(0, self.total_size, 3*self.total_size, self.total_size, fill=border_color, width=border_width)  #horizontal line 1
        self.background_canvas.create_line(0, 2*self.total_size, 3*self.total_size, 2*self.total_size, fill=border_color, width=border_width)  #horizontal line 2

    #create canvases for the 3x3 grid
    def create_grid(self):
        for row in range(3):
            canvas_row = []
            for col in range(3):
                canvas = tk.Canvas(self.background_canvas, width=self.cell_size, height=self.cell_size, bg="white", highlightthickness=0)
                canvas.grid(row=row, column=col, padx=(0, self.border_width) if col < 2 else 0, pady=(0, self.border_width) if row < 2 else 0)
                canvas.bind("<Button-1>", lambda event, r=row, c=col: self.on_click(event, r, c))
                canvas_row.append(canvas)
            self.canvases.append(canvas_row)

    #check for a winner
    def check_winner(self):
        #check rows and columns
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != "":
                return self.board[i][0]
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != "":
                return self.board[0][i]
        #check diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != "":
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != "":
            return self.board[0][2]
        #check for tie
        if all(self.board[row][col] != "" for row in range(3) for col in range(3)):
            return "Tie"
        return None

    #reset the board
    def reset_board(self):
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.current_player = self.starting_player
        for row in self.canvases:
            for canvas in row:
                canvas.delete("all")

    #display the results
    def display_results(self, winner):
        results_frame = tk.Frame(self.root, bg="white")
        results_frame.grid(row=0, column=0, rowspan=3, columnspan=3, sticky="nsew")

        font_path = "SimHei"  #use the Chinese-style font
        winner_text = f"Winner: Player {1 if winner == 'X' else 2} ({winner})" if winner != "Tie" else "It's a Tie!"
        winner_label = tk.Label(results_frame, text=winner_text, font=(font_path, 24, "bold"), fg="red", bg="white")
        winner_label.pack(pady=40)

        scores_label = tk.Label(results_frame, text=f"Scores\nPlayer 1 (X): {self.player1_wins}\nPlayer 2 (O): {self.player2_wins}\nTie: {self.ties}", font=(font_path, 18), fg="green", bg="white")
        scores_label.pack(pady=20)

        message_label = tk.Label(results_frame, text="Click anywhere to play again", font=(font_path, 12), bg="white")
        message_label.pack(pady=10)

        results_frame.bind("<Button-1>", lambda event: [results_frame.destroy(), self.reset_board()])

        #switch starting player for the next round
        self.starting_player = "O" if self.starting_player == "X" else "X"

    #animate the image
    def animate_image(self, canvas, image, final_size, step, delay):
        current_size = int(final_size * step)
        resized_image = image.resize((current_size, current_size), Image.LANCZOS)
        tk_image = ImageTk.PhotoImage(resized_image)
        
        canvas.delete("drawn")
        canvas.create_image(self.cell_size/2, self.cell_size/2, image=tk_image, anchor=tk.CENTER, tags="drawn")
        canvas.image = tk_image  #store reference to avoid garbage collection

        if step < 1.0:
            canvas.after(delay, self.animate_image, canvas, image, final_size, step + 0.2, delay)  #increase step size for faster animation

    #handle canvas clicks
    def on_click(self, event, row, col):
        canvas = self.canvases[row][col]

        #check if the cell is already occupied
        if not canvas.find_withtag("drawn"):
            #select the image based on the current player
            image_orig = self.x_image_orig if self.current_player == "X" else self.o_image_orig
            
            #animate the image
            self.animate_image(canvas, image_orig, int(self.cell_size * 0.9), 0.1, 20)  #reduce delay for faster animation

            #update the board state
            self.board[row][col] = self.current_player

            #check for a winner
            winner = self.check_winner()
            if winner:
                if winner == "X":
                    self.player1_wins += 1
                    print(f"Player 1 (X) wins! Total wins: {self.player1_wins}")
                elif winner == "O":
                    self.player2_wins += 1
                    print(f"Player 2 (O) wins! Total wins: {self.player2_wins}")
                else:
                    self.ties += 1
                    print(f"It's a tie! Total ties: {self.ties}")
                self.display_results(winner)
                return

            #switch player
            self.current_player = "O" if self.current_player == "X" else "X"

#run the game
if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()
