    #import packages
import chess.pgn
pgn = open("/root/code/zuzannaszu/chess_hacker/lichess_db_standard_rated_2013-01/lichess_db_standard_rated_2013-01.pgn")
chess.pgn.read_game(pgn)
import chess
board = chess.Board()
import math

    #show board
board
    #start from 0
chess.pgn.__file__
board._set_piece_map
board._clear_board()
board
    # Evaluation function to determine the score of a given board state
def evaluate(board):
    score = 0
    for piece in board.piece_map().values():
        if piece.color == chess.BLACK:
            score += piece.piece_type
        else:
            score -= piece.piece_type
    return score

    #transforming dictionnary of coordinate in to readable number combination for chess package
#example of dictionnary for  game

#function to transform the coordinate location
def get_coordinate(coordinate):
    num = int(coordinate[1])
    letter = coordinate[0]
    letter_dict = {'A': 0, 'B': 1, 'C':2, 'D': 3, 'E': 4,
                  'F': 5, 'G': 6, 'H': 7}
    new_coordinate = ( num - 1 ) * 8 + letter_dict[letter]
    return new_coordinate

#function to transform the the piece colour and form
get_coordinate('F1')
def get_piece(piece):
    piece_split = piece.split('_')
    colour = piece_split[0].lower()
    colour_dict = {'black': 0, 'white': 1}
    form = piece_split[1]
    piece_dict = {'p': 1,
                 'r': 4,
                 'kn': 2,
                 'b': 3,
                 'q' :5,
                 'ki': 6
                 }
    new_colour = colour_dict[colour]
    new_piece = piece_dict[form]
    return new_piece, new_colour
get_piece("White_ki")

#get the final function to get the position and the piece together in a list
def dict_to_list_of_tuples(my_dict):
    final_list = []
    for k,v in my_dict.items():
        coord = get_coordinate(k)
        piece, colour = get_piece(v)
        translation = (coord, piece, colour)
        final_list.append(translation)
    return final_list

#example
my_dict = {"D8" : "Black_q",
    "E2" : "White_q",
    "E4" : "white_p",
    "E5" : "Black_p",
    "F1" : "White_r",
    "F2" : "white_p",
    "F3" : "White_kn",
    "F6" : "Black_kn",
    "F7" : "Black_p",
    "F8" : "Black_r",
    "G1" : "White_ki",
    "G2" : "white_p",
    "G5" : "White_b",
    "G6" : "Black_p",
    "G7" : "Black_b",
    "G8" : "Black_ki",
    "H3" : "white_p",

    "H7" : "Black_p"}

my_list = dict_to_list_of_tuples(my_dict)
print(my_list)

    #create a board set
pieces = [(8, 1, 0), (40, 1, 1), (56, 4, 1), (9, 1, 0), (49, 1, 1), (10, 1, 0), (18, 2, 0), (42, 3, 1), (50, 1, 1), (3, 4, 0), (59, 5, 1), (12, 5, 0), (28, 1, 0), (36, 1, 1), (5, 4, 0), (13, 1, 0), (21, 2, 0), (45, 2, 1), (53, 1, 1), (61, 4, 1), (6, 6, 0), (14, 1, 0), (38, 3, 0), (46, 1, 1), (54, 3, 1), (62, 6, 1), (23, 1, 0), (55, 1, 1)]

board._clear_board()

for s,p,c in pieces:
    board._set_piece_at(square=s,piece_type=p,color=c)

board2 = board
board2

    #Predicticting with Minimax & Alpha Bets Pruning
# Minimax algorithm with alpha-beta pruning
def minimax(board2, depth, alpha, beta, is_maximizing_player):
    if depth == 0 or board.is_game_over():
        return evaluate(board)
    if is_maximizing_player:
        max_eval = -math.inf
        for move in board2.legal_moves:
            board2.push(move)
            eval = minimax(board2, depth-1, alpha, beta, False)
            board2.pop()
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = math.inf
        for move in board2.legal_moves:
            board.push(move)
            eval = minimax(board2, depth-1, alpha, beta, True)
            board.pop()
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

# Function to get the best move using the minimax algorithm
def get_best_move(board, depth):
    best_move = None
    max_eval = -math.inf
    alpha = -math.inf
    beta = math.inf
    for move in board2.legal_moves:
        board2.push(move)
        eval = minimax(board2, depth-1, alpha, beta, False)
        board.pop()
        if eval > max_eval:
            max_eval = eval
            best_move = move
        alpha = max(alpha, eval)
    return best_move

    #Select position (BLACK/ WHITE)
board2.turn = chess.WHITE

    #Selext board and Depth (Depth = turn, "1" = next move)
get_best_move(board2, 1)

    #push your best move onto the board
board2.push(get_best_move(board2, 3))

    #show the board with the best move
board2
