"""
Mini-max Tic-Tac-Toe Player
"""

import poc_ttt_gui
import poc_ttt_provided as provided
import random

# Set timeout, as mini-max can take a long time
import codeskulptor
codeskulptor.set_timeout(150)

# SCORING VALUES - DO NOT MODIFY
SCORES = {provided.PLAYERX: 1,
          provided.DRAW: 0,
          provided.PLAYERO: -1}

def mm_move(board, player):
    """
    Make a move on the board.
    
    Returns a tuple with two elements.  The first element is the score
    of the given board and the second element is the desired move as a
    tuple, (row, col).
    """
    empty_squares = board.get_empty_squares()
    if len(empty_squares) == 0:
        winner = board.check_win()
        return SCORES[winner], (-1,-1)
    else:
        dummy = {}
        for square in empty_squares:
            current_board = board.clone()
            current_board.move(square[0], square[1], player)
            winner = current_board.check_win()
            if winner != player:
                other_player = provided.switch_player(player)
                moves = mm_move(current_board, other_player)
                dummy[moves[0]] = dummy.get(moves[0], [])
                dummy[moves[0]].append(square)
            else:
                return SCORES[winner], square        
        dum = dummy.keys()
        min_dum = min(dum)
        max_dum = max(dum)
        if player == provided.PLAYERX:
            return max_dum, dummy[max_dum][random.randrange(len(dummy[max_dum]))]
        if player == provided.PLAYERO:
            return min_dum, dummy[min_dum][random.randrange(len(dummy[min_dum]))]
    
                
def move_wrapper(board, player, trials):
    """
    Wrapper to allow the use of the same infrastructure that was used
    for Monte Carlo Tic-Tac-Toe.
    """
    move = mm_move(board, player)
    assert move[1] != (-1, -1), "returned illegal move (-1, -1)"
    return move[1]

# Test game with the console or the GUI.
# Uncomment whichever you prefer.
# Both should be commented out when you submit for
# testing to save time.

#provided.play_game(move_wrapper, 1, False)        
#poc_ttt_gui.run_gui(3, provided.PLAYERO, move_wrapper, 1, False)


