import os.path
import shutil



#sdir, letter = './smp1', 'D'
#sdir, letter = './smp2', 'G'
#sdir, letter = './rrr', 'R'
#sdir, letter = './gnd1', 'D'
#sdir, letter = './gnd2', 'G'
#sdir, letter = './track3', 'T'
sdir, tdir = './g2', './g'


def renameFiles(sourceDir,letter):   # put _ + letter in front of all file in sdir example: image.jpg ===> D_image.jpg
    for files in os.listdir(sourceDir):
        sourceFile = os.path.join(sourceDir, files)
        targetFile = os.path.join(sourceDir, letter + '_' + files)
        #if os.path.isfile(sourceFile) and sourceFile.find('.TIF') < 0:
        if os.path.isfile(sourceFile):
            #shutil.move(sourceFile, targetFile)
            os.rename(sourceFile, targetFile)
            print sourceFile, '=======>', targetFile


def renametonumber(sourcedir, targetdir):   # rename files with number
    n = 8425   # start number
    for files in os.listdir(sourcedir):
        sourceFile = os.path.join(sourcedir, files)
        targetFile = os.path.join(targetdir, str(n) + files[-4:])
        #if os.path.isfile(sourceFile) and sourceFile.find('.TIF') < 0:
        if os.path.isfile(sourceFile):
            #shutil.move(sourceFile, targetFile)
            os.rename(sourceFile, targetFile)
            print sourceFile, '=======>', targetFile
            n = n + 1

#renameFiles(sdir, letter)
renametonumber(sdir, tdir)
