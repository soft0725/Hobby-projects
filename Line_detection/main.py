import cv2 
import numpy as np


def image_filtering(image):
    image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    lower = np.array([0, 0, 230])
    upper = np.array([180, 255, 255])
    mask = cv2.inRange(image_hsv, lower, upper)
    image = cv2.bitwise_and(image, image, mask=mask)
    
    gaussian = cv2.GaussianBlur(image, (3, 3), 0)
    canny = cv2.Canny(gaussian, 50, 150)
    
    return canny


def roi(image):
    height, width = image.shape[:2]
    roi_corners = np.array([[(600, height), (1700, height), (1000, 700), (1100, 700)]], dtype=np.int32)

    mask = np.zeros_like(image)
    cv2.fillConvexPoly(mask, roi_corners, 255)

    edges = cv2.bitwise_and(image, mask)
    
    return edges


def draw_line(edges, origin):
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 0, 0)
    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv2.line(origin, (x1, y1), (x2, y2), (0, 0, 255), 2)

    show_image(origin)


def show_image(origin):
    cv2.imwrite('result.png', origin)
    cv2.imshow('image', origin)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def main():
    path = './data/image.png'
    image = cv2.imread(path, cv2.IMREAD_COLOR)
    origin = image.copy()

    image = image_filtering(image)
    edges = roi(image)
    image = draw_line(edges, origin)
    show_image(image)

main()