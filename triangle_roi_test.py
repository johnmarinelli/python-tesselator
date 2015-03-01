import cv2
import numpy as np

#points: [ [x1,y1], [x2,y2], [x3,y3] ... ]
def get_rect_coords_from_points(points):
    # find leftmost point
    left = min(points, key = lambda item: item[0])[0]
    # find rightmost point
    right = max(points, key = lambda item: item[0])[0]
    #find topmost point
    top = min(points, key = lambda item: item[1])[1]
    #find bottom point
    bottom = max(points, key = lambda item: item[1])[1]
    
    return left, top, right, bottom

    
def create_rect_linear_gradient(mat, colorFrom, colorTo, maskColor):
    # opencv is row-major so dimensions are height, width.  fucked up right?
    width = mat.shape[1]
    height = mat.shape[0]

    #http://stackoverflow.com/questions/25622612/linear-color-gradient-in-opencv
    def get_color_val(row, height, colorValFrom, colorValTo):
        return (row*colorValFrom+(height-row)*colorValTo) / height

    for row in range(0, height):
        colorR = get_color_val(row, height, colorFrom[0], colorTo[0])
        colorG = get_color_val(row, height, colorFrom[1], colorTo[1])
        colorB = get_color_val(row, height, colorFrom[2], colorTo[2])

        color = colorR, colorG, colorB

        for col in range(0, width):
            if not np.array_equal(maskColor, mat[row][col]):
                mat[row][col] = color

# corners must be an np.array([ [[x,y],[z,b]] ])
def get_masked_image(corners, original):
    mask = np.zeros(original.shape, dtype=np.uint8)
    roi_corners = np.array(corners, dtype=np.int32)
    white = 255, 255, 255
    cv2.fillPoly(mask, roi_corners, white)
    return cv2.bitwise_and(original, mask)

def get_roi_from_masked_image(corners, masked_image):
    rect_coords = get_rect_coords_from_points(corners)
    left = rect_coords[0]
    right = rect_coords[2]
    top = rect_coords[1]
    bottom = rect_coords[3]

    return masked_image[top:bottom, left:right]

def insert_roi_into_image(roi, image, corners, mask_color):
    rect_coords = get_rect_coords_from_points(corners)
    left = rect_coords[0]
    right = rect_coords[2]
    top = rect_coords[1]
    bottom = rect_coords[3]

    for row in range(top, bottom):
        roi_coord_space_row = row-top
        for col in range(left, right):
            roi_coord_space_col = col-left
            if not np.array_equal(roi[roi_coord_space_row][roi_coord_space_col], mask_color):
                image[row][col] = roi[roi_coord_space_row][roi_coord_space_col]
    
    return
    
image = cv2.imread('knightley.jpg')

points = [
    [20, 15],
    [300, 34],
    [24, 66]
]

# create mask for selected roi
masked_image = get_masked_image(np.array([points]), image)
roi = get_roi_from_masked_image(points, masked_image)
create_rect_linear_gradient(roi, (255, 0, 0), (0, 0, 255), (0,0,0))
insert_roi_into_image(roi, image, points, (0,0,0))

while (True):
    cv2.imshow('d', image)#cv2.bitwise_or(image, masked_image))
    cv2.waitKey()
