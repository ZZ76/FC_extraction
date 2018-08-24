import cv2
import numpy as np
import random
import os
import re

sample_size = 100 # the ground sample image size
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
    while flag1 < 2:
        l = random.randint(30, 200)  # square length
        xg = random.randint(0, width - l)  # start position x
        yg = random.randint(0, height - l)  # start position y
        gp = [(xg, yg), (xg + l, yg), (xg + l, yg + l), (xg, yg + l)]
        gcnt = [np.array([gp])]
        print 'gp = ', gp
        flag2 = 0
        for i2 in cnt2:
            #print 'i2 is ', i2
            if pointpoly(gcnt[0], i2) == 0:  # points on cnt2(bound box) outside of gcnt(random box)
                pass
            else:
                #cv2.drawContours(img, gcnt, 0, (0, 255, 255), 2)
                flag2 = 1
                break

        while flag2 < 1:
            if contours2(cnt2, gp) < 0:
                #cv2.drawContours(img, gcnt, 0, (255, 0, 255), 2)
                break
            else:  # find right ground
                #cv2.drawContours(img, gcnt, 0, (0, 0, 255), 2)
                #cv2.putText(img, str(flag1 + 1), gp[3], font, 1, (255, 255, 255), 2, cv2.LINE_AA)
                flag1 = flag1 + 1
                flag2 = 1
                gd = img2[gp[0][1]:gp[2][1], gp[0][0]:gp[2][0]]
                gd = cv2.resize(gd, (sample_size, sample_size))  # resize image
                name = num + '_' + str(flag1)
                #cv2.imwrite(smp_path + '/' + name + '.jpg', gd)

                cv2.imshow(name, gd)
                print name
                break

def readandselect(bin_name, img_name, num):
    #bnr_image_name = 'DFC_AOI6_FC_tiles303.TIF'
    #image_name = 'DFC_AOI_RGB_tile303.TIF'
    bin1 = cv2.imread(bin_path + '/' + bin_name, -1)
    #bin2 = cv2.imread(bnr_image_name, -1)   #just showing contour
    bin = cv2.cvtColor(bin1, cv2.COLOR_GRAY2BGR)
    #img = cv2.imread(image_name, 1)   # showing bound boxs 1-color 0-gray
    img2 = cv2.imread(img_path + '/' + img_name, 1)   # extract fcs
    font = cv2.FONT_HERSHEY_SIMPLEX

    lower = np.array([0,0,0])
    upper = np.array([255,255,255])
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
            pass
        else:
            #img = cv2.rectangle(img, (x, y), (x2, y2), (0, 255, 0), 2)
            if cnt2 is None:
                cnt2 = [np.array([[x, y], [x, y2], [x2, y2], [x2, y]])]
            else:
                cnt2 = np.append(cnt2, [[[x, y], [x, y2], [x2, y2], [x2, y]]], axis=0)
            #cv2.drawContours(img, [i1], 0, (0, 255, 0), 2)
        n = n+1
    selectground(cnt2, width, height, img2, num)


#bin_path = "./DFC_AOI6_FC_tiles"   # binary image folder
#img_path = "./DFC_AOI6_RGB_tiles"   # raw image folder
#smp_path = "./gnd1"   # save image folder
# group 2
#bin_path = "./GFC_AOI6_FC_tiles"
#img_path = "./GFC_AOI6_RGB_tiles"
#smp_path = "./gnd2
# testing
bin_path = "./bin"
img_path = "./img"
smp_path = "./gnd_test"

bin_files = os.listdir(bin_path)
img_files = os.listdir(img_path)
#n_img = 0   # pointer in image folder
for file_bin in bin_files:
    if not os.path.isdir(file_bin):   # search in bin folder find .tif file
        if file_bin[-4:] == '.TIF':
            num = re.findall('\d+', file_bin)[1]
            print num

            #for file_img in img_files[n_img:]:   # search in img folder find the corresponding image
            for file_img in img_files:
                #print img_files[n_img:]
                if file_img[-4:] == '.TIF':
                    #img_num = re.findall('\d+', file_img)[0]   # number(0 or 1) in [] may change according to file name
                    img_num = re.findall('\d+', file_img)[0]   # group 2
                    if img_num == num:
                        #print file_img
                        readandselect(file_bin, file_img, num)
                        break
                #print 'n_img =', n_img
                #n_img = n_img + 1


#cv2.imshow('bin', bin)
#cv2.imshow('bin2', bin2)
#cv2.imshow('img', img)

cv2.waitKey(0)
cv2.destroyAllWindows()