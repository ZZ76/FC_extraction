import cv2
import numpy as np
import random

def pointpoly(contour, points):
    for j1 in points:
        if cv2.pointPolygonTest(contour, (j1[0], j1[1]), False) > 0:   # point outside contour
            return -1
    else:
        return 0

def pointpoly2(contour, points):
    for j2 in points:
        if cv2.pointPolygonTest(contour, j2, False) > 0:   # point outside contour
            return -1
    else:
        return 0

def contours2(cts, cpoints):
    for i in cts:
        if pointpoly2(i, cpoints) < 0:
            return -1
    else:
        return 0

def selectground(cnt2, width, height):
    flag1 = 0
    while flag1 < gnd_num:
        l = random.randint(80, 200)  # square length
        xg = random.randint(0, width - l)  # start position x
        yg = random.randint(0, height - l)  # start position y
        gp = [(xg, yg), (xg + l, yg), (xg + l, yg + l), (xg, yg + l)]
        gcnt = [np.array([gp])]
        print 'gp = ', gp
        flag2 = 0
        for i2 in cnt2:
            print 'i2 is ', i2
            if pointpoly(gcnt[0], i2) == 0:  # points on cnt2(bound box) outside of gcnt(random box)
                pass
            else:
                cv2.drawContours(img, gcnt, 0, (0, 255, 255), 2)
                flag2 = 1
                break

        while flag2 < 1:
            if contours2(cnt2, gp) < 0:
                cv2.drawContours(img, gcnt, 0, (255, 0, 255), 2)
                break
            else:  # find right ground
                cv2.drawContours(img, gcnt, 0, (0, 0, 255), 2)
                cv2.putText(img, str(flag1 + 1), gp[3], font, 1, (255, 255, 255), 2, cv2.LINE_AA)
                flag1 = flag1 + 1
                gd = img2[gp[0][1]:gp[2][1], gp[0][0]:gp[2][0]]
                # gd = cv2.resize(gd, (sample_size, sample_size))
                name = 'gd' + str(flag1)
                cv2.imshow(name, gd)   # show single samples
                break

gnd_num = 3
bnr_image_name = 'DFC_AOI6_FC_tiles524.TIF'
image_name = 'DFC_AOI_RGB_tile524.TIF'
bin1 = cv2.imread(bnr_image_name, -1)
bin2 = cv2.imread(bnr_image_name, -1)
bin = cv2.cvtColor(bin1, cv2.COLOR_GRAY2BGR)
img = cv2.imread(image_name, 1)   # showing bound boxs 1-color 0-gray
img2 = cv2.imread(image_name, 1)   # extract fcs
font = cv2.FONT_HERSHEY_SIMPLEX

lower = np.array([0, 0, 0])
upper = np.array([255, 255, 255])
bin = cv2.inRange(bin, lower, upper)


_, contours, _ = cv2.findContours(bin, 1, 2)
cnt = contours
print 'length = ', len(cnt)   # contour quantity

height, width = bin.shape[:2]
n = 1
sample_size = 100
cnt2 = None
for i1 in cnt:
    x, y, w, h = cv2.boundingRect(i1)
    if w > h:
        y = y - (w - h) / 2
        tmp = w
    else:
        x = x - (h - w) / 2
        tmp = h
    x2 = x + tmp
    y2 = y + tmp

    if (x2 - x) < 20:
        if cnt2 is None:
            cnt2 = [np.array([[x, y], [x, y2], [x2, y2], [x2, y]])]
        else:
            cnt2 = np.append(cnt2, [[[x, y], [x, y2], [x2, y2], [x2, y]]], axis=0)
        pass
    else:
        img = cv2.rectangle(img, (x, y), (x2, y2), (0, 255, 0), 2)
        if cnt2 is None:
            cnt2 = [np.array([[x, y], [x, y2], [x2, y2], [x2, y]])]
        else:
            cnt2 = np.append(cnt2, [[[x, y], [x, y2], [x2, y2], [x2, y]]], axis=0)
        cv2.drawContours(img, [i1], 0, (0, 255, 0), 2)
    n = n+1
selectground(cnt2, width, height)


#cv2.imshow('bin', bin)
#cv2.imshow('bin2', bin2)
cv2.imshow('img', img)

cv2.waitKey(0)
cv2.destroyAllWindows()
