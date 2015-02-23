#!/usr/bin/python

import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay

img = cv2.imread('shibe.jpg',1)

surf = cv2.SURF(400)

kp, des = surf.detectAndCompute(img, None)
delaunay_points = []

for x in range(0, len(kp)):
    delaunay_points.append([kp[x].pt[0], kp[x].pt[1]])

print delaunay_points
delaunay_points = np.array(delaunay_points)
tri = Delaunay(delaunay_points)

plt.triplot(delaunay_points[:,0], delaunay_points[:,1], tri.simplices.copy())
plt.plot(delaunay_points[:,0], delaunay_points[:,1], 'o')

color = 0;

for tri in delaunay_points[tri.simplices]:
    col = img[tri[0][0]][tri[0][1]][0]
    cv2.fillPoly(img, np.array([tri], np.int32), int(col))

plt.imshow(img)
plt.show()
