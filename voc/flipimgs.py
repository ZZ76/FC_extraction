import os.path
import cv2
import shutil

#sdir, tdir = './DFC_300', './DFC_300'
#sdir, tdir = './DFC_bw_300', './DFC_bw_300'
#sdir, tdir = './GFC_300', './GFC_300'
#sdir, tdir = './GFC_bw_300', './GFC_bw_300'

def flipimgs(sourceDir, targetDir):
    for files in os.listdir(sourceDir):
        sourceFile = os.path.join(sourceDir, files)
        newfiles = files[:-4] + '_f' + files[-4:]
        targetFile = os.path.join(targetDir, newfiles)
        if os.path.isfile(sourceFile):
            img = cv2.imread(sourceFile)
            newimg = cv2.flip(img, 1)
            cv2.imwrite(targetFile, newimg)
            print(sourceFile, '=======>', targetFile)

flipimgs(sdir, tdir)
