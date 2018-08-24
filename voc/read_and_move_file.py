import os.path
import shutil
import re
import os

#bin_path = "./bin"   # binary folder
#img_path = "./img"   # rgb folder

bin_path = "./DFC_bw"   # binary folder
img_path = "./DFC"   # rgb folder
bin_files = os.listdir(bin_path)
img_files = os.listdir(img_path)
#n_img = 0
sdir, tdir = img_path, './DFC2'   # rgb folder and new rgb folder

def MoveFiles(sourceDir,targetDir, file):
    sourceFile = os.path.join(sourceDir, file)
    targetFile = os.path.join(targetDir, file)
    #if os.path.isfile(sourceFile) and sourceFile.find('.TIF') < 0:
    if os.path.isfile(sourceFile) and file[-4:] == '.TIF':
        shutil.move(sourceFile, targetFile)
        print(sourceFile, '=======>', targetFile)


def ReadandMove(bnrfolder, imgfolder):
    for file_bin in bnrfolder:
        if not os.path.isdir(file_bin):   # search in bin folder find .tif file
            if file_bin[-4:] == '.TIF':
                num = re.findall('\d+', file_bin)[-1]
                print('num = ', num)
                for file_img in imgfolder:   # search in img folder find the corresponding image
                    #print(img_files[n_img:])
                    if file_img[-4:] == '.TIF':
                        img_num = re.findall('\d+', file_img)[-1]
                        if img_num == num:
                            print(file_img)
                            #MoveFiles(sdir, tdir, file_img)   # Move File to target folder
                            break
                else:
                    print('no such file !!!', num)

#moveFiles(sdir, tdir)
ReadandMove(bin_files, img_files)
