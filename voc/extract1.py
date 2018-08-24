import cv2
import numpy as np
import matplotlib.cm as mpcm
import random
from matplotlib._cm import cubehelix


def colors_subselect(colors, num_colors=10):
    dt = len(colors) // num_colors
    sub_colors = []
    for i in range(num_colors):
        color = colors[i*dt]
        if isinstance(color[0], float):
            sub_colors.append([int(c * 255) for c in color])
        else:
            sub_colors.append([c for c in color])
    return sub_colors
colors_plasma = colors_subselect(mpcm.viridis.colors, num_colors=20)   # 'viridis', 'plasma', 'inferno', 'magma', cubehelix
#print colors_plasma.size
print (colors_plasma)
#print len(colors_plasma[0])
for i in range(0, len(colors_plasma)):
    temp = colors_plasma[i][0]
    colors_plasma[i][0] = colors_plasma[i][2]
    colors_plasma[i][2] = temp
print (colors_plasma)
#color1 = colors_plasma[random.randint(15, 20)]
#color2 = colors_plasma[random.randint(0, 5)]

bnr_image_name = 'DFC_AOI6_FC_tiles303.TIF'
image_name = 'DFC_AOI_RGB_tile303.TIF'
bin1 = cv2.imread(bnr_image_name, -1)
bin2 = cv2.imread(bnr_image_name, -1)
bin = cv2.cvtColor(bin1, cv2.COLOR_GRAY2BGR)
img = cv2.imread(image_name)
img2 = img.copy()

#ret,thresh = cv2.threshold(bin,127,255,cv2.THRESH_BINARY_INV)

#bin = cv2.cvtColor(bin, cv2.COLOR_BGR2HSV)
#cv2.imshow('i1', bin)
lower = np.array([0, 0, 0])
upper = np.array([255, 255, 255])
bin = cv2.inRange(bin, lower, upper)

# Bitwise-AND mask and original image
#res = cv2.bitwise_and(bin,bin, mask= mask)

_, contours, _ = cv2.findContours(bin, 1, 2)
cnt = contours
print ('length = ', len(cnt))

height, width = bin.shape[:2]
n = 1
scale_rate = 4   # enlarge in (2/scale_rate) of bounding box
sample_size = 100
print(scale_rate)
for i in cnt:
    print ('n = ', n)
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
    x = x - tmp / scale_rate   # x extend 20% to left
    y = y - tmp / scale_rate
    x2 = x2 + tmp / scale_rate   # x extend 20% to right 40% in total
    y2 = y2 + tmp / scale_rate

    if y < 0 or x < 0 or x2 > width or y2 > height or (x2 - x) < 20:
        color2 = colors_plasma[random.randint(0, 5)]
        #cv2.drawContours(img, [i], 0, (0, 0, 255), 2)
        cv2.drawContours(img, [i], 0, color2, 2)
        if x < 0:
            x = 0
        if y < 0:
            y = 0
        if x2 > width:
            x2 = width - 1
        if y2 > height:
            y2 = height - 1
        #img = cv2.rectangle(img, (x, y), (x2, y2), (0, 0, 255), 2)
        img = cv2.rectangle(img, (x, y), (x2, y2), color2, 2)
        pass
    else:
        print (x, y, x2, y2)
        color1 = colors_plasma[random.randint(14, 19)]
        #img = cv2.rectangle(img, (x, y), (x2, y2), (0, 255, 0), 2)
        img = cv2.rectangle(img, (x, y), (x2, y2), color1, 2)
        #cv2.drawContours(img, [i], 0, (0, 255, 0), 2)
        cv2.drawContours(img, [i], 0, color1, 2)
        fc = img2[y:y2, x:x2]
        fc = cv2.resize(fc, (sample_size, sample_size))
        name = 'fc' + str(n)
        #cv2.imwrite(name+'.jpg', fc)
        cv2.imshow(name, fc)
    n = n+1


#cv2.imshow('bin', bin)
cv2.imshow('bin2', bin2)
cv2.imshow('img', img)

cv2.waitKey(0)
cv2.destroyAllWindows()