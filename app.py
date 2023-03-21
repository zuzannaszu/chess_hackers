import streamlit as st
import cv2 as cv
from Python_files.utils import edge_detector, hough_lines_detector, filtering_lines, intersection_calculation, coordinate_generator, image_cropping, save_cropped_img
from Python_files.Display_func import display_hough_lines, display_filtered_lines, display_intersection, displaying_coordinates
from Python_files.Model import select_image, generate_dict, prep_imgs, make_predict
import chess
from Python_files.move_predict import evaluate, get_coordinate, get_piece, dict_to_list_of_tuples, minimax, get_best_move
import glob
import tensorflow as tf
import base64

@st.cache_resource
def read_model():

    bucket_name = 'chess_model_032023'
    model_path = 'chessmodel.h5'
    url = f'gs://{bucket_name}/{model_path}'

    model = tf.keras.models.load_model(url)
    return model

def render_svg(svg):
    """Renders the given svg string."""
    b64 = base64.b64encode(svg.encode('utf-8')).decode("utf-8")
    html = r'<img src="data:image/svg+xml;base64,%s"/>' % b64
    return html


st.text('''Chess board detection and move prediction''')
st.markdown("""---""")

img_path = "streamlit_data/Board56.jpg"
st.text(f"Picture of the board {img_path[-6:-4]}")

img = cv.imread(img_path, -1)
img = cv.resize(img,(1280, 1280), interpolation = cv.INTER_AREA)

b,g,r = cv.split(img)
rgb_img = cv.merge([r,g,b])

st.image(rgb_img, width=500)

st.markdown("""---""")
white_bottom = False

st.text("Option to choose")

white_bottom = st.checkbox("White at the bottom?")
option = st.selectbox('Which player to play?',('white', 'black'))

run_code = st.button("generate")

model = read_model()

if run_code:

    edge = edge_detector(rgb_img, 80, 300)

    lines = hough_lines_detector(img, edge)

    horizontal_lines, vertical_lines, total_lines = filtering_lines(lines)

    intersections, intersections_df = intersection_calculation(horizontal_lines, vertical_lines)


    #st.markdown("""---""")

    #st.text("Coordinate generator")

    coordinates = coordinate_generator(intersections_df, white_bottom)

    img_coor = displaying_coordinates(rgb_img, coordinates)

    #st.image(img_coor)

    crop_imgs = image_cropping(intersections, img, white_bottom, 40)

    #save_path = "streamlit_data/crop_img/"

    #save_cropped_img(crop_imgs, save_path, coordinates)

    #-------------Model stuffs--------------------------------

    #crop_path = sorted(glob.glob(save_path + "*.jpg"))

    #crop_imgs = select_image(crop_path)

    images = prep_imgs(crop_imgs)

    output_dict = make_predict(model, images, coordinates)

    #-------------Move predict--------------------------------

    st.markdown("""---""")

    #st.text("reconstructed")

    board = chess.Board()

    player_turn = option

    my_list = dict_to_list_of_tuples(output_dict)

    board._clear_board()

    for s,p,c in my_list:
        board._set_piece_at(square=s,piece_type=p,color=c)

    board.push(get_best_move(board, 1, option))
    board.pop()

    boardsvg = chess.svg.board(board, lastmove=get_best_move(board, 1, option))

    board_img = render_svg(boardsvg)

    col1, col2= st.columns(2)

    with col1:
        st.header("Original board")
        st.image(rgb_img)

    with col2:
        st.header("Reconstructed board")
        st.write(board_img, unsafe_allow_html=True)

    st.text(f"The recommended move is {get_best_move(board, 1, option)}")
