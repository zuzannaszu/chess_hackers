import math
import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageColor

def display_hough_lines(img, lines):
    """Display the hough lines created byt the hough lines detector"""
    plt.figure()
    img_line = img.copy()
    if lines is not None:
        for i in range(0, len(lines)):
            rho = lines[i][0][0]
            theta = lines[i][0][1]
            a = math.cos(theta)
            b = math.sin(theta)
            x0 = a * rho
            y0 = b * rho
            pt1 = (int(x0 + 1500*(-b)), int(y0 + 1500*(a)))
            pt2 = (int(x0 - 1500*(-b)), int(y0 - 1500*(a)))
            cv.line(img_line, pt1, pt2, (0,0,152), 3, cv.LINE_AA)
    plt.imshow(img_line)
    plt.show(block=False)

def display_filtered_lines(horizontal, vertical, total, img):
    """Required the three output of the line filtering function as well as the image"""

    if total is not None:
        plt.figure()
        plt.title(f"board")
        x = np.linspace(0, img.shape[1],total)
        x_h = horizontal["slope"].tolist()
        y_h = horizontal["intercept"].tolist()
        for i in range(len(x_h)):
            y = x_h[i] * x + y_h[i]
            plt.plot(x, y, '-r', label = f"line{i}")
            ax = plt.gca()
            ax.set_xlim([0, img.shape[1]])
            ax.set_ylim([img.shape[0], 0])

        vert = vertical["Rho"].tolist()
        x_v = vertical["slope"].tolist()
        y_v = vertical["intercept"].tolist()
        for i in range(len(x_v)):
            if x_v[i] == np.inf or x_v[i] == -np.inf:
                plt.axvline(x = vert[i], color = 'b')
            else:
                y = x_v[i] * x + y_v[i]
                plt.plot(x, y, '-b', label = f"line{i}")
        plt.imshow(img)

def display_intersection(inter, img, horizontal, vertical):
    """input are the image, the ouput of the intersection calculation and the dataframe from the line filtering function"""

    x = np.linspace(0,1500)

    if inter is not None:
        plt.figure()
        plt.title(f"board")
        img_2 = Image.fromarray(img)
        for i in range(len(inter[0])):
            text = f"{i}"
            x1 = inter[0][i]
            y1 = inter[1][i]
            plt.plot(x1,y1, marker="o", markersize=7, markerfacecolor="black")
            ax = plt.gca()
            ax.set_xlim([0, img.shape[1]])
            ax.set_ylim([img.shape[1], 0])
            draw = ImageDraw.Draw(img_2)
            font_type = ImageFont.truetype("arial.ttf", 40)
            draw.text((x1+20,y1+20),text, font=font_type, fill=255)

        x_h = horizontal["slope"].tolist()
        y_h = horizontal["intercept"].tolist()
        vert = vertical["Rho"].tolist()
        x_v = vertical["slope"].tolist()
        y_v = vertical["intercept"].tolist()

        for i in range(len(x_h)):
            y = x_h[i] * x + y_h[i]
            plt.plot(x, y, '-r', label = f"line{i}")
            ax = plt.gca()
            ax.set_xlim([0, img.shape[1]])
            ax.set_ylim([img.shape[0], 0])

        for i in range(len(x_v)):
            if x_v[i] == np.inf or x_v[i] == -np.inf:
                plt.axvline(x = vert[i], color = 'b')
            else:
                y = x_v[i] * x + y_v[i]
                plt.plot(x, y, '-b', label = f"line{i}")
        plt.imshow(img_2, cmap="gray")

def displaying_coordinates(img, coordinate):
    if coordinate is not None:
        img_3 = Image.fromarray(img)
        plt.figure()
        for key, value in coordinate.items():
            text = key
            pos = (value[0]-100, value[1]-100)
            draw = ImageDraw.Draw(img_3)
            font_type = ImageFont.truetype("arial.ttf", 50)
            draw.text(pos,text, font=font_type, fill=255)
        plt.imshow(img_3)
