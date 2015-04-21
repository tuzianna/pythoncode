"""
    Monte Carlo Tic-Tac-Toe Player
    """

import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# You may change the values of these constants as desired, but
#  do not change their names.
NTRIALS = 50        # Number of trials to run
SCORE_CURRENT = 1.0 # Score for squares played by the current player
SCORE_OTHER = 1.0   # Score for squares played by the other player


# Add your functions here.
def is_game_over(board):
    """
        if there is a winner or it is a tie, the game is over
        """
    return board.check_win() != None


def select_move(board):
    """
        select a random empty sqaure to be the next move
        """
    empty_squares = board.get_empty_squares()
    num = len(empty_squares)
    return empty_squares[random.randrange(num)]


def get_max_score(board, scores):
    """
        helper function for best move
        """
    max_score = None
    empty_squares = board.get_empty_squares()
    for square in empty_squares:
        if max_score == None:
            max_score = scores[square[0]][square[1]]
        elif max_score < scores[square[0]][square[1]]:
            max_score = scores[square[0]][square[1]]
    return max_score


def mc_trial(board, player):
    """
        play the game until there is a winner
        or it is a tie
        meaning one trial or game is over
        """
    if not is_game_over(board):
        square = select_move(board)
        board.move(square[0], square[1], player)
        while not is_game_over(board):
            square = select_move(board)
            player = provided.switch_player(player)
            board.move(square[0], square[1], player)


def mc_update_scores(scores, board, player):
    """
        if the game is a tie, update every square with score 0
        if player wins, update square wiht player's move with SCORE_CURRENT
        and update squares with other player's move with -SCORE_OTHER
        
        and vice versa
        """
    dim = board.get_dim()
    if board.check_win() != provided.DRAW:
        winner = board.check_win()
        if winner == player:
            for dummy_i in range(dim):
                for dummy_j in range(dim):
                    if board.square(dummy_i, dummy_j) == player:
                        scores[dummy_i][dummy_j] += SCORE_CURRENT
                    elif board.square(dummy_i, dummy_j) != provided.EMPTY:
                        scores[dummy_i][dummy_j] += -SCORE_OTHER
        else:
            for dummy_i in range(dim):
                for dummy_j in range(dim):
                    if board.square(dummy_i, dummy_j) == player:
                        scores[dummy_i][dummy_j] += -SCORE_CURRENT
                    elif board.square(dummy_i, dummy_j) != provided.EMPTY:
                        scores[dummy_i][dummy_j] += SCORE_OTHER


def get_best_move(board, scores):
    """
        select any of the sqaure with best score
        """
    moves = []
    max_score = get_max_score(board, scores)
    empty_squares = board.get_empty_squares()
    for square in empty_squares:
        if scores[square[0]][square[1]] == max_score:
            moves.append(square)
    
    return moves[random.randrange(len(moves))]



def mc_move(board, player, trials):
    """
        play the game multiple times
        and update the score
        """
    dim = board.get_dim()
    scores = [[0 for dummy_j in range(dim)] for dummy_i in range(dim)]
    for dummy in range(trials):
        new_board = board.clone()
        current_player = player
        mc_trial(new_board, current_player)
        mc_update_scores(scores, new_board, current_player)
    
    move = get_best_move(board, scores)
    return move


# Test game with the console or the GUI.  Uncomment whichever
# you prefer.  Both should be commented out when you submit
# for testing to save time.

provided.play_game(mc_move, NTRIALS, False)
poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)
