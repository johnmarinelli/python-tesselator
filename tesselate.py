#!/usr/bin/python

import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay

img = cv2.imread('shibe.jpg', -1)
surf = cv2.SURF(400)

# get keypoints of features
kp, des = surf.detectAndCompute(img, None)
delaunay_points = []

# setup points to triangulate (opencv -> numpy)
#for x in range(0, len(kp)):
#    delaunay_points.append([kp[x].pt[0], kp[x].pt[1]])

keypoints = []

for y in range(0, img.shape[0], img.shape[0] / 100):
    for x in range(0, img.shape[1], img.shape[1] / 100):
        keypoint = cv2.KeyPoint(x, y, 1)
        keypoints.append(keypoint)

for i in range(0, len(keypoints)):
    delaunay_points.append([keypoints[i].pt[0], keypoints[i].pt[1]])

delaunay_points = np.array(delaunay_points)

# get triangles
tri = Delaunay(delaunay_points)

#delaunay_points[tri.simplices] gives us an array of all the triangles.  below we plot the points
#plt.triplot(delaunay_points[:,0], delaunay_points[:,1], tri.simplices.copy())
#plt.plot(delaunay_points[:,0], delaunay_points[:,1], 'o')

# for each of these triangles,
# we'll want to create some sort of color gradient from corner to corner
# for ( [x,y], [x,y], [x,y] ) coords in our triangle set
for triangles in delaunay_points[tri.simplices]:
    try:
        # triangle: [x,y]
        corner1 = triangles[0]
        col1 = img[corner1[0]][corner1[1]]
        
        corner2 = triangles[1]
        col2 = img[corner2[0]][corner2[1]]

        corner3 = triangles[2]
        col3 = img[corner3[0]][corner3[1]]

        oX = (corner1[0]+corner2[0]+corner3[0])/3
        oY = (corner1[1]+corner2[1]+corner3[1])/3

        avg = img[oX][oY][0]

        cv2.fillPoly(img, np.array([triangles], np.int32), int(avg))
    except IndexError:
        print ''

plt.imshow(img)
plt.show()
