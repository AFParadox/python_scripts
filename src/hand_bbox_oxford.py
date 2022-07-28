import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
import magic, re, scipy.io
import requests, tarfile
import torch, random
import numpy as np
from IPython.display import Image, clear_output
import os, shutil


def get_width_height_from_img_path(file_full_path : str) -> np.ndarray:
    t = magic.from_file(filename=file_full_path)
    print(t)
    size_str = re.search("(\d+)x(\d+)", t[106:120]).groups() # format is WxH
    size = np.array(object=(float(size_str[0]), float(size_str[1])), dtype=float)
    return size

def extract_annotation(annotations_full_path : str) -> list: 
    # load mat file and get correct data
    annotation = scipy.io.loadmat(annotations_full_path)
    boxes = annotation.get("boxes")

    # convert to ndarray
    hand_boxes_accurate : list[np.ndarray] = []
    for i in range(boxes.shape[1]):
        pts = np.zeros(shape=(4,2), dtype=int)
        for j in range(4):
            pts[j,0] = round(boxes[0,i][0,0][j][0,1])
            pts[j,1] = round(boxes[0,i][0,0][j][0,0])
        hand_boxes_accurate.append(pts)
        del(pts)
    
    return hand_boxes_accurate

def convert_box_to_yolov5_std_str(img_size : np.ndarray, hand_box : np.ndarray) -> str:
    # calculate relaxed bbox coordinates
    top_left_pt = np.zeros(shape=2, dtype=float)
    bottom_right_pt = np.zeros(shape=2, dtype=float)
    np.amin(hand_box, axis=0, out=top_left_pt)
    np.amax(hand_box, axis=0, out=bottom_right_pt)

    # compute bbox size
    bbox_size = bottom_right_pt - top_left_pt

    # compute bbox center
    center = top_left_pt + bbox_size/2.

    # normalization (image width and height considered as 1)
    bbox_size = bbox_size / img_size
    center = center / img_size

    # here the initial zero represent the class of the object, since all are hands it is always the same
    return "0 {:.6f} {:.6f} {:.6f} {:.6f}".format(center[0],center[1],bbox_size[0],bbox_size[1])

def save_annotations_to_txt(img_size : np.ndarray, bad_annotation : list, new_annotation_path : str):
    txt = open(new_annotation_path, "w")

    final_annotation : str = ""
    for annot in bad_annotation:
        final_annotation += convert_box_to_yolov5_std_str(img_size=img_size, hand_box=annot) + "\n"
    
    txt.write(final_annotation[:len(final_annotation)-2])   # do not write last \n
    
    txt.close()

datasets_extr = ['/home/leonardo/Downloads/hand_dataset/training_dataset/training_data/', '/home/leonardo/Downloads/hand_dataset/validation_dataset/validation_data/', '/home/leonardo/Downloads/hand_dataset/test_dataset/test_data/']


for dir_path in datasets_extr:

    if not os.path.exists(dir_path+"labels"):  # create dir containing new labels
        os.mkdir(path=dir_path+"labels")
    
    for file_name in os.listdir(path=dir_path+"images/"):

        cur_img_full_path = dir_path + "images/" + file_name
        cur_size = get_width_height_from_img_path(cur_img_full_path) # get width & height of current image
        #print(curr_size)

        cur_annot_full_path = dir_path + "annotations/" + file_name[:len(file_name)-4] + ".mat"
        cur_annotation = extract_annotation(cur_annot_full_path)
        #print(cur_annotation[0])

        new_annot_full_path = dir_path + "labels/" + file_name[:len(file_name)-4] + ".txt"
        save_annotations_to_txt(img_size=cur_size, bad_annotation=cur_annotation, new_annotation_path=new_annot_full_path)