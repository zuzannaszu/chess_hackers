import streamlit as st
import cv2 as cv
from Python_files.utils import edge_detector, hough_lines_detector, filtering_lines, intersection_calculation, coordinate_generator, image_cropping, save_cropped_img
from Python_files.Display_func import display_hough_lines, display_filtered_lines, display_intersection, displaying_coordinates
import chess
from move_predict import evaluate, get_coordinate, get_piece, dict_to_list_of_tuples, minimax, get_best_move
import cairosvg

st.markdown('''
Chess board detection and move prediction
''')
st.markdown("""---""")

img_path = "/home/thierry/code/zuzannaszu/chess_hackers/Raw_Data/Final_boards/Board48.jpg"
st.text("Picture of the board")

img = cv.imread(img_path, -1)
img = cv.resize(img,(1280, 1280), interpolation = cv.INTER_AREA)

b,g,r = cv.split(img)
rgb_img = cv.merge([r,g,b])

st.image(rgb_img)

edge = edge_detector(img, 80, 300)

lines = hough_lines_detector(img, edge)

horizontal_lines, vertical_lines, total_lines = filtering_lines(lines)

intersections, intersections_df = intersection_calculation(horizontal_lines, vertical_lines)

st.markdown("""---""")

st.text("Option to choose")
white_bottom = False
white_bottom = st.checkbox("White at the bottom?")
option = st.selectbox('Which player to play?',('white', 'black'))

st.markdown("""---""")

st.text("Coordinate generator")

coordinates = coordinate_generator(intersections_df, white_bottom)

img_coor = displaying_coordinates(rgb_img, coordinates)

st.image(img_coor)

#-------------Model stuffs--------------------------------

my_dict = {"A2" : "white_p",
    "A6" : "Black_p",
    "A8" : "Black_r",
    "B2" : "white_p",
    "B7" : "Black_p",
    "C2" : "white_p",
    "C3" : "White_kn",
    "C6" : "Black_b",
    "C7" : "Black_p",
    "D1" : "White_r",
    "D8" : "Black_q",
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

#-------------Move predict--------------------------------

st.markdown("""---""")

st.text("reconstructed")

board = chess.Board()
board._clear_board()

player_turn = option

my_list = dict_to_list_of_tuples(my_dict)

board._clear_board()

for s,p,c in my_list:
    board._set_piece_at(square=s,piece_type=p,color=c)

board.push(get_best_move(board, 1, option))

boardsvg = chess.svg.board(board, lastmove=get_best_move(board, 1, option))
outputfile = open('board.svg', "w")
outputfile.write(boardsvg)

img = cairosvg.svg2png(url='board.svg', write_to='board.png', scale=7)

st.image('board.png')
