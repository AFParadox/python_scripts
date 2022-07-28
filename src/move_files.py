import os
import shutil


def move_it(path_1, path_2):
    for dir in os.scandir(path_1):              
        if dir.is_file():                       # If we find a file we move it
            shutil.copy(dir, path_2)
            print(str(dir) + 'got moved!')      
        elif dir.is_dir():                      # If we find a sub-directory we explore it
            move_it(dir, path_2)


# Here we set the starting directory and the goal directory
path_1 = '/home/leonardo/Documents/Unipd_Magistrale/1.2_computer_vision/Project/dataset_OFFICIAL/oxford/train/labels/'
path_2 = '/home/leonardo/Documents/Unipd_Magistrale/1.2_computer_vision/Project/dataset_OFFICIAL/labels/'

move_it(path_1, path_2)