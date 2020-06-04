import numpy as np
import cv2
from datetime import datetime as dt

keys = np.array([['!', '@', '#', '$', '%', '^', '&', '*', '(', ')'],
                 ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'],
                 ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
                 ['A', 'S ', 'D', 'F', 'G', 'H', 'J', 'K', 'L', '\n'],
                 ['Z', 'X', 'C', 'V', 'B', 'N', 'M', ' ', ' ', 'SHIFT'],
                 [':', ';', '"', '\'', ',', '.', '<', '>', '/', '?']])
text = []
t1, t2, key, key_pressed, pressed_once = 0, 0, (0, 0), False, False

cap = cv2.VideoCapture('VKeyboard.mp4')


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
def coordinates(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    low = np.array([9, 160, 120])
    high = np.array([12, 255, 250])

    color = cv2.inRange(img, low, high)
    M = cv2.moments(color)
    x = int(M["m10"] / M["m00"])
    y = int(M["m01"] / M["m00"])

    return x, y


# To find which key is pressed
def is_key_pressed(x, y):
    global t1, t2, key, key_pressed, pressed_once
    xrange = np.arange(0, 1281, step=128)
    yrange = np.arange(0, 721, step=120)
    xKey, yKey = 0, 0

    for i in range(0, 10):
        if xrange[i] < x < xrange[i + 1]:
            xKey = i
    for j in range(0, 6):
        if yrange[j] < y < yrange[j + 1]:
            yKey = j

    if key == (yKey, xKey):
        enter_new_cell = False
    else:
        key = (yKey, xKey)
        enter_new_cell = True
        pressed_once = False

    if enter_new_cell:
        t1 = dt.now()
    else:
        t2 = dt.now()

    if (t2 - t1).seconds > 1 and not pressed_once:
        key_pressed = True
        pressed_once = True

    # return key, key_pressed


# Testing
frame = cv2.imread('IMG.jpg')
frame = cv2.resize(frame, (1280, 720))
cv2.imshow('one', frame)

res = perspective(frame)
cv2.imshow('result', res)

x, y = coordinates(res)
is_key_pressed(x, y)

if pressed_once:
    text.append(key)

cv2.waitKey(0)
cv2.destroyAllWindows()
