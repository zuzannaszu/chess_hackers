import cv2 as cv
import numpy as np
import pandas as pd
import math

def edge_detector(img, lower, upper):
    """Return the edges used for the Hough lines detection.
    args: lower and upper are values for the Canny edge detector.
    Returns teh edges as numpy arrays
    """
    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    blur = cv.blur(img,(3,3),0)
    edge = cv.Canny(blur, lower, upper) #70,250 for old
    kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE,(3,3))
    dilated = cv.dilate(edge, kernel, iterations=2)
    return dilated

def hough_lines_detector(img, edge):
    """Hough line detector. Requires edge detector output. Returns all the lines in polar coordinates."""
    v = int(np.median(img))
    lines = cv.HoughLines(edge, 1, np.pi/180, v*3)
    return lines

def filtering_lines(lines):
    if lines is not None:

        df = pd.DataFrame(lines[:,0,:]).rename(columns={0: "Rho", 1: "Theta"})
        df["diff"] = df["Rho"].diff() + 10*np.abs(df["Theta"].diff())
        new_lines = df
        new_lines["a"] = new_lines["Theta"].apply(math.cos)
        new_lines["b"] = new_lines["Theta"].apply(math.sin)
        new_lines["slope"] = -new_lines["a"]/new_lines["b"]
        new_lines["intercept"] = new_lines["Rho"]/new_lines["b"]

        mask_vert = (np.abs(new_lines["a"]) > 0.97) & (np.abs(new_lines["b"]) < 0.4 )
        mask_vert_2 = new_lines.isin([np.inf]).any(axis=1)
        mask_horizontal = (np.abs(new_lines["a"]) < 0.97) & (np.abs(new_lines["b"]) > 0.9 )
        vertical_2 = new_lines[mask_vert_2 + mask_vert]
        horizontal = new_lines[mask_horizontal]

        horizontal = horizontal.sort_values(by="intercept")
        horizontal["diff"] = horizontal["intercept"].diff()
        horizontal_f = horizontal[(horizontal["diff"]>55) | horizontal["diff"].isna()]

        vertical_2["x_intercept"] = vertical_2["Rho"].abs()
        vertical_2 = vertical_2.sort_values(by="x_intercept")
        vertical_2["diff"] = np.abs(vertical_2["x_intercept"]).diff()
        vertical_2_f = vertical_2[(vertical_2["diff"] > 40) | (vertical_2["diff"].isna())]

        return horizontal_f, vertical_2_f, len(new_lines)

    else: return None, None, None


def intersection(line1, line2):
    if np.inf not in [line1[0], line1[1], line2[0], line2[1]] or -np.inf not in [line1[0], line1[1], line2[0], line2[1]]:
        x0 = (line2[1] - line1[1]) / (line1[0] - line2[0])
        y0 = line1[0] * x0 + line1[1]
    else:
        if np.inf in line1 or -np.inf in line1:
            linev = line1
            linenv = line2
        else:
            linev = line2
            linenv = line1
        x0 = linev[2]
        y0 = linenv[0] * x0 + linenv[1]

    return x0, y0

def intersection_calculation(horizontal, vertical):
    """input are two dataframes created by the filtering_line function. Output a tuple of list of coordinates and a dataframe of the same coordinates"""
    if vertical is not None:

        intersections_p = []
        total_lines = pd.concat([horizontal, vertical])

        x_l = total_lines["slope"]
        y_l = total_lines["intercept"]
        r_l = total_lines["Rho"]

        for x1,y1,r1 in zip(x_l, y_l, r_l):
            for x2,y2,r2 in zip(x_l, y_l, r_l):
                line1 = (x1, y1, r1)
                line2 = (x2, y2, r2)
                if line1 != line2:
                    if line1[0] - line2[0] != 0:
                        x0, y0 = intersection(line1, line2)
                        intersections_p.append((round(x0,0), round(y0,0)))

        intersections_pd = pd.DataFrame(intersections_p)
        intersections_pd = intersections_pd[intersections_pd>0][intersections_pd<1400].dropna().drop_duplicates().reset_index()
        x_in = intersections_pd[0].to_list()
        y_in = intersections_pd[1].to_list()

        return (x_in, y_in), intersections_pd

    else: return (None, None), None

def coordinate_generator(inter):
    """input is a dataframe output by the intersection calculation funtion.
    Requires change so A0 can be setup differently"""
    if inter is not None:
        if len(inter) > 80:
            inter = inter.drop(columns="index")
            A0 = inter.loc[0].to_list()
            coordinate = {}
            letters = ["A", "B", "C", "D", "E", "F", "G", "H"]
            i = 0
            for col in letters:
                for line in range(8):
                    val = inter.loc[10+i + 9*line].to_list()
                    text = f"{col}{line}"
                    coordinate[text] = val
                i += 1
        return coordinate
    else: return None

def image_cropping(square, img_plus, padding=0):
    """imput are the list of tuples created in the intersection_calculation funtion and the picture taken. Additionaly, the padding can be specified"""

    if square is not None:
        corner_sq = []
        crop_imgs = []

        for lin in range(8):
            for col in range(8):

                corner_1 = [int(square[0][col+ 9 * lin]), int(square[1][col+ 9 * lin])]
                corner_2 = [int(square[0][col + 1+ 9 * lin]), int(square[1][col + 1+ 9 * lin])]
                corner_3 = [int(square[0][col + 9*(lin+1) + 1]), int(square[1][col + 9*(lin+1) + 1])]
                corner_4 = [int(square[0][col + 9*(lin+1)]), int(square[1][col + 9*(lin+1)])]
                corner_sq = [corner_1, corner_2, corner_3, corner_4]

                crop_img = img_plus[max(corner_1[1]-padding,0):corner_3[1]+int(padding/2), max(corner_1[0]-int(padding/2),0):corner_2[0]+int(padding)]
                crop_imgs.append(crop_img)

        return crop_imgs
    return None

def save_cropped_img(crop_imgs, save_path, coordinates):
    """input is the list of all the cropped images created in the image_cropping function"""
    if coordinates is not None:
        for img, coordinate in zip(crop_imgs, coordinates.keys()):
            name = f"crop-{coordinate}.jpg"
            #print(save_path + name)
            cv.imwrite(save_path + name, img)
    else: print("What is going on!?")
