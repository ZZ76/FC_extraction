import cv2
import numpy as np
import random
import os
import re

sample_size = 100   # the ground sample image size
numperimg = 4   # number of ground selected per image
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

def selectground(cnt2, width, height, img2, num):
    flag1 = 0
    while flag1 < numperimg:
        l = random.randint(30, 200)  # square length
        xg = random.randint(0, width - l)  # start position x
        yg = random.randint(0, height - l)  # start position y
        gp = [(xg, yg), (xg + l, yg), (xg + l, yg + l), (xg, yg + l)]
        gcnt = [np.array([gp])]
        flag2 = 0
        for i2 in cnt2:
            if pointpoly(gcnt[0], i2) == 0:  # points on cnt2(bound box) outside of gcnt(random box)
                pass
            else:
                flag2 = 1
                break

        while flag2 < 1:
            if contours2(cnt2, gp) < 0:
                break
            else:  # find right ground
                flag1 = flag1 + 1
                gd = img2[gp[0][1]:gp[2][1], gp[0][0]:gp[2][0]]
                gd = cv2.resize(gd, (sample_size, sample_size))  # resize image
                name = num + '_' + str(flag1)
                cv2.imwrite(smp_path + '/' + name + '.jpg', gd)
                print name
                break

def readandselect(bin_name, img_name, num):
    bin1 = cv2.imread(bin_path + '/' + bin_name, -1)
    bin = cv2.cvtColor(bin1, cv2.COLOR_GRAY2BGR)
    img2 = cv2.imread(img_path + '/' + img_name, 1)   # extract fcs
    lower = np.array([0,0,0])
    upper = np.array([255,255,255])
    bin = cv2.inRange(bin, lower, upper)
    _, contours, _ = cv2.findContours(bin, 1, 2)
    cnt = contours
    height, width = bin.shape[:2]
    n = 1
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
            if cnt2 is None:
                cnt2 = [np.array([[x, y], [x, y2], [x2, y2], [x2, y]])]
            else:
                cnt2 = np.append(cnt2, [[[x, y], [x, y2], [x2, y2], [x2, y]]], axis=0)
        n = n+1
    selectground(cnt2, width, height, img2, num)

#DFC
#bin_path = "./DFC_AOI6_FC_tiles"   # binary image folder
#img_path = "./DFC_AOI6_RGB_tiles"   # raw image folder
#smp_path = "./gnd1"   # save image folder
# GFC
bin_path = "./GFC_AOI6_FC_tiles"
img_path = "./GFC_AOI6_RGB_tiles"
smp_path = "./gnd2"
'''testing
bin_path = "./bin"
img_path = "./img"
smp_path = "./gnd_test"'''

bin_files = os.listdir(bin_path)
img_files = os.listdir(img_path)
for file_bin in bin_files:
    if not os.path.isdir(file_bin):   # search in bin folder find .tif file
        if file_bin[-4:] == '.TIF':
            num = re.findall('\d+', file_bin)[-1]
            #print num
            for file_img in img_files:
                #print img_files[n_img:]
                if file_img[-4:] == '.TIF':
                    img_num = re.findall('\d+', file_img)[-1]   # 0 for group DFC, 1 for group GFC !!!!!!!!!!!!!!!!!!!!!!
                    if img_num == num:
                        print file_bin, ',', file_img
                        #num = num + '_2'   # get rid of same name
                        readandselect(file_bin, file_img, num)
                        break

cv2.waitKey(0)
cv2.destroyAllWindows()
