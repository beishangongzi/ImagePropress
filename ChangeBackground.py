import cv2
import numpy as np

img = cv2.imread(r"/media/andy/Data/info/p.jpg")
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)


lower_blue=np.array([90,70,70])
upper_blue=np.array([110,255,255])
mask = cv2.inRange(hsv, lower_blue, upper_blue)
cv2.imshow('Mask', mask)

rows,cols,channels = img.shape
for i in range(rows):
    for j in range(cols):
        if mask[i,j]==255:
            img[i,j]=(255,255,255)#此处替换颜色，为BGR通道

cv2.imshow('res',img)
cv2.imwrite(r"kanghuan_new.jpg", img)
cv2.waitKey(0)
# cv2.destroyAllWindow()
