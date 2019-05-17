import imutils
import cv2
from matplotlib import pyplot as plt

img  = cv2.imread("../Veriler/ters.png")

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (7, 7), 0)
edged = cv2.Canny(blurred, 50, 150)
cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
                        cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
"""
cv2.imshow("sadasd", edged)
cv2.waitKey(0)
"""
for i in cnts:
    peri = cv2.arcLength(i, True)
    approx = cv2.approxPolyDP(i, 0.01 * peri, True)
    x, y, w, h = cv2.boundingRect(approx)

    edged2 = edged.copy()
    edged2[:,:] = 0
    edged2[y+10:y+h-10, x+10:x + w-10] = edged[y+10:y+h-10, x+10:x + w-10]
    cnts2 = cv2.findContours(edged2.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts2 = imutils.grab_contours(cnts2)
    """
    if len(approx) >= 4 and len(approx) <= 6:
        #(x, y, w, h) = cv2.boundingRect(approx)
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        print(x, y, w, h)
        cv2.imshow("sadasd", img)
        cv2.waitKey(0)
    """
    for j in cnts2:
        peri2 = cv2.arcLength(j, True)
        approx2 = cv2.approxPolyDP(j, 0.01 * peri2, True)
        if len(approx2) >= 4 and len(approx2) <= 6:
            x2, y2, w2, h2 = cv2.boundingRect(approx2)

            if (x2 - x) > 0 and (y2 - y) > 0 and (h - h2) > 0 and (w - w2) > 0:

                M = cv2.moments(approx)
                (cX, cY) = (int(M["m10"] // M["m00"]), int(M["m01"] // M["m00"]))
                print(cX,cY) #approx2 yapmadım en büyük karenin merkezi


plt.imshow(img)
plt.show()
cv2.imwrite("../Veriler/t4.png",edged2)
############YAPILACAKLAR###########

# Tespit edilen ve etrafına dikdörtgen çizilen şekilden yeni resim elde etceksin düşük pikselli
# sonra onun içinde kare arıyacaksın diğer yöntemlerle birleştirip olası kareyi bulup onun x,y,w,h ını bulacaksın
# çıkan ikinci x,y,w, h 'lardan ilklein qfarkına bakıp içinde olup olmadığına bakacaksın.