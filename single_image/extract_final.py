'''import os
import re
import cv2
import numpy as np'''

def extract(bin_name, img_name, num):
    bin1 = cv2.imread(bin_path + '/' + bin_name, -1)
    bin2 = cv2.cvtColor(bin1, cv2.COLOR_GRAY2BGR)
    #img = cv2.imread(img_path + '/' + img_name)   # show for test
    img2 = cv2.imread(img_path + '/' + img_name)

    # ret,thresh = cv2.threshold(bin,127,255,cv2.THRESH_BINARY_INV)

    # bin = cv2.cvtColor(bin, cv2.COLOR_BGR2HSV)
    # cv2.imshow('i1', bin)
    lower = np.array([0, 0, 0])
    upper = np.array([255, 255, 255])
    bin2 = cv2.inRange(bin2, lower, upper)

    # Bitwise-AND mask and original image
    # res = cv2.bitwise_and(bin,bin, mask= mask)

    _, contours, _ = cv2.findContours(bin2, 1, 2)
    cnt = contours
    print 'amount of contours = ', len(cnt)

    height, width = bin2.shape[:2]
    n = 1
    sample_size = 100
    for i in cnt:
        #print 'n = ', n
        # if n == len(cnt):
        # break
        x, y, w, h = cv2.boundingRect(i)
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

        if y < 0 or x < 0 or x2 > width or y2 > height or (x2 - x) < 20:   # do not use FC on border or size too small
            pass
        else:
            #print x, y, x2, y2
            #img = cv2.rectangle(img, (x, y), (x2, y2), (0, 255, 0), 2)   # draw contour and rectangle for test
            #cv2.drawContours(img, [i], 0, (0, 255, 0), 2)
            fc = img2[y:y2, x:x2]
            fc = cv2.resize(fc, (sample_size, sample_size))   # resize image
            name = num + '_' + str(n)
            cv2.imwrite(smp_path + '/' + name + '.jpg', fc)
            #cv2.imshow(name, fc)
        n = n + 1

    #cv2.imshow('bin', bin)   # show image for test
    #cv2.imshow('img', img)

    #cv2.waitKey(0)
    cv2.destroyAllWindows()

# group 1
bin_path = "./DFC_AOI6_FC_tiles"   # binary image folder
img_path = "./DFC_AOI6_RGB_tiles"   # raw image folder
smp_path = "./smp1"   # sample image folder
# group 2
#bin_path = "./GFC_AOI6_FC_tiles"
#img_path = "./GFC_AOI6_RGB_tiles"
#smp_path = "./smp2"

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
                    img_num = re.findall('\d+', file_img)[1]   # group 2
                    if img_num == num:
                        #print file_img
                        extract(file_bin, file_img, num)
                        break
                #print 'n_img =', n_img
                #n_img = n_img + 1

