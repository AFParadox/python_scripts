import os
import shutil

path_1 = '/home/leonardo/Documents/Unipd_Magistrale/1.2_computer_vision/Project/dataset_OFFICIAL/images/'
path_2 = '/home/leonardo/Documents/Unipd_Magistrale/1.2_computer_vision/Project/dataset_OFFICIAL/labels/'

for file in os.listdir(path_1):
    txt_name = file[:-4] + '.txt'
    if txt_name not in os.listdir(path_2):
        print(txt_name + ' missing')