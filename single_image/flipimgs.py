import os.path
import cv2
import shutil

#sdir, tdir = './sample_source/smp_d', './smp_d_f'   # dfc
#sdir, tdir = './sample_source/smp_g', './smp_g_f'   # dfc
#sdir, letter = './gnd1', 'D'
#sdir, letter = './gnd2', 'G'
#sdir, tdir = './rrr', './rrr/new'
#sdir, tdir = './thing', './thing2'
sdir, tdir = './g', './g'
def flipimgs(sourceDir, targetDir):
    for files in os.listdir(sourceDir):
        sourceFile = os.path.join(sourceDir, files)
        newfiles = files[:-4] + '_f' + files[-4:]
        targetFile = os.path.join(targetDir, newfiles)
        if os.path.isfile(sourceFile):
            img = cv2.imread(sourceFile)
            newimg = cv2.flip(img, 1)
            cv2.imwrite(targetFile, newimg)
            print sourceFile, '=======>', targetFile

flipimgs(sdir, tdir)
