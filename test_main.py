import matplotlib.pyplot as plt
import cv2 as cv
from Python_files.utils import edge_detector, hough_lines_detector, filtering_lines, intersection_calculation, coordinate_generator, image_cropping, save_cropped_img
from Python_files.Display_func import display_hough_lines, display_filtered_lines, display_intersection, displaying_coordinates

display = 1

img_path = "/home/thierry/code/zuzannaszu/chess_hackers/Raw_Data/Final_boards/Board1.jpg"
img = cv.imread(img_path, 1)
img = cv.resize(img,(1280, 1280), interpolation = cv.INTER_AREA)

edge = edge_detector(img, 80, 300)

if display == 1:
    plt.imshow(edge)

lines = hough_lines_detector(img, edge)

if display == 1:
    display_hough_lines(img, lines)

horizontal_lines, vertical_lines, total_lines = filtering_lines(lines)

if display == 1:
    display_filtered_lines(horizontal_lines, vertical_lines, total_lines, img)

intersections, intersections_df = intersection_calculation(horizontal_lines, vertical_lines)

if display == 1:
    display_intersection(intersections,img,horizontal_lines, vertical_lines)

coordinates = coordinate_generator(intersections_df)

if display == 1:
    displaying_coordinates(img, coordinates)

cropped_imgs = image_cropping(intersections, img,40)

save_path = "/home/thierry/code/zuzannaszu/chess_hackers/Test_save/"

save_cropped_img(cropped_imgs, save_path, coordinates)
