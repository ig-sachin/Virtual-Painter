import cv2
import numpy as np
import time
import os
import HandTrackingModule as htm

brushThickness = 15
eraserThickness = 80

folderPath = "Header"
myList = os.listdir(folderPath)
# print(myList)
overlayList = []

for imgPath in myList:
    image = cv2.imread(f'{folderPath}/{imgPath}')
    overlayList.append(image)
# print(len(overlayList))

header = overlayList[0]
drawColor = (255, 0, 255)

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

# Square Initialization
isRect = False
tx = -1
ty = -1
bx = -1
by = -1
top = []
topFlag = True
bottom = []
bottomFlag = True

# Circle Initialization
isCircle = False
xc = -1
yc = -1
xr = -1
yr = -1
isCC = True
isRad = True
radius = -1
circlePts = []
radiusPts = []

detector = htm.handDetector(detectionCon=0.85)
xp, yp = 0, 0
imgCanvas = np.zeros((720, 1280, 3), np.uint8)

while True:
    # 1. Import image
    success, img = cap.read()
    img = cv2.flip(img, 1)

    # 2. Find Hand Landmarks
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList) != 0:
        # print(lmList[8])
        # Tip of Index and Middle Finger
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]
        # print(x1, y1)

        if isRect:
            if topFlag:
                top.append([x1, y1])

                if len(top) > 20:
                    top = top[1:]

                if len(top) == 20:
                    forx = True
                    initialX = top[0][0]
                    xsum = 0
                    ysum = 0

                    for i in range(1, len(top)):
                        arr = top[i]
                        xsum += arr[0]
                        if int(arr[0]) in range(initialX - 10, initialX + 10, 1):
                            forx = True
                        else:
                            forx = False
                            break

                    fory = True
                    initialY = top[0][1]

                    for i in range(1, len(top)):
                        arr = top[i]
                        ysum += arr[1]
                        if int(arr[1]) in range(initialY - 10, initialY + 10, 1):
                            fory = True
                        else:
                            fory = False
                            break

                    if forx and fory:
                        topFlag = False
                        tx = int(xsum / 20)
                        ty = int(ysum / 20)

            if not topFlag:
                print("Top Set")

            if not topFlag:
                bottom.append([x1, y1])

                if len(bottom) > 20:
                    bottom = bottom[1:]

                if len(bottom) == 20:
                    forx = True
                    initialX = bottom[0][0]
                    xsum = 0
                    ysum = 0

                    for i in range(1, len(bottom)):
                        arr = bottom[i]
                        xsum += arr[0]
                        if int(arr[0]) in range(initialX - 10, initialX + 10, 1):
                            forx = True
                        else:
                            forx = False
                            break

                    fory = True
                    initialY = bottom[0][1]

                    for i in range(1, len(bottom)):
                        arr = bottom[i]
                        ysum += arr[1]
                        if int(arr[1]) in range(initialY - 10, initialY + 10, 1):
                            fory = True
                        else:
                            fory = False
                            break

                    if forx and fory:
                        bottomFlag = False
                        bx = int(xsum / 20)
                        by = int(ysum / 20)

            if not bottomFlag:
                print("Bottom Set")

        if isCircle:
            if isCC:
                circlePts.append([x1, y1])
                if len(circlePts) > 20:
                    circlePts = circlePts[1:]
                if len(circlePts) == 20:
                    forx = True
                    initialX = circlePts[0][0]
                    xsum = 0
                    ysum = 0

                    for i in range(1, len(circlePts)):
                        arr = circlePts[i]
                        xsum += arr[0]
                        if int(arr[0]) in range(initialX - 10, initialX + 10, 1):
                            forx = True
                        else:
                            forx = False
                            break

                    fory = True
                    initialY = circlePts[0][1]

                    for i in range(1, len(circlePts)):
                        arr = circlePts[i]
                        ysum += arr[1]
                        if int(arr[1]) in range(initialY - 10, initialY + 10, 1):
                            fory = True
                        else:
                            fory = False
                            break

                    if forx and fory:
                        isCC = False
                        xc = int(xsum / 20)
                        yc = int(ysum / 20)

            if not isCC:
                print("Center Set")

            if not isCC:
                radiusPts.append([x1, y1])

                if len(radiusPts) > 20:
                    radiusPts = radiusPts[1:]

                if len(radiusPts) == 20:
                    forx = True
                    initialX = radiusPts[0][0]
                    xsum = 0
                    ysum = 0

                    for i in range(1, len(radiusPts)):
                        arr = radiusPts[i]
                        xsum += arr[0]
                        if int(arr[0]) in range(initialX - 10, initialX + 10, 1):
                            forx = True
                        else:
                            forx = False
                            break

                    fory = True
                    initialY = radiusPts[0][1]

                    for i in range(1, len(radiusPts)):
                        arr = radiusPts[i]
                        ysum += arr[1]
                        if int(arr[1]) in range(initialY - 10, initialY + 10, 1):
                            fory = True
                        else:
                            fory = False
                            break

                    if forx and fory:
                        isRad = False
                        xr = int(xsum / 20)
                        yr = int(ysum / 20)

            if not isRad:
                print("Radius Set")

            if not isCC and not isRad:
                radius = ((((xr - xc) ** 2) + ((yr - yc) ** 2)) ** 0.5)
                print(f"The radius is {int(radius)}")

        # 3. Check Which fingers are up
        fingers = detector.fingersUp()
        # print(fingers)

        # 4. If Selection Mode - Two Fingers are up
        if fingers[1] and fingers[2] and (not isRect):
            xp, yp = 0, 0
            # print("Selection Mode")
            # Checking for the Click
            if y1 < 100:
                if 250 < x1 < 450:
                    header = overlayList[0]
                    drawColor = (255, 0, 255)
                elif 550 < x1 < 750:
                    header = overlayList[1]
                    drawColor = (255, 0, 0)
                elif 800 < x1 < 950:
                    header = overlayList[2]
                    drawColor = (0, 255, 0)
                elif 1050 < x1 < 1200:
                    header = overlayList[3]
                    drawColor = (0, 0, 0)
            cv2.rectangle(img, (x1, y1 - 25), (x2, y2 + 25), drawColor, cv2.FILLED)
        # 5. If Drawing Mode - Index Finger is Up
        if fingers[1] and fingers[2] == False and (not isRect):
            cv2.circle(img, (x1, y1), 10, drawColor, cv2.FILLED)
            # print("Drawing Mode")
            if xp == 0 and yp == 0:
                xp, yp = x1, y1

            if drawColor == (0, 0, 0):
                cv2.line(img, (xp, yp), (x1, y1), drawColor, eraserThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, eraserThickness)
            else:
                cv2.line(img, (xp, yp), (x1, y1), drawColor, brushThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushThickness)

            xp, yp = x1, y1

        if isRect and (fingers[1] and fingers[2] == False):
            if tx != -1 and ty != -1 and bx != -1 and by != -1:
                cv2.rectangle(img, (tx, ty), (bx, by), drawColor, thickness=10)
                cv2.rectangle(imgCanvas, (tx, ty), (bx, by), drawColor, thickness=10)
                tx = -1
                ty = -1
                bx = -1
                by = -1
                top = []
                topFlag = True
                bottom = []
                bottomFlag = True
                isRect = False
                xp = x1
                yp = y1

        if isCircle and (fingers[1] and fingers[2] == False):
            if xc != -1 and yc != -1 and xr != -1 and yr != -1:
                print("i am here")
                cv2.circle(img, (xc, yc), radius=int(radius/2), color=drawColor, thickness=5)
                cv2.circle(imgCanvas, (xc, yc), radius=int(radius/2), color=drawColor, thickness=5)
                isCircle = False
                xc = -1
                yc = -1
                xr = -1
                yr = -1
                isCC = True
                isRad = True
                radius = -1
                circlePts = []
                radiusPts = []

            # isRect = False

    imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(img, imgInv)
    img = cv2.bitwise_or(img, imgCanvas)

    # Setting the header image
    img[0:100, 0:1280] = header
    img = cv2.addWeighted(img, 0.8, imgCanvas, 0.5, 0)
    cv2.imshow("Image", img)
    # cv2.imshow("Image Canvas", imgCanvas)

    # For Rectangle
    k = cv2.waitKey(1)
    k = k - 48
    if k == 1:
        isCircle = False
        isRect = True
        print("Rect Mode")
        tx = -1
        ty = -1
        bx = -1
        by = -1
        top = []
        topFlag = True
        bottom = []
        bottomFlag = True

    # For Circle
    c = cv2.waitKey(2)
    c = c - 48
    if c == 2:
        isCircle = True
        isRect = False
        xc = -1
        yc = -1
        xr = -1
        yr = -1
        isCC = True
        isRad = True
        radius = -1
        circlePts = []
        radiusPts = []
        print("Circle Mode")
