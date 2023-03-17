#import packages
import chess.pgn
import chess
import math

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

#get the final function to get the position and the piece together in a list
def dict_to_list_of_tuples(my_dict):
    final_list = []
    for k,v in my_dict.items():
        coord = get_coordinate(k)
        piece, colour = get_piece(v)
        translation = (coord, piece, colour)
        final_list.append(translation)
    return final_list


def minimax(board, depth, alpha, beta, is_maximizing_player):
    if depth == 0 or board.is_game_over():
        return evaluate(board)
    if is_maximizing_player:
        max_eval = -math.inf
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth-1, alpha, beta, False)
            board.pop()
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = math.inf
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth-1, alpha, beta, True)
            board.pop()
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

# Function to get the best move using the minimax algorithm
def get_best_move(board, depth, colour):
    if colour == "white":
        board.turn = chess.WHITE
    else:
        board.turn = chess.BLACK

    best_move = None
    max_eval = -math.inf
    alpha = -math.inf
    beta = math.inf
    for move in board.legal_moves:
        board.push(move)
        eval = minimax(board, depth-1, alpha, beta, False)
        board.pop()
        if eval > max_eval:
            max_eval = eval
            best_move = move
        alpha = max(alpha, eval)
    return best_move

    #push your best move onto the board
#board2.push(get_best_move(board2, 3))

    #show the board with the best move
#board2
