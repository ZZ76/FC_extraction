import os.path
import shutil
import numpy as np

# read files from sdir, shuffle and cut to ddir

#sdir, letter = './smp1', 'D'
#sdir, letter = './smp2', 'G'
#sdir, letter = './rrr', 'R'
#sdir, letter = './gnd1', 'D'
#sdir, letter = './gnd2', 'G'
#sdir, letter = './track3', 'T'
sdir, ddir = './touse/t2', './touse/t'

def renameFiles(sourceDir,letter):
    for files in os.listdir(sourceDir):
        sourceFile = os.path.join(sourceDir, files)
        targetFile = os.path.join(sourceDir, letter + '_' + files)
        #if os.path.isfile(sourceFile) and sourceFile.find('.TIF') < 0:
        if os.path.isfile(sourceFile):
            #shutil.move(sourceFile, targetFile)
            os.rename(sourceFile, targetFile)
            print sourceFile, '=======>', targetFile

def renametonumber(sourceDir, destinationDir):
    n = 1
    sourceFile = []
    for files in os.listdir(sourceDir):
        sourceFile.append(os.path.join(sourceDir, files))
    np.random.shuffle(sourceFile)
    #print sourceFile
    for f in sourceFile:
        targetFile = os.path.join(destinationDir, str(n) + files[-4:])
        if os.path.isfile(f):
            #shutil.move(f, targetFile)
            os.rename(f, targetFile)
            print f, '=======>', targetFile
            n = n + 1

#renameFiles(sdir, letter)
renametonumber(sdir, ddir)
