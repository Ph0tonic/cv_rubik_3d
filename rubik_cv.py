import numpy as np
import cv2
import math
from enum import Enum, auto

# helper function:
# finds a cosine of angle between vectors
# from pt0->pt1 and from pt0->pt2
def angle(pt1, pt2, pt0):
    dx1 = pt1[0][0] - pt0[0][0]
    dy1 = pt1[0][1] - pt0[0][1]
    dx2 = pt2[0][0] - pt0[0][0]
    dy2 = pt2[0][1] - pt0[0][1]

    return (dx1*dx2 + dy1*dy2) / math.sqrt((dx1*dx1 + dy1*dy1)*(dx2*dx2 + dy2*dy2) + 1e-10)

class color(Enum):
    RED = auto()
    GREEN = auto()
    BLUE = auto()
    YELLOW = auto()
    ORANGE = auto()
    WHITE = auto()



# images -> mat
# squares -> vector<vector<Point>>
def drawSquares(image, squares):
    for square in squares:
        p = square[0]
        n = len(square)
        shift = 1

        x, y, w, h = cv2.boundingRect(square)
        r = np.zeros((h, w, 3), dtype=np.uint8)

        x = x + w // 4
        y = y + w // 4
        w = w // 2
        h = h // 2

        roi = r
        color = cv2.mean(roi)
        cv2.polylines(image, np.int32([p]), True, color, 2, cv2.LINE_AA, shift)

        cv2.ellipse(image, (x+w//2, y+h//2), (w//2,h//2), 0, 0, 360, color, 2, cv2.LINE_AA)

def detect_color(image):
    square_zone = ((170, 500), (480, 480)) # x;y -> left corner , w;h
    result = numpy.full([3,3], -1)

    width_one_square = square_zone[1][0] // 3

    for i in range(0,3):
        for j in range(0,3):
            pass

def findCorners(image):
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    dst = cv2.cornerHarris(gray, 2, 5, 0.04)

    #result is dilated for marking the corners, not important
    dst = cv2.dilate(dst, None)

    # Threshold for an optimal value, it may vary depending on the image.
    image[dst>0.01*dst.max()]=[0,0,255]


# returns sequence of squares detected on the image.
# the sequence is stored in the specified memory storage
# iamge -> mat
# inv -> bool
def findSquares(image, inv = False):
    squares = []

    # gray0 = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(image, (7,7), 1.5, 1.5)

    gray = cv2.Canny(image,0,75,apertureSize = 3)

    cv2.imshow("Canny", gray)

    # find contours and store them all as a list
    contours, hierarchy = cv2.findContours(gray, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    # test each contour
    for cont in contours:
        # approximate contour with accuracy proportional
        # to the contour perimeter
        # OLD -> approxPolyDP(Mat(contours[i]), approx, 9, true);
        approx = cv2.approxPolyDP(cont, 9, True)

        # square contours should have 4 vertices after approximation
        # relatively large area (to filter out noisy contours)
        # and be convex.
        # Note: absolute value of an area is used because
        # area may be positive or negative - in accordance with the
        # contour orientation
        if len(approx) == 4 and math.fabs(cv2.contourArea(approx)) > 2 and cv2.isContourConvex(approx):
            maxCosine = 0

            for j in range(2,5):
                # find the maximum cosine of the angle between joint edges
                cosine = math.fabs(angle(approx[j%4], approx[j-2], approx[j-1]))
                maxCosine = max(maxCosine, cosine)

            # if cosines of all angles are small
            # (all angles are ~90 degree) then write quandrange
            # vertices to resultant sequence
            if maxCosine < 0.5:
                squares.append(approx)

    return squares


if __name__ == '__main__':
    # try:
    #     cap = cv2.VideoCapture(0)
    # except Exception as e:
    #     print("error while opening camera")
    #     raise e

    img = cv2.imread('img/01.jpg', cv2.IMREAD_GRAYSCALE)

    # while True:
    #     ret, frame = cap.read()
    #
    #     if frame.size == 0:
    #         raise Exception(-1)

    squares = findSquares(img)
    drawSquares(img, squares)
    # findCorners(frame)
    print(squares)
    cv2.imshow("Rubic Detection Demo", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
