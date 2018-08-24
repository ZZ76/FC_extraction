import os.path
import shutil

#sdir, tdir = './DFC_AOI6_RGB_tiles', './DFC_AOI6_RGB_tiles/trash'   # DFC original
#sdir, tdir = './DFC_AOI6_FC_tiles', './DFC_AOI6_FC_tiles/trash'   # DFC binary
#sdir, tdir = './GFC_AOI6_RGB_tiles', './GFC_AOI6_RGB_tiles/trash'   # GFC original
#sdir, tdir = './GFC_AOI6_FC_tiles', './GFC_AOI6_FC_tiles/trash'   # GFC binary
def moveFiles(sourceDir,targetDir):
    for files in os.listdir(sourceDir):
        sourceFile = os.path.join(sourceDir, files)
        targetFile = os.path.join(targetDir, files)
        #if os.path.isfile(sourceFile) and sourceFile.find('.TIF') < 0:
        if os.path.isfile(sourceFile) and files[-4:] != '.TIF':
            shutil.move(sourceFile, targetFile)
            print sourceFile, '=======>', targetFile

moveFiles(sdir, tdir)
