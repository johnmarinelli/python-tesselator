#!/usr/bin/python

import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay
import triangle_roi_utility as roi_util

keypoints = []

#def create_rect_linear_gradient(mat, colorFrom, colorTo):
#    # opencv is row-major so dimensions are height, width.  fucked up right?
#    width = mat.shape[1]
#    height = mat.shape[0]
#
#    #http://stackoverflow.com/questions/25622612/linear-color-gradient-in-opencv
#    def get_color_val(row, height, colorValFrom, colorValTo):
#        return (row*colorValFrom+(height-row)*colorValTo) / height
#
#    for row in range(0, height):
#        colorR = get_color_val(row, height, colorFrom[0], colorTo[0])
#        colorG = get_color_val(row, height, colorFrom[1], colorTo[1])
#        colorB = get_color_val(row, height, colorFrom[2], colorTo[2])
#
#        color = colorR, colorG, colorB
#
#        for col in range(0, width):
#            mat[row][col] = color
#
def store_point(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        keypoints.append([x,y])
        cv2.circle(img, (x, y), 1, (255, 255, 255), -1)
    elif event == cv2.EVENT_RBUTTONDOWN:
        do_delaunay()

def do_delaunay():
    global keypoints
    local_keypoints = list(keypoints)
    keypoints = []

    if len(local_keypoints) > 3:
        delaunay_points = np.array(local_keypoints)
        triangles = Delaunay(delaunay_points)

        for triangle in delaunay_points[triangles.simplices]:
            try:
                # triangle: [x,y]
                corner1 = triangle[0]
                col1 = img[corner1[0]][corner1[1]]
                
                corner2 = triangle[1]
                col2 = img[corner2[0]][corner2[1]]

                corner3 = triangle[2]
                col3 = img[corner3[0]][corner3[1]]

                oX = (corner1[0]+corner2[0]+corner3[0])/3
                oY = (corner1[1]+corner2[1]+corner3[1])/3

                avg = img[oX][oY]
                avgr = avg[0]
                avgg = avg[1]
                avgb = avg[2]

                col = (int(avgr), int(avgg), int(avgb))
                print triangle
                roi_util.color_triangle_in_image(triangle, img)
#                cv2.fillPoly(img, np.array([triangle], np.int32), col)
            except IndexError:
                print '' 

img = cv2.imread('shibe.jpg', -1)
cv2.namedWindow('image')
cv2.setMouseCallback('image', store_point)

while(True):
    cv2.imshow('image', img)
    if cv2.waitKey(20) & 0xFF == 27:
        break

cv2.destroyAllWindows()
