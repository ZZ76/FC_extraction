import os.path
import cv2
import shutil

#sdir, tdir = './sample_source/smp_d', './smp_d_f'   # dfc
#sdir, tdir = './sample_source/smp_g', './smp_g_f'   # dfc
#sdir, letter = './gnd1', 'D'
#sdir, letter = './gnd2', 'G'
#sdir, tdir = './rrr', './rrr'
sdir, tdir = './track', './track'

sample_size = 100
def resizeimgs(sourceDir, targetDir):
    for files in os.listdir(sourceDir):
        sourceFile = os.path.join(sourceDir, files)
        #newfiles = files[:-4] + '_f' + files[-4:]
        targetFile = os.path.join(targetDir, files)
        if os.path.isfile(sourceFile):
            img = cv2.imread(sourceFile)
            newimg = cv2.resize(img, (sample_size, sample_size))
            cv2.imwrite(targetFile, newimg)
            print files

resizeimgs(sdir, tdir)
