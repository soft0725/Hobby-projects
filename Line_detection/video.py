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
    roi_corners = np.array([[(400, height), (1700, height), (1000, 700), (1100, 700)]], dtype=np.int32)

    mask = np.zeros_like(image)
    cv2.fillConvexPoly(mask, roi_corners, 255)

    edges = cv2.bitwise_and(image, mask)
    
    return edges

def draw_line(edges, origin):
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 0, 0)
    for line in lines:
        # 검출된 선분 초록색으로 그리기
        x1, y1, x2, y2 = line[0]
        cv2.line(origin, (x1, y1), (x2, y2), (0, 0, 255), 2)

    return origin

def show_video():
    cap = cv2.VideoCapture('./data/video.mp4')
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret:
            edges = image_filtering(frame)
            edges = roi(edges)
            frame = draw_line(edges, frame)
            cv2.imshow('video', frame)
        else:
            break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

show_video()