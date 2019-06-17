import imutils
import cv2
from imutils.video import VideoStream
from imutils.video import FPS
import time

# co
count8 = 0
# load the video
# camera = cv2.VideoCapture("../Veriler/v1.mp4")

img = cv2.imread("../Veriler/t2.png")

frame = img[:]
status = "No Targets"

frame = imutils.resize(frame, width=800)
ratio = img.shape[1]/ float(frame.shape[1])

(H, W) = frame.shape[:2]
print(H, W)

gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (7, 7), 0)
edged = cv2.Canny(blurred, 50, 150)

cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
                        cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)

cv2.imshow("Frame", edged)

cv2.waitKey()

for c in cnts:

    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.01 * peri, True)

    if len(approx) >= 4 and len(approx) <= 6:

        (x, y, w, h) = cv2.boundingRect(approx)
        aspectRatio = w / float(h)

        area = cv2.contourArea(c)
        hullArea = cv2.contourArea(cv2.convexHull(c))
        solidity = area / float(hullArea)

        keepDims = w > 5 and h > 5
        keepSolidity = solidity > 0.8
        keepAspectRatio = aspectRatio >= 0.8 and aspectRatio <= 1.2
        print("ilk kare")
        print(w, h, solidity, aspectRatio)
        print(keepDims, keepSolidity, keepAspectRatio)

        # ensure that the contour passes all our tests
        if keepDims and keepSolidity and keepAspectRatio:
            edged2 = edged.copy()
            edged2[:, :] = 0
            edged2[y + 10:y + h - 10, x + 10:x + w - 10] = edged[y + 10:y + h - 10, x + 10:x + w - 10]

            cv2.imshow("Frame", edged2)
            cv2.waitKey()

            cnts2 = cv2.findContours(edged2.copy(), cv2.RETR_EXTERNAL,
                                     cv2.CHAIN_APPROX_SIMPLE)
            cnts2 = imutils.grab_contours(cnts2)

            for j in cnts2:
                peri2 = cv2.arcLength(j, True)
                approx2 = cv2.approxPolyDP(j, 0.01 * peri2, True)
                print("aprroxx 2 ", approx2)
                if len(approx2) >= 4 and len(approx2) <= 6:
                    x2, y2, w2, h2 = cv2.boundingRect(approx2)

                    if (x2 - x) > 0 and (y2 - y) > 0 and (h - h2) > 0 and (w - w2) > 0:
                        aspectRatio2 = w2 / float(h2)
                        area2 = cv2.contourArea(j)
                        hullArea2 = cv2.contourArea(cv2.convexHull(j))
                        solidity2 = area2 / float(hullArea2)

                        keepDims2 = w2 > 5 and h2 > 5
                        keepSolidity2 = solidity2 > 0.8
                        keepAspectRatio2 = aspectRatio2 >= 0.8 and aspectRatio2 <= 1.2

                        print("\n\nikinci kare")

                        print(w2, h2, solidity2, aspectRatio2)
                        print(keepDims2, keepSolidity2, keepAspectRatio2)

                        if keepDims2 and keepSolidity2 and keepAspectRatio2:
                            count8 = count8 + 1
                            print(count8)
                            cv2.drawContours(frame, [approx], -1, (0, 0, 255), 4)
                            status = "Target(s) Acquired"

                            M = cv2.moments(approx)
                            (cX, cY) = (int(M["m10"] // M["m00"]), int(M["m01"] // M["m00"]))
                            (startX, endX) = (int(cX - (w * 0.15)), int(cX + (w * 0.15)))
                            (startY, endY) = (int(cY - (h * 0.15)), int(cY + (h * 0.15)))
                            cv2.line(frame, (startX, cY), (endX, cY), (0, 0, 255), 3)
                            cv2.line(frame, (cX, startY), (cX, endY), (0, 0, 255), 3)
                            (resultX, resultY, radius) = (cX * ratio, cY * ratio, w*ratio)
                            print( "istenen sey " , (resultX,resultY,radius) )
                            print()

                            # draw the status text on the frame
                            cv2.putText(frame, status, (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                        (0, 0, 255), 2)

# show the frame and record if a key is pressed


cv2.imshow("Frame", frame)
cv2.waitKey()
