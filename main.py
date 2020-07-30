import os
import numpy as np
import cv2
import argparse


# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument('-i', '--images', type=str, required=True,
                default='./images',
                help='path to input directory of images to stitch')
ap.add_argument('-o', '--output', type=str, required=True,
                default='./images',
                help='path to the output image')
args = vars(ap.parse_args())


def list_images(base_path: str, contains=None):
    # return the set of files that are valid
    image_types = (".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff")
    return list_files(base_path, valid_exts=image_types, contains=contains)


def list_files(base_path: str, valid_exts=None, contains=None):
    # loop over the directory structure
    for (root_dir, dir_names, file_names) in os.walk(base_path):
        # loop over the file names in the current directory
        for file_name in file_names:
            # if the contains string is not none and the file name does not
            # contain the supplied string, then ignore the file
            if contains is not None and file_name.find(contains) == -1:
                continue

            # determine the file extension of the current file
            ext = file_name[file_name.rfind('.'):].lower()

            # check to see if the file is an image and should be processed
            if valid_exts is None or ext.endswith(valid_exts):
                # construct the path to the image and yield it
                image_path = os.path.join(root_dir, file_name)
                yield image_path


# grab the paths to the input images and initialize our images list
image_paths = sorted(list(list_images(args['images'])))
images = []

# loop over the image paths, load each one, and add them to our
# images to stitch list
for image_path in image_paths:
    image = cv2.imread(image_path)
    images.append(image)

stitcher = cv2.Stitcher_create()
(status, stitched) = stitcher.stitch(images)

if status == 0:
    # cv2.imwrite(args['output'], stitched)
    cv2.imshow('Stitched', stitched)
    cv2.waitKey(0)
else:
    print(f'[INFO] image stitching failed ({status})')
