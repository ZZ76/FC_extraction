import os.path
import shutil


#sdir, tdir = './DFC_300', './tmp'
#sdir, tdir = './DFC_bw_300', './tmp2'
#sdir, tdir = './GFC_300', './tmp'
sdir, tdir = './GFC_bw_300', './tmp2'

def renameFiles(sourceDir,letter):   # put _ + letter in front of all file in sdir example: image.jpg ===> D_image.jpg
    for files in os.listdir(sourceDir):
        sourceFile = os.path.join(sourceDir, files)
        targetFile = os.path.join(sourceDir, letter + '_' + files)
        #if os.path.isfile(sourceFile) and sourceFile.find('.TIF') < 0:
        if os.path.isfile(sourceFile):
            #shutil.move(sourceFile, targetFile)
            os.rename(sourceFile, targetFile)
            print(sourceFile, '=======>', targetFile)


def renametonumber(sourcedir, targetdir):   # rename files with number
    n = 3073   # start number
    for files in os.listdir(sourcedir):
        sourceFile = os.path.join(sourcedir, files)
        s = str(n).zfill(5)
        targetFile = os.path.join(targetdir, s + files[-4:])
        #if os.path.isfile(sourceFile) and sourceFile.find('.TIF') < 0:
        if os.path.isfile(sourceFile):
            #shutil.move(sourceFile, targetFile)
            os.rename(sourceFile, targetFile)
            print(sourceFile, '=======>', targetFile)
            n = n + 1

#renameFiles(sdir, letter)
renametonumber(sdir, tdir)
