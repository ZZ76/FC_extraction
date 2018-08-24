import cv2
import numpy as np
bin = cv2.imread('DFC_AOI6_FC_tiles181.TIF', 0)
img = cv2.imread('DFC_AOI_RGB_tile181.TIF')
cv2.imshow('i1', bin)
_, contours, _ = cv2.findContours(bin, 1, 2)
cnt = contours
print 'length = ', len(cnt)

n = 1
for i in cnt:
    print 'n = ', n
    if n == len(cnt):
        break
    cv2.drawContours(img, [i], 0, (0, 255, 0), 2)
    x, y, w, h = cv2.boundingRect(i)
    print x, y, w, h
    if w > h:
        y = y - (w - h) / 2
        tmp = w
    else:
        x = x - (h - w) / 2
        tmp = h
    x2 = x + tmp
    y2 = y + tmp
    x = x - tmp / 5
    y = y - tmp / 5
    x2 = x2 + tmp / 5
    y2 = y2 + tmp / 5

    img = cv2.rectangle(img, (x, y), (x2, y2), (0, 255, 0), 2)
    print x, y, x2, y2
    n = n+1


cv2.imshow('bin', bin)
cv2.imshow('img', img)

cv2.waitKey(0)
cv2.destroyAllWindows()