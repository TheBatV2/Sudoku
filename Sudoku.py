import arcade
import random
import copy


# Constants
WIDTH = 600
HEIGHT = 700
MARGIN = 5
GRID_SIZE = 9
CELL_SIZE = (WIDTH - 20) // GRID_SIZE  # Added small padding for right edge
TOP_MARGIN = 100  # Space for UI elements at top
BOTTOM_MARGIN = 20  # Added small padding for bottom edge

# Calculate the actual game board area
BOARD_WIDTH = CELL_SIZE * GRID_SIZE
BOARD_HEIGHT = CELL_SIZE * GRID_SIZE
BOARD_LEFT = (WIDTH - BOARD_WIDTH) // 2  # Center the board horizontally
BOARD_TOP = HEIGHT - TOP_MARGIN
BOARD_BOTTOM = BOARD_TOP - BOARD_HEIGHT

DIFFICULTY_HINTS = {
    "Easy": 40,
    "Medium": 30,
    "Hard": 20
}

DIFFICULTY_POINTS = {
    "Easy": 100,
    "Medium": 150,
    "Hard": 200
}

# Improved how to play instructions with shorter lines
HOW_TO_PLAY = [
    "Goal: Fill the grid so each row, column,",
    "and 3x3 box contains digits 1-9 without repeating.",
    "Click a cell to select it, then press",
    "a number key to enter a value.",
    "You can use regular number keys or numpad keys.",
    "You lose a life when you make an incorrect entry.",
    "Your streak ends if you run out of lives.",
    "Press ESC for menu, and R to reshuffle the puzzle."
]

class SudokuGame(arcade.Window):
    def __init__(self):
        super().__init__(WIDTH, HEIGHT, "Sudoku Game")
        arcade.set_background_color(arcade.color.WHITE)
        self.selected_cell = (0, 0)
        self.user_board = []
        self.solution = []
        self.given_cells = set()
        self.lives = 3
        self.difficulty = "Easy"
        self.streak = {"Easy": 0, "Medium": 0, "Hard": 0}
        self.score = 0
        self.high_score = 0
        self.show_menu = True
        self.show_how_to_play = False
        self.show_congrats = False
        self.setup()  # Initialize the game state

    def setup(self, difficulty="Easy"):
        self.difficulty = difficulty
        self.lives = 3
        
        if not self.show_menu and not self.show_congrats:  # Only reset the board if we're not in menu or congrats
            full_board = self.generate_full_board()
            self.solution = copy.deepcopy(full_board)
            self.user_board = self.remove_cells(copy.deepcopy(full_board), DIFFICULTY_HINTS[difficulty])

            self.given_cells = {
                (x, y)
                for y in range(9)
                for x in range(9)
                if self.user_board[y][x] != 0
            }
        else:
            # Initialize empty boards for the menu state
            self.user_board = [[0 for _ in range(9)] for _ in range(9)]
            self.solution = [[0 for _ in range(9)] for _ in range(9)]
            self.given_cells = set()

    def generate_full_board(self):
        board = [[0 for _ in range(9)] for _ in range(9)]
        self.solve_board(board)
        return board

    def solve_board(self, board):
        for y in range(9):
            for x in range(9):
                if board[y][x] == 0:
                    nums = list(range(1, 10))
                    random.shuffle(nums)
                    for num in nums:
                        if self.is_valid(board, x, y, num):
                            board[y][x] = num
                            if self.solve_board(board):
                                return True
                            board[y][x] = 0
                    return False
        return True

    def is_valid(self, board, x, y, num):
        for i in range(9):
            if board[y][i] == num or board[i][x] == num:
                return False
        box_x = (x // 3) * 3
        box_y = (y // 3) * 3
        for i in range(3):
            for j in range(3):
                if board[box_y + i][box_x + j] == num:
                    return False
        return True

    def remove_cells(self, board, keep_count):
        positions = [(x, y) for y in range(9) for x in range(9)]
        random.shuffle(positions)
        removed = 0
        while 81 - removed > keep_count:
            x, y = positions.pop()
            if board[y][x] != 0:
                board[y][x] = 0
                removed += 1
        return board

    def on_draw(self):
        self.clear()
        
        # Always draw the board as background
        self.draw_board()
        self.draw_info_top()
        
        # Draw menu overlay if in menu mode
        if self.show_menu:
            # Semi-transparent overlay
            arcade.draw_lrbt_rectangle_filled(0, WIDTH, 0, HEIGHT, 
                                              (255, 255, 255, 200))  # White with alpha
            self.draw_menu()
        elif self.show_how_to_play:
            # Semi-transparent overlay
            arcade.draw_lrbt_rectangle_filled(0, WIDTH, 0, HEIGHT, 
                                              (255, 255, 255, 200))  # White with alpha
            self.draw_how_to_play()
        elif self.show_congrats:
            # Semi-transparent overlay
            arcade.draw_lrbt_rectangle_filled(0, WIDTH, 0, HEIGHT, 
                                              (255, 255, 255, 200))  # White with alpha
            self.draw_congrats_screen()

    def draw_menu(self):
        arcade.draw_text("SUDOKU", WIDTH / 2, HEIGHT - 80,
                         arcade.color.BLACK, 36, anchor_x="center")
        
        arcade.draw_text("Select Difficulty", WIDTH / 2, HEIGHT - 150,
                         arcade.color.BLACK, 24, anchor_x="center")
        arcade.draw_lrbt_rectangle_filled(90, WIDTH - 90, 60, HEIGHT - 120, arcade.color.LIGHT_GRAY)
        arcade.draw_lrbt_rectangle_outline(90, WIDTH - 90, 60, HEIGHT - 120, arcade.color.BLACK, 2)
        
        # Draw difficulty buttons
        for i, level in enumerate(DIFFICULTY_HINTS.keys()):
            cx = WIDTH / 2
            cy = HEIGHT - 220 - i * 60
            half_w = 100
            half_h = 30
            
            # Draw button background
            arcade.draw_lrbt_rectangle_filled(
                cx - half_w, cx + half_w, cy - half_h, cy + half_h, 
                arcade.color.LIGHT_BLUE
            )
            
            # Draw button border
            arcade.draw_lrbt_rectangle_outline(
                cx - half_w, cx + half_w, cy - half_h, cy + half_h,
                arcade.color.BLACK, 2
            )
            
            # Draw button text
            arcade.draw_text(level, cx, cy - 10, arcade.color.BLACK, 20, anchor_x="center")
        
        # Draw "How to Play" button
        cx = WIDTH / 2
        cy = HEIGHT - 220 - 3 * 60  # Position below difficulty buttons
        half_w = 100
        half_h = 30
        
        arcade.draw_lrbt_rectangle_filled(
            cx - half_w, cx + half_w, cy - half_h, cy + half_h, 
            arcade.color.LIGHT_GREEN
        )
        
        arcade.draw_lrbt_rectangle_outline(
            cx - half_w, cx + half_w, cy - half_h, cy + half_h,
            arcade.color.BLACK, 2
        )
        
        arcade.draw_text("How to Play", cx, cy - 10, arcade.color.BLACK, 20, anchor_x="center")
        
        # Draw high score
        arcade.draw_text(f"High Score: {self.high_score}", 
                         WIDTH / 2, 80, 
                         arcade.color.DARK_GREEN, 24, anchor_x="center")

    def draw_how_to_play(self):
        arcade.draw_text("How to Play Sudoku", WIDTH / 2, HEIGHT - 80,
                         arcade.color.BLACK, 36, anchor_x="center")
        arcade.draw_lrbt_rectangle_filled(90, WIDTH - 90, 60, HEIGHT - 120, arcade.color.LIGHT_GRAY)
        arcade.draw_lrbt_rectangle_outline(90, WIDTH - 90, 60, HEIGHT - 120, arcade.color.BLACK, 2)
        
        # Draw instructions with smaller font size and more spacing
        for i, instruction in enumerate(HOW_TO_PLAY):
            arcade.draw_text(instruction, 
                             WIDTH / 2, HEIGHT - 180 - (i * 35),
                             arcade.color.BLACK, 14, anchor_x="center")
        
        # Draw back button
        cx = WIDTH / 2
        cy = 100
        half_w = 100
        half_h = 30
        
        arcade.draw_lrbt_rectangle_filled(
            cx - half_w, cx + half_w, cy - half_h, cy + half_h, 
            arcade.color.LIGHT_BLUE
        )
        
        arcade.draw_lrbt_rectangle_outline(
            cx - half_w, cx + half_w, cy - half_h, cy + half_h,
            arcade.color.BLACK, 2
        )
        
        arcade.draw_text("Back to Menu", cx, cy - 10, arcade.color.BLACK, 20, anchor_x="center")

    def draw_congrats_screen(self):
        # Calculate total score for this puzzle
        puzzle_score = DIFFICULTY_POINTS[self.difficulty]
        
        arcade.draw_text("Congratulations!", WIDTH / 2, HEIGHT - 150,
                         arcade.color.DARK_GREEN, 36, anchor_x="center")
        
        arcade.draw_text(f"You completed the {self.difficulty} puzzle!", 
                         WIDTH / 2, HEIGHT - 220,
                         arcade.color.BLACK, 20, anchor_x="center")
        
        arcade.draw_text(f"Points earned: {puzzle_score}", 
                         WIDTH / 2, HEIGHT - 260,
                         arcade.color.BLUE, 20, anchor_x="center")
        
        arcade.draw_text(f"Current streak: {self.streak[self.difficulty]}", 
                         WIDTH / 2, HEIGHT - 300,
                         arcade.color.PURPLE, 20, anchor_x="center")
        
        arcade.draw_text(f"Total score: {self.score}", 
                         WIDTH / 2, HEIGHT - 340,
                         arcade.color.RED, 20, anchor_x="center")
        
        # Draw continue button
        cx = WIDTH / 3
        cy = HEIGHT - 400
        half_w = 80
        half_h = 30
        
        arcade.draw_lrbt_rectangle_filled(
            cx - half_w, cx + half_w, cy - half_h, cy + half_h, 
            arcade.color.LIGHT_GREEN
        )
        
        arcade.draw_lrbt_rectangle_outline(
            cx - half_w, cx + half_w, cy - half_h, cy + half_h,
            arcade.color.BLACK, 2
        )
        
        arcade.draw_text("Continue", cx, cy - 10, arcade.color.BLACK, 20, anchor_x="center")
        
        # Draw menu button
        cx = 2 * WIDTH / 3
        
        arcade.draw_lrbt_rectangle_filled(
            cx - half_w, cx + half_w, cy - half_h, cy + half_h, 
            arcade.color.LIGHT_BLUE
        )
        
        arcade.draw_lrbt_rectangle_outline(
            cx - half_w, cx + half_w, cy - half_h, cy + half_h,
            arcade.color.BLACK, 2
        )
        
        arcade.draw_text("Main Menu", cx, cy - 10, arcade.color.BLACK, 20, anchor_x="center")

    def draw_board(self):
        # Store selected cell for highlighting
        sel_col, sel_row = self.selected_cell
        
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                # Calculate cell position with offset for centering
                center_x = BOARD_LEFT + col * CELL_SIZE + CELL_SIZE // 2
                center_y = BOARD_TOP - (row * CELL_SIZE) - CELL_SIZE // 2
                half = (CELL_SIZE - MARGIN) // 2

                # Determine cell background color
                color = arcade.color.WHITE
                
                # Highlight row and column of selected cell
                if not self.show_menu and not self.show_congrats and not self.show_how_to_play and (row == sel_row or col == sel_col):
                    color = arcade.color.LIGHT_YELLOW
                
                # Selected cell gets priority highlight
                if (col, row) == self.selected_cell:
                    color = arcade.color.LIGHT_GRAY
                    
                # Draw cell background
                arcade.draw_lrbt_rectangle_filled(
                    center_x - half, center_x + half, 
                    center_y - half, center_y + half, 
                    color
                )
                
                # Draw cell outline
                left = center_x - CELL_SIZE // 2 + MARGIN // 2
                right = center_x + CELL_SIZE // 2 - MARGIN // 2
                bottom = center_y - CELL_SIZE // 2 + MARGIN // 2
                top = center_y + CELL_SIZE // 2 - MARGIN // 2
                arcade.draw_lrbt_rectangle_outline(
                    left, right, bottom, top,
                    arcade.color.BLACK, 1
                )
                
                # Draw cell value
                val = self.user_board[row][col]
                if val != 0:
                    text_color = arcade.color.BLACK if (col, row) in self.given_cells else arcade.color.BLUE
                    arcade.draw_text(str(val), center_x, center_y - 10, text_color, 20, anchor_x="center")

        # Draw grid lines
        for i in range(GRID_SIZE + 1):
            line_width = 4 if i % 3 == 0 else 1
            # Horizontal lines
            y = BOARD_TOP - i * CELL_SIZE
            arcade.draw_line(BOARD_LEFT, y, BOARD_LEFT + BOARD_WIDTH, y, arcade.color.BLACK, line_width)
            # Vertical lines
            x = BOARD_LEFT + i * CELL_SIZE
            arcade.draw_line(x, BOARD_TOP, x, BOARD_BOTTOM, arcade.color.BLACK, line_width)

    def draw_info_top(self):
        # Draw background for top info area
        arcade.draw_lrbt_rectangle_filled(
            0, WIDTH, BOARD_TOP, HEIGHT, 
            arcade.color.LIGHT_GRAY
        )
        
        # Draw difficulty
        arcade.draw_text(f"Difficulty: {self.difficulty}", 
                         20, HEIGHT - 30, 
                         arcade.color.BLACK, 16, anchor_x="left")
        
        # Draw lives with heart symbols
        lives_text = f"Lives: {self.lives}"
        arcade.draw_text(lives_text, 
                         20, HEIGHT - 60, 
                         arcade.color.RED, 16, anchor_x="left")
        
        # Draw current score
        arcade.draw_text(f"Score: {self.score}", 
                         WIDTH - 20, HEIGHT - 30, 
                         arcade.color.DARK_GREEN, 16, anchor_x="right")
        
        # Draw streak
        arcade.draw_text(f"Streak: {self.streak[self.difficulty]}", 
                         WIDTH - 20, HEIGHT - 60, 
                         arcade.color.PURPLE, 16, anchor_x="right")
        
        # Draw high score in the middle
        arcade.draw_text(f"High Score: {self.high_score}", 
                         WIDTH // 2, HEIGHT - 30, 
                         arcade.color.DARK_BLUE, 16, anchor_x="center")

    def on_mouse_press(self, x, y, button, modifiers):
        # Handle menu interaction
        if self.show_menu:
            # Check if user clicked on a difficulty button
            for i, level in enumerate(DIFFICULTY_HINTS.keys()):
                cx = WIDTH / 2
                cy = HEIGHT - 220 - i * 60
                if cx - 100 < x < cx + 100 and cy - 30 < y < cy + 30:
                    self.show_menu = False  # Hide the menu
                    self.setup(level)  # Setup game with selected difficulty
                    return
            
            # Check if user clicked on "How to Play" button
            cx = WIDTH / 2
            cy = HEIGHT - 220 - 3 * 60
            if cx - 100 < x < cx + 100 and cy - 30 < y < cy + 30:
                self.show_menu = False
                self.show_how_to_play = True
                return
            
            return
        
        # Handle "How to Play" back button
        if self.show_how_to_play:
            cx = WIDTH / 2
            cy = 100
            if cx - 100 < x < cx + 100 and cy - 30 < y < cy + 30:
                self.show_how_to_play = False
                self.show_menu = True
                return
            
            return
        
        # Handle congratulations screen buttons
        if self.show_congrats:
            cy = HEIGHT - 400
            
            # Continue button
            cx = WIDTH / 3
            if cx - 80 < x < cx + 80 and cy - 30 < y < cy + 30:
                self.show_congrats = False
                self.setup(self.difficulty)  # Start new puzzle with same difficulty
                return
            
            # Main menu button
            cx = 2 * WIDTH / 3
            if cx - 80 < x < cx + 80 and cy - 30 < y < cy + 30:
                self.show_congrats = False
                self.show_menu = True
                return
            
            return

        # Normal game play - select a cell
        if y < BOARD_BOTTOM or y > BOARD_TOP or x < BOARD_LEFT or x > BOARD_LEFT + BOARD_WIDTH:
            return  # Click outside the grid

        # Adjust column and row calculation to account for board offset
        col = int((x - BOARD_LEFT) // CELL_SIZE)
        row = int((BOARD_TOP - y) // CELL_SIZE)

        if 0 <= col < GRID_SIZE and 0 <= row < GRID_SIZE:
            self.selected_cell = (col, row)

    def on_key_press(self, key, modifiers):
        if self.show_menu or self.show_how_to_play or self.show_congrats:
            return  # Ignore key presses in menu

        # Process number input from both regular number keys and numpad
        number = None
        
        # Check for regular number keys 1-9 (ASCII 49-57)
        if key in range(49, 58):
            number = key - 48  # Convert ASCII to actual number
        
        # Check for numpad keys 1-9 (numpad constants in arcade)
        elif key in (arcade.key.NUM_1, arcade.key.NUM_2, arcade.key.NUM_3,
                    arcade.key.NUM_4, arcade.key.NUM_5, arcade.key.NUM_6,
                    arcade.key.NUM_7, arcade.key.NUM_8, arcade.key.NUM_9):
            # Map numpad keys to numbers 1-9
            numpad_mapping = {
                arcade.key.NUM_1: 1, arcade.key.NUM_2: 2, arcade.key.NUM_3: 3,
                arcade.key.NUM_4: 4, arcade.key.NUM_5: 5, arcade.key.NUM_6: 6,
                arcade.key.NUM_7: 7, arcade.key.NUM_8: 8, arcade.key.NUM_9: 9
            }
            number = numpad_mapping[key]
            
        # Process number input if we have a valid number
        if number is not None:
            x, y = self.selected_cell
            
            # Ensure x and y are integers
            x, y = int(x), int(y)
            
            # Cannot modify given cells
            if (x, y) in self.given_cells:
                return
                
            # Check if the number is correct
            if number == self.solution[y][x]:
                self.user_board[y][x] = number
                if self.check_win():
                    # Add points for solving the puzzle
                    puzzle_points = DIFFICULTY_POINTS[self.difficulty]
                    self.score += puzzle_points
                    self.streak[self.difficulty] += 1
                    
                    # Update high score if needed
                    if self.score > self.high_score:
                        self.high_score = self.score
                    
                    # Show congratulations screen
                    self.show_congrats = True
            else:
                self.lives -= 1
                if self.lives == 0:
                    self.streak[self.difficulty] = 0
                    self.show_menu = True
        
        # 'R' key to reset the game
        elif key == 114:  # ASCII for 'r'
            self.setup(self.difficulty)
        
        # ESC key to show menu
        elif key == arcade.key.ESCAPE:
            self.show_menu = True

    def check_win(self):
        for y in range(9):
            for x in range(9):
                if self.user_board[y][x] != self.solution[y][x]:
                    return False
        return True

def main():
    game = SudokuGame()
    arcade.run()

if __name__ == "__main__":
    main()