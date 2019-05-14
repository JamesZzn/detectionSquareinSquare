import imutils
import cv2
from matplotlib import pyplot as plt

img  = cv2.imread("../Veriler/t4.png")

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (7, 7), 0)
edged = cv2.Canny(blurred, 50, 150)
cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
                        cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)

cv2.imshow("sadasd", edged)
cv2.waitKey(0)

for i in cnts:
    peri = cv2.arcLength(i, True)
    approx = cv2.approxPolyDP(i, 0.01 * peri, True)
    x, y, w, h = cv2.boundingRect(approx)
    img2 = img[y+10:y+h-10, x+10:x + w-10]
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

    print(x,y ,w ,h)

    cv2.imshow("sadasd",img)
    cv2.waitKey(0)

plt.imshow(img)
plt.show()
cv2.imwrite("../Veriler/t4.png",img2)


############YAPILACAKLAR###########

# Tespit edilen ve etrafına dikdörtgen çizilen şekilden yeni resim elde etceksin düşük pikselli
# sonra onun içinde kare arıyacaksın diğer yöntemlerle birleştirip olası kareyi bulup onun x,y,w,h ını bulacaksın
# çıkan ikinci x,y,w, h 'lardan ilklein farkına bakıp içinde olup olmadığına bakacaksın.