import os
import re

bin_path = "./bin"
img_path = "./img"
bin_files = os.listdir(bin_path)
img_files = os.listdir(img_path)
n_img = 0
for file_bin in bin_files:
    if not os.path.isdir(file_bin):   # search in bin folder find .tif file
        if file_bin[-4:] == '.TIF':
            num = re.findall('\d+', file_bin)[1]
            print(num)

            for file_img in img_files[n_img:]:   # search in img folder find the corresponding image
                #print(img_files[n_img:])
                if file_img[-4:] == '.TIF':
                    img_num = re.findall('\d+', file_img)[0]
                    if img_num == num:
                        print(file_img)
                        break
                print('n_img =', n_img)
                n_img = n_img + 1
        '''f = open(path+"/"+file);
        iter_f = iter(f)
        str = ""
        for line in iter_f:
            str = str + line
          s.append(str)'''