import cv2
import numpy as np
import random

def selectground(width, height):
    counter = 0
    while counter < select_num:
        l = random.randint(50, 500)  # square length
        xg = random.randint(0, width - l)  # start position x
        yg = random.randint(0, height - l)  # start position y
        gp = [(xg, yg), (xg + l, yg), (xg + l, yg + l), (xg, yg + l)]
        gcnt = [np.array([gp])]
        print 'gp = ', gp
        counter = counter + 1
        cv2.drawContours(img, gcnt, 0, (0, 0, 255), 5)
        cv2.putText(img, str(counter), gp[3], font, 1, (255, 255, 255), 2, cv2.LINE_AA)
        #name = 'smp' + str(counter)
        #smp = img2[gp[0][1]:gp[2][1], gp[0][0]:gp[2][0]]
        #cv2.imwrite(smp_path + '/' + name + '.jpg', smp)
        #cv2.imshow(name, smp)


select_num = 30
smp_path = './2'   # saving path
font = cv2.FONT_HERSHEY_SIMPLEX
image_name = 'nationalgeographic_1022083.jpg'   # image for selecting
img = cv2.imread(image_name, 1)
img2 = img.copy
height, width = img.shape[:2]
n = 1
selectground(width, height)
img = cv2.resize(img, (width/5, height/5))
cv2.imshow('img', img)

cv2.waitKey(0)
cv2.destroyAllWindows()