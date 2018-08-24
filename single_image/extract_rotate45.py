import cv2
import numpy as np
import os
import re
import math


def extract_rotate45(bin_name, img_name, num, letter=None, save=False):
    bin = cv2.imread(bin_path + '/' + bin_name, -1)
    bin2 = cv2.cvtColor(bin, cv2.COLOR_GRAY2BGR)
    img = cv2.imread(img_path + '/' + img_name)   # original image to show bounding boxes
    img2 = img.copy()   # original image to extract fcs

    lower = np.array([0,0,0])
    upper = np.array([255,255,255])
    bin2 = cv2.inRange(bin2, lower, upper)

    _, contours, _ = cv2.findContours(bin2, 1, 2)
    cnt = contours
    print 'length = ', len(cnt)

    height, width = bin2.shape[:2]
    n = 1
    #scale_rate = 0.5   # zoom in (2/scale_rate) of bounding box
    sample_size = 100
    #print(scale_rate)
    for i in cnt:
        print 'n = ', n
        #if n == len(cnt):
            #break
        x, y, w, h = cv2.boundingRect(i)
        if w > h:
            y = y - (w - h) / 2   # adjust y1 location
            tmp = w   # long side for square length
        else:
            x = x - (h - w) / 2   # or adjust x1 location
            tmp = h   # long side length
        x2 = x + tmp
        y2 = y + tmp
        x = x - int(tmp / 1.5)   # 2
        y = y - int(tmp / 1.5)
        x2 = x2 + int(tmp / 1.5)   # 2
        y2 = y2 + int(tmp / 1.5)

        if y < 0 or x < 0 or x2 > width or y2 > height or (x2 - x) < 20:
            pass
        else:
            print x, y, x2, y2
            img = cv2.rectangle(img, (x, y), (x2, y2), (0, 255, 0), 2)
            cv2.drawContours(img, [i], 0, (0, 255, 0), 2)
            fc = img2[y:y2, x:x2]
            rows, cols = fc.shape[:2]
            M = cv2.getRotationMatrix2D((cols / 2, rows / 2), 45, 1.42)   # scale is sqrt(2), use 1.42 here
            fc = cv2.warpAffine(fc, M, (cols, rows))
            fc = cv2.resize(fc, (sample_size, sample_size))
            name = str(num) + '_' + str(n)
            if letter is not None:
                name = letter + '_' + name
            if save is True:
                cv2.imwrite(smp_path + '/' + name + '.jpg', fc)
            else:
                cv2.imshow(name, fc)
                cv2.imshow('bin', bin)
                #cv2.imshow('bin2', bin2)
                cv2.imshow('img', img)
        n = n+1


def read_filse_and_extract():
    bin_files = os.listdir(bin_path)
    img_files = os.listdir(img_path)
    #n_img = 0   # pointer in image folder
    for file_bin in bin_files:
        if not os.path.isdir(file_bin):   # search in bin folder find .tif file
            if file_bin[-4:] == '.TIF':
                num = re.findall('\d+', file_bin)[-1]
                print num

                #for file_img in img_files[n_img:]:   # search in img folder find the corresponding image
                for file_img in img_files:
                    #print img_files[n_img:]
                    if file_img[-4:] == '.TIF':
                        #img_num = re.findall('\d+', file_img)[0]   # group 1 number(0 or 1) in [] may change according to file name
                        img_num = re.findall('\d+', file_img)[-1]   # group 2
                        if img_num == num:
                            #print file_img
                            extract_rotate45(file_bin, file_img, num, letter=L, save=True)
                            break

bnr_image_name = 'DFC_AOI6_FC_tiles426.TIF'
image_name = 'DFC_AOI_RGB_tile426.TIF'
# group 1
bin_path = "./DFC_AOI6_FC_tiles"   # binary image folder
img_path = "./DFC_AOI6_RGB_tiles"   # raw image folder
smp_path = "./smp1"   # sample image folder
L = 'D45'
# group 2
#bin_path = "./GFC_AOI6_FC_tiles"
#img_path = "./GFC_AOI6_RGB_tiles"
#smp_path = "./smp2"
#L = 'G45'

#read_filse_and_extract()
extract_rotate45(bnr_image_name, image_name, 0)

cv2.waitKey(0)
cv2.destroyAllWindows()
