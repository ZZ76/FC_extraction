import os
import re
import cv2
import numpy as np
from lxml.etree import Element, SubElement, tostring, ElementTree
import pprint
from xml.dom.minidom import parseString


def write_xml(filename, fc_array):
    node_root = Element('annotation')

    node_folder = SubElement(node_root, 'folder')
    node_folder.text = 'FCs'

    node_filename = SubElement(node_root, 'filename')
    node_filename.text = filename

    node_size = SubElement(node_root, 'size')
    node_width = SubElement(node_size, 'width')
    node_width.text = str(img_shape[0])

    node_height = SubElement(node_size, 'height')
    node_height.text = str(img_shape[1])

    node_depth = SubElement(node_size, 'depth')
    node_depth.text = str(img_shape[2])
    xd, yd = fc_array.shape[0], fc_array.shape[1]
    for i in range(0, xd):
        node_object = SubElement(node_root, 'object')
        node_name = SubElement(node_object, 'name')
        node_name.text = 'fc'
        node_truncated = SubElement(node_object, 'truncated')
        node_truncated.text = str(fc_array[i, 4])
        node_difficult = SubElement(node_object, 'difficult')
        node_difficult.text = '0'
        node_bndbox = SubElement(node_object, 'bndbox')
        node_xmin = SubElement(node_bndbox, 'xmin')
        node_xmin.text = str(fc_array[i, 0])
        node_ymin = SubElement(node_bndbox, 'ymin')
        node_ymin.text = str(fc_array[i, 1])
        node_xmax = SubElement(node_bndbox, 'xmax')
        node_xmax.text = str(fc_array[i, 2])
        node_ymax = SubElement(node_bndbox, 'ymax')
        node_ymax.text = str(fc_array[i, 3])
    tree = ElementTree(node_root)
    tree.write(save_xml_path + '/' + xml_name + '.xml', pretty_print=True, xml_declaration=False, encoding='utf-8')
    #xml = tostring(node_root, pretty_print=True)
    #dom = parseString(xml)
    #with open(save_path + '/' + xml_name + '.xml', 'w') as f:
    #    f.write(str(dom))
    #print(dom)


def extract(bin_name, img_name, num):
    global img_shape
    bin1 = cv2.imread(bin_path + '/' + bin_name, -1)
    bin2 = bin1.copy()
    #bin2 = cv2.cvtColor(bin1, cv2.COLOR_GRAY2BGR)
    bin2 = cv2.rectangle(bin2, (0, 0), (299, 299), (255, 255, 255), 1)
    img = cv2.imread(img_path + '/' + img_name)   # show for test
    #img2 = cv2.imread(img_path + '/' + img_name)
    img_shape = img.shape
    lower = np.array([10, 10, 10])
    upper = np.array([255, 255, 255])
    bin2 = cv2.inRange(bin2, lower, upper)
    _, contours, _ = cv2.findContours(bin2, 1, 2)
    cnt = contours
    print('number of contours = ', len(cnt))

    height, width = bin2.shape[:2]
    n = 1
    sample_size = 100
    first_printed_cnt = True   # if True, print imt_name
    for i in cnt:
        x, y, w, h = cv2.boundingRect(i)
        if w / h >= 4 or h / w >= 4:   # filter shape which is too narrow, or too edge
            pass
        else:
            x2 = x + w
            y2 = y + h
            x = int(x - w / 5)
            y = int(y - h / 5)
            x2 = int(x2 + w / 5)
            y2 = int(y2 + h / 5)
            trun = 0
            if x < 0:
                x = 0
                trun = 1
            if y < 0:
                y = 0
                trun = 1
            if x2 > width:
                x2 = width - 1
                trun = 1
            if y2 > height:
                y2 = height - 1
                trun = 1
            #if y < 0 or x < 0 or x2 > width or y2 > height or (x2 - x) < 20:   # do not use FC on border or size too small
                #pass
            if x2 - x <= 20 or y2 - y <= 20 or x2 - x >= 150 or y2 - y >= 150:   # filter fcs with too small size
                pass
            else:
                if first_printed_cnt is True:
                    print(img_name, x, y, x2, y2)
                    first_printed_cnt = False
                    fc_arr = np.array([[x, y, x2, y2, trun]])
                else:
                    print(x, y, x2, y2)
                    fc_arr = np.append(fc_arr, [[x, y, x2, y2, trun]], axis=0)

                #img = cv2.rectangle(img, (x, y), (x2, y2), (0, 255, 0), 2)   # draw contour and rectangle for test
                #cv2.drawContours(img, [i], 0, (0, 255, 0), 2)
    if first_printed_cnt is False:
        print(fc_arr)
        write_xml(img_name, fc_arr)
        cv2.imwrite(save_img_path + '/' + img_name, img)
        n = n + 1

    #cv2.imshow('bin', bin)   # show image for test
    #cv2.imshow(img_name, img)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

# group 1
#bin_path = "./DFC_bw_300"   # binary image folder
#img_path = "./DFC_300"   # raw image folder
#save_img_path = "./smp"   # sample image folder
# group 2
bin_path = "./GFC_bw_300"
img_path = "./GFC_300"
save_img_path = "./smp"

#save_xml_path = './xml_Test'
save_xml_path = './xml'

bin_files = os.listdir(bin_path)
img_files = os.listdir(img_path)
#n_img = 0   # pointer in image folder
img_shape = None
xml_name = None
for file_bin in bin_files:
    if not os.path.isdir(file_bin):   # search in bin folder find .tif file
        if file_bin[-4:] == '.TIF':
            num = re.findall('\d+', file_bin)[-1]
            print(num)

            #for file_img in img_files[n_img:]:   # search in img folder find the corresponding image
            for file_img in img_files:
                #print img_files[n_img:]
                if file_img[-4:] == '.jpg':
                    #img_num = re.findall('\d+', file_img)[0]   # number(0 or 1) in [] may change according to file name
                    img_num = re.findall('\d+', file_img)[-1]   # group 2
                    xml_name = file_img[:-4]
                    if img_num == num:
                        #print file_img
                        extract(file_bin, file_img, num)
                        break
                #print 'n_img =', n_img
                #n_img = n_img + 1

