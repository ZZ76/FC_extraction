import os.path
import cv2
import shutil

#sdir, tdir = './DFC', './DFC_300'
sdir, tdir = './DFC_bw', './DFC_bw_300'
#sdir, tdir = './GFC', './GFC_300'
#sdir, tdir = './GFC_bw', './GFC_bw_300'

sample_size = 300
def resizeimgs(sourceDir, targetDir):
    for files in os.listdir(sourceDir):
        sourceFile = os.path.join(sourceDir, files)
        #newfiles = files[:-4] + '_f' + files[-4:]
        files_jpg = files
        #files_jpg = files_jpg.replace('.TIF', '.jpg')   # jpg for rgb images
        targetFile = os.path.join(targetDir, files_jpg)
        if os.path.isfile(sourceFile):
            img = cv2.imread(sourceFile, -1)   # -1 for binary images
            newimg = cv2.resize(img, (sample_size, sample_size))
            cv2.imwrite(targetFile, newimg)
            print(files)

resizeimgs(sdir, tdir)
