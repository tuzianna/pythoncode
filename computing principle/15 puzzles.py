"""
Loyd's Fifteen puzzle - solver and visualizer
Note that solved configuration has the blank (zero) tile in upper left
Use the arrows key to swap this tile with its neighbors
"""

import poc_fifteen_gui

#for m * n grid
# only applies to move tiles with row > m - 2 and col > 0
MOVE = {'left' : ('ulldr','dllur'),
        'right': ('urrdl', 'drrul'),
        'down': ('lddru', 'rddlu')
        }

class Puzzle:
    """
    Class representation for the Fifteen puzzle
    """

    def __init__(self, puzzle_height, puzzle_width, initial_grid=None):
        """
        Initialize puzzle with default height and width
        Returns a Puzzle object
        """
        self._height = puzzle_height
        self._width = puzzle_width
        self._grid = [[col + puzzle_width * row
                       for col in range(self._width)]
                      for row in range(self._height)]

        if initial_grid != None:
            for row in range(puzzle_height):
                for col in range(puzzle_width):
                    self._grid[row][col] = initial_grid[row][col]

    def __str__(self):
        """
        Generate string representaion for puzzle
        Returns a string
        """
        ans = ""
        for row in range(self._height):
            ans += str(self._grid[row])
            ans += "\n"
        return ans

    #####################################
    # GUI methods

    def get_height(self):
        """
        Getter for puzzle height
        Returns an integer
        """
        return self._height

    def get_width(self):
        """
        Getter for puzzle width
        Returns an integer
        """
        return self._width

    def get_number(self, row, col):
        """
        Getter for the number at tile position pos
        Returns an integer
        """
        return self._grid[row][col]

    def set_number(self, row, col, value):
        """
        Setter for the number at tile position pos
        """
        self._grid[row][col] = value

    def clone(self):
        """
        Make a copy of the puzzle to update during solving
        Returns a Puzzle object
        """
        new_puzzle = Puzzle(self._height, self._width, self._grid)
        return new_puzzle

    ########################################################
    # Core puzzle methods

    def current_position(self, solved_row, solved_col):
        """
        Locate the current position of the tile that will be at
        position (solved_row, solved_col) when the puzzle is solved
        Returns a tuple of two integers        
        """
        solved_value = (solved_col + self._width * solved_row)

        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col] == solved_value:
                    return (row, col)
        assert False, "Value " + str(solved_value) + " not found"

    def update_puzzle(self, move_string):
        """
        Updates the puzzle state based on the provided move string
        """
        zero_row, zero_col = self.current_position(0, 0)
        for direction in move_string:
            if direction == "l":
                assert zero_col > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col - 1]
                self._grid[zero_row][zero_col - 1] = 0
                zero_col -= 1
            elif direction == "r":
                assert zero_col < self._width - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col + 1]
                self._grid[zero_row][zero_col + 1] = 0
                zero_col += 1
            elif direction == "u":
                assert zero_row > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row - 1][zero_col]
                self._grid[zero_row - 1][zero_col] = 0
                zero_row -= 1
            elif direction == "d":
                assert zero_row < self._height - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row + 1][zero_col]
                self._grid[zero_row + 1][zero_col] = 0
                zero_row += 1
            else:
                assert False, "invalid direction: " + direction

    ##################################################################
    # Phase one methods

    def lower_row_invariant(self, target_row, target_col):
        """
        Check whether the puzzle satisfies the specified invariant
        at the given position in the bottom rows of the puzzle (target_row > 1)
        Returns a boolean
        """
        # replace with your code
        assert target_row < self._height and target_row >= 0, "row out of grid"
        assert target_col < self._width and target_col >= 0, "column out of grid"

        
        zero_row, zero_col = self.current_position(0, 0)
        
        boolean_1 = True
        for row in range(target_row + 1, self._height):
            for col in range(self._width):
                if self._grid[row][col] != col + row * self._width:
                    boolean_1 = False
                    break
            if boolean_1 == False:
                break
        
        boolean_2 = True        
        if target_col < self._width - 1:
            for col in range(target_col + 1, self._width):
                if self._grid[target_row][col] != col + target_row * self._width:
                    boolean_2 = False
                    break
                    
        return (zero_row, zero_col) == (target_row, target_col) and boolean_1 and boolean_2


    def solve_interior_tile(self, target_row, target_col):
        """
        Place correct tile at target position
        Updates puzzle and returns a move string
        """
        assert target_row > 1, "this method only applied to tiles with row > 1"
        assert target_col > 0, "this method only applied to tiles with col > 0"
        assert self.lower_row_invariant(target_row, target_col) == True, "only applies when self.lower_row_invariant(target_row, target_col) == True"
        
        ans = ""
        row, col = self.current_position(target_row, target_col)
        row_dis = target_row - row
        col_dis = col - target_col
        if row_dis == 0:
            ans += 'l' * abs(col_dis)
            ans += MOVE['right'][0] * (abs(col_dis) - 1)
        else:
            ans += 'u' * row_dis
            if col_dis != 0:
                if col_dis > 0:
                    ans += 'r' * col_dis
                    if row == 0:
                        ans += MOVE['left'][1] * (col_dis - 1)
                        ans += 'dlu'
                        ans += MOVE['down'][0] * (row_dis - 1)
                    else:
                        ans += MOVE['left'][0] * (col_dis - 1)
                        ans += 'ul'
                        ans += MOVE['down'][0] * row_dis
                else:
                    ans += 'l' * abs(col_dis)
                    if row == 0:
                        ans += MOVE['right'][1] * (abs(col_dis) - 1)  
                    else:
                        ans += MOVE['right'][0] * (abs(col_dis) - 1)                    
                    # adjust to prepare for move down
                    ans += 'dru'
                    # move down
                    ans += MOVE['down'][0] * (row_dis - 1)
            else:
                ans += MOVE['down'][0] * (row_dis - 1)
            # so that lower_row_invariant(target_row, target_col - 1) == True
            ans += 'ld'
        self.update_puzzle(ans)
        return ans

    def solve_col0_tile(self, target_row):
        """
        Solve tile in column zero on specified row (> 1)
        Updates puzzle and returns a move string
        """
        # replace with your code
        assert target_row > 1, "only applies to target_row > 1"
        assert self.lower_row_invariant(target_row, 0) == True, "only applies when self.lower_row_invariant(target_row, 0) == True"
        
        ans = ''
        row, col = self.current_position(target_row, 0)
        
        row_dis = target_row - row
        col_dis = col
        # if target is above tile 0, directly move it down
        if row_dis ==  1:
            if col_dis == 0:
                ans += 'u'
            elif col_dis == 1:
                ans += 'u'
                ans += "ruldrdlurdluurddlu"
            else:
                ans += 'u'
                ans += 'r' * col_dis
                ans += MOVE['left'][0] * (col_dis - 2)
                ans += 'ulld'
                ans += "ruldrdlurdluurddlu"
        # if target if in column 0
        else:
            if col_dis == 0:
            # first move tile 0 to column 1
                ans += 'ur'
            # move tile 0 to the right of the targeted tile
                ans += 'u' * (row_dis - 1)
            # move targeted tile to column 1
                ans += 'l'
                ans += 'dru'
                ans += MOVE['down'][0] * (row_dis - 2)                
            elif col_dis == 1:
            # move tile 0 to the left of the targeted tile
                ans += 'u' * row_dis
                ans += 'dru'
                ans += MOVE['down'][0] * (row_dis - 2)
            else:
            # move tile 0 to the left of the targeted tile
                ans += 'u' * row_dis
                ans += 'r' * col_dis
                if row == 0:
                    ans += MOVE['left'][1] * (col_dis - 2)   
                else:
                    ans += MOVE['left'][0] * (col_dis - 2)
                ans += 'dlu'
                ans += MOVE['down'][0] * (row_dis - 2)
        # tile 0 should be to the left of targeted tile
        # and the resolve string        
            ans += 'ld'
            ans += "ruldrdlurdluurddlu"
        # move tile 0 to the right most of target_row - 1
        ans += 'r' * (self._width - 1)
        self.update_puzzle(ans)
        return ans

    #############################################################
    # Phase two methods

    def row0_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row zero invariant
        at the given column (col > 1)
        Returns a boolean
        """
        # replace with your code
        assert target_col < self._width, "target_col out of grid"
        
        bool_1 = self._grid[0][target_col] == 0
        if bool_1 == True:
            bool_2 = True
            for dummy in range(target_col + 1, self._width):
                if self._grid[0][dummy] != dummy:
                    bool_2 = False
                    break

            bool_3 = True
            for dummy in range(target_col, self._width):
                if self._grid[1][dummy] != dummy + self._width:
                    bool_2 = False
                    break

            bool_4 = True
            for dummy_i in range(2, self._height):
                for dummy_j in range(self._width):
                    if self._grid[dummy_i][dummy_j] != dummy_j + dummy_i * self._width:
                        bool_4 = False
                        break
                if bool_4 == False:
                    break
            return bool_2 and bool_3 and bool_4
        return bool_1

    def row1_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row one invariant
        at the given column (col > 1)
        Returns a boolean
        """
        # replace with your code
        assert target_col < self._width, "target_col out of grid"
        
        bool_1 = self._grid[1][target_col] == 0
        
        if bool_1 == True:
            bool_2 = True
            for row in range(2):
                for col in range(target_col + 1, self._width):
                    if self._grid[row][col] != col + row * self._width:
                        bool_2 = False
                        break
                if bool_2 == False:
                    break
                    
            bool_3 = True
            for dummy_i in range(2, self._height):
                for dummy_j in range(self._width):
                    if self._grid[dummy_i][dummy_j] != dummy_j + dummy_i * self._width:
                        bool_3 = False
                        break
                if bool_3 == False:
                    break
                    
            return bool_1 and bool_2 and bool_3
        
        return bool_1

    def solve_row0_tile(self, target_col):
        """
        Solve the tile in row zero at the specified column
        Updates puzzle and returns a move string
        """
        # replace with your code
        assert target_col > 1, "target_col > 1"
        assert self.row0_invariant(target_col) == True, "self.row0_invariant(target_col) != True"
        
        row, col = self.current_position(0, target_col)
        row_dis = row
        col_dis = target_col - col
        
        ans = ''
        if col_dis == 1:
            if row_dis == 0:
                ans += 'ld' 
            else:
                ans += 'lld'
                ans += "urdlurrdluldrruld"
        else:
            if row_dis == 0:
                ans += 'ld'
                ans += 'l' * (col_dis - 1)
                ans += 'u'
                ans += 'rdl'
                ans += MOVE['right'][0] * (col_dis - 2)
            else:
                ans += 'l' * col_dis
                ans += 'rdl'
                ans += MOVE['right'][0] * (col_dis - 2)
            ans += "urdlurrdluldrruld"
            
        self.update_puzzle(ans)
        return ans

    def solve_row1_tile(self, target_col):
        """
        Solve the tile in row one at the specified column
        Updates puzzle and returns a move string
        """
        # replace with your code
        assert target_col > 1, "target_col > 1"
        assert self.row1_invariant(target_col) == True, "self.row1_invariant(target_col) != True"
        
        row, col = self.current_position(1, target_col)
        row_dis = 1 - row
        col_dis = target_col - col      
        ans = ''
        if row_dis == 0:
            ans += 'l' * col_dis
            ans += MOVE['right'][0] * (col_dis - 1)
            ans += 'ur'
        else:
            if col_dis == 0:
                ans += 'u'
            else:
                ans += 'l' * col_dis
                ans += 'u'
                ans += 'rdl'
                ans += MOVE['right'][0] * (col_dis - 1)
                ans += 'ur'
        self.update_puzzle(ans)
        
        return ans

    ###########################################################
    # Phase 3 methods

    def solve_2x2(self):
        """
        Solve the upper left 2x2 part of the puzzle
        Updates the puzzle and returns a move string
        """
        # replace with your code
        assert self.row1_invariant(1) == True, "not ready yet"
        ans = ""
        ans += 'lu'
        self.update_puzzle('lu')
        count = 0
        resolved = self.get_number(0,1) == 1 and self.get_number(1,0) == self._width and self.get_number(1,1) == 1 + self._width
        while not resolved:
            count += 1
            self.update_puzzle('rdlu')
            resolved = self.get_number(0,1) == 1 and self.get_number(1,0) == self._width and self.get_number(1,1) == 1 + self._width
            
        ans += 'rdlu' * count 
        return ans

    def solve_puzzle(self):
        """
        Generate a solution string for a puzzle
        Updates the puzzle and returns a move string
        """
        # replace with your code
        assert self._height > 1 and self._width > 1, "dimension should at least be 2 x 2"
        
        ans = ""
        row, col = self.current_position(0,0)
        row_dis = self._height - 1 - row
        col_dis = self._width - 1 - col
        
        ans += 'r' * col_dis + 'd' * row_dis
        self.update_puzzle(ans)
        
        for dum_i in range(self._height - 1, 1, -1):
            for dum_j in range(self._width - 1, -1, -1):
                if dum_j > 0:
                    ans += self.solve_interior_tile(dum_i, dum_j)
                else:
                    ans += self.solve_col0_tile(dum_i)
                
        for dum_j in range(self._width - 1, 1, -1):
            for dum_i in range(1, -1, -1):
                if dum_i == 0:
                    ans += self.solve_row0_tile(dum_j)
                else:
                    ans += self.solve_row1_tile(dum_j)
                    
        ans += self.solve_2x2()
        
        return ans

# Start interactive simulation

