import cv2
import numpy as np
import random
import os
import re


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
        l = random.randint(area_range[0], area_range[1])  # square length
        xg = random.randint(0, width - l)  # start position x
        yg = random.randint(0, height - l)  # start position y
        gp = [(xg, yg), (xg + l, yg), (xg + l, yg + l), (xg, yg + l)]
        gcnt = [np.array([gp])]   # contours of ground
        if cnt2 is None:
            cv2.drawContours(img, gcnt, 0, (0, 0, 255), 2)   # show result
            cv2.putText(img, str(flag1 + 1), gp[3], font, 1, (255, 255, 255), 2, cv2.LINE_AA)
            flag1 = flag1 + 1
            gd = img2[gp[0][1]:gp[2][1], gp[0][0]:gp[2][0]]
            gd = cv2.resize(gd, (sample_size, sample_size))
            name = str(flag1)  # name is pure number
            #cv2.imshow(smp_path + '/' + name + '.jpg', gd)
            print smp_path + '/' + name + '.jpg'
            cv2.imwrite(smp_path + '/' + name + '.jpg', gd)
        else:
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
                    cv2.drawContours(img, gcnt, 0, (0, 0, 255), 2)   # show result
                    cv2.putText(img, str(flag1 + 1), gp[3], font, 1, (255, 255, 255), 2, cv2.LINE_AA)
                    flag1 = flag1 + 1
                    gd = img2[gp[0][1]:gp[2][1], gp[0][0]:gp[2][0]]
                    gd = cv2.resize(gd, (sample_size, sample_size))  # resize image
                    #name = num + '_' + str(flag1)   # name is file number + number
                    name = str(flag1)   # name is pure number
                    #cv2.imshow(smp_path + '/' + name + '.jpg', gd)
                    print smp_path + '/' + name + '.jpg'
                    cv2.imwrite(smp_path + '/' + name + '.jpg', gd)
                    break
        #cv2.imshow('img', img)

def readandselect(bin_name, img_name, num):
    global img, font
    img = cv2.imread(img_file, 1)
    img2 = cv2.imread(img_file, 1)  # extract fcs
    font = cv2.FONT_HERSHEY_SIMPLEX
    if os.path.exists(bin_file) is True:
        bin1 = cv2.imread(bin_file, -1)
        bin = cv2.cvtColor(bin1, cv2.COLOR_GRAY2BGR)
        lower = np.array([0, 0, 0])
        upper = np.array([255, 255, 255])
        bin = cv2.inRange(bin, lower, upper)
        _, contours, _ = cv2.findContours(bin, 1, 2)
        cnt = contours   # contours of FCs
        height, width = bin.shape[:2]
        n = 1
        cnt2 = None
        for i1 in cnt:   # generate bounding box of  to cnt2
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
    else:
        cnt2 = None
        height, width = img2.shape[:2]
    selectground(cnt2, width, height, img2, num)


sample_size = 100   # the ground sample image size
numperimg = 100   # number of ground selected per image
area_range = (35, 150)
# DFC
bin_file = "./DFC_AOI6_FC_tiles/DFC_AOI6_FC_tiles519.TIF"
img_file = "./DFC_AOI6_RGB_tiles/DFC_AOI_RGB_tile519.TIF"
# GFC
#bin_file = "./GFC_AOI6_FC_tiles/GFC_AOI6_FC_tile733.TIF"   # binary image folder
#img_file = "./GFC_AOI6_RGB_tiles/GFC_AOI6_RGB_tile733.TIF"   # raw image folder

smp_path = "./tmp"   # save path

num = re.findall('\d+', img_file)[0]   # 0 for group DFC, 1 for group GFC !!!!!!!!!!!!!!!!!!!!!!
#print(num)
readandselect(bin_file, img_file, num)

'''for file_bin in bin_files:
    if not os.path.isdir(file_bin):   # search in bin folder find .tif file
        if file_bin[-4:] == '.TIF':
            num = re.findall('\d+', file_bin)[1]
            #print num
            for file_img in img_files:
                #print img_files[n_img:]
                if file_img[-4:] == '.TIF':
                    img_num = re.findall('\d+', file_img)[1]   # 0 for group 1, 1 for group 2 !!!!!!!!!!!!!!!!!!!!!!
                    if img_num == num:
                        print file_bin, ',', file_img
                        #num = num + '_2'   # get rid of same name
                        readandselect(file_bin, file_img, num)
                        break'''

cv2.waitKey(0)
cv2.destroyAllWindows()