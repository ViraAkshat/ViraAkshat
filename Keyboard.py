import numpy as np
import cv2
from datetime import datetime as dt


# To bring keyboard in perspective
def perspective(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thg = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 71, 7)
    gauss = cv2.GaussianBlur(thg, (5, 5), 0)

    contours, h = cv2.findContours(gauss, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    maxArea, maxContour = 0, contours[0]
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > maxArea:
            maxContour = contour
        maxArea = max(area, maxArea)

    epsilon = 0.1 * cv2.arcLength(maxContour, True)
    approx = cv2.approxPolyDP(maxContour, epsilon, True)
    pts = np.float32([approx[1][0], approx[0][0], approx[2][0], approx[3][0]])
    d = np.float32([[0, 0], [719, 0], [0, 1279], [719, 1279]])
    print(approx)
    matrix = cv2.getPerspectiveTransform(pts, d)
    print(matrix)
    final = cv2.warpPerspective(image, matrix, (720, 1280))
    final = np.rot90(final)

    return final


# To find coordinates of fingertip
def coordinates(h, s, v, uh, img):
    x, y = 0, 0
    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lcolor = np.array([h, s, v])
    hcolor = np.array([h, 255, 255])
    color = cv2.inRange(img, lcolor, hcolor)
    M = cv2.moments(color)
    x = int(M["m10"] / M["m00"])
    y = int(M["m01"] / M["m00"])

    return x, y


# To find which key is pressed
def is_key_pressed(x, y):
    global t1, t2, key, key_pressed
    xrange = np.arange(0, 1281, step=128)
    yrange = np.arange(0, 721, step=120)
    xKey, yKey = 0, 0

    for i in range(0, 10):
        if xrange[i] < x < xrange[i + 1]:
            xKey = i
    for j in range(0, 6):
        if yrange[j] < y < yrange[j + 1]:
            yKey = j

    if key == (xKey, yKey):
        enter_new_cell = False
    else:
        key = (xKey, yKey)
        enter_new_cell = True
        pressed_once = False

    if enter_new_cell:
        t1 = dt.now()
    else:
        t2 = dt.now()

    if (t2 - t1).seconds > 1 and pressed_once == False:
        key_pressed = True
        pressed_once = True

    return key


# Testing
t1, t2, key, key_pressed = 0, 0, (0, 0), False
frame = cv2.imread('IMG.jpg')
frame = cv2.resize(frame, (1280, 720))
cv2.imshow('one', frame)

res = perspective(frame)
cv2.imshow('result', res)

cv2.waitKey(0)
cv2.destroyAllWindows()
