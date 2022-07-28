import os

path_1 = '/home/leonardo/Documents/Unipd_Magistrale/1.2_computer_vision/Project/dataset_OFFICIAL/oxford/test/images/'
path_2 = '/home/leonardo/Documents/Unipd_Magistrale/1.2_computer_vision/Project/dataset_OFFICIAL/oxford/test/labels/'

starting_point = 40000
counter = 0

for file in sorted(os.listdir(path_2)):
    new_name = str(starting_point + counter) + '.txt'
    print(file)
    print(new_name)
    os.rename(path_2+file, path_2+new_name)
    counter += 1