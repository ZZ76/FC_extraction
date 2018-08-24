import os
import re
import cv2
import numpy as np

# test
#src_path = './smp_test'
#dst_path = './smp_test_rotated'

# smp1
#src_path = './smp1'
#dst_path = './smp1_rotated'

# smp2
#src_path = './smp2'
#dst_path = './smp2_rotated'

# dfc
#src_path = './smp_d_f'
#dst_path = './smp_d_f_r'

# gfc
#src_path = './smp_g_f'
#dst_path = './smp_g_f_r'

src_path = './g'
dst_path = './g2'

sample_size = 100

def rotate_save(name):
    img = cv2.imread(src_path + '/' + name)
    rows, cols = img.shape[:2]
    #print rows, cols
    new_name = name[:-4] + '_1' + name[-4:]
    print 'new_name = ', new_name
    cv2.imwrite(dst_path + '/' + new_name, img)
    for n in range(2, 5, 1):
        M = cv2.getRotationMatrix2D((cols / 2, rows / 2), 90, 1)
        #print M
        img = cv2.warpAffine(img, M, (cols, rows))
        #M2 = np.float32([[1, 0, 0], [0, 1, -1]])
        #img = cv2.warpAffine(img, M2, (cols, rows))
        new_img = img[1:100, 1:100]   # get rid of black border after affine transformation
        new_img = cv2.resize(new_img, (sample_size, sample_size))
        new_name = name[:-4] + '_' + str(n) + name[-4:]
        print 'new_name = ', new_name
        cv2.imwrite(dst_path + '/' + new_name, new_img)
        n = n + 1


src_files = os.listdir(src_path)
for img in src_files:
    if not os.path.isdir(img):
        print img
        rotate_save(img)
        pass