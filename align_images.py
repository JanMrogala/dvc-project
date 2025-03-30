# Sourced from: https://docs.opencv.org/4.x/d4/dc6/tutorial_py_template_matching.html
import os
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
from tqdm import tqdm

def __shift_img(original_img, row_shift, col_shift, save_path):
        rows = original_img.shape[0]
        cols = original_img.shape[1]

        # create new image with the same shape as original image
        new_img = np.zeros_like(original_img, np.uint8)

        # if the image was shifted down and left, place the original image in the new image accordingly
        if(row_shift >= 0 and col_shift <= 0):
            new_img[:rows-row_shift, -col_shift:] = original_img[row_shift:, :cols+col_shift]
        # if the image was shifted down and right, ...
        elif(row_shift >= 0 and col_shift >= 0):
            new_img[:rows-row_shift, :cols-col_shift] = original_img[row_shift:, col_shift:]
        # if the image was shifted up and left, ...
        elif(row_shift <= 0 and col_shift <= 0):
            new_img[-row_shift:, -col_shift:] = original_img[:rows+row_shift, :cols+col_shift]
        # if the image was shifted up and right, ...
        elif(row_shift <= 0 and col_shift >= 0):
            new_img[-row_shift:, :cols-col_shift] = original_img[:rows+row_shift, col_shift:]

        # save new_img
        cv.imwrite(save_path, new_img)

def align(ref_folder_path, def_folder_path, save_folder_path, row_range, col_range):
    """
    Align images by shifting. Saves aligned images to save_folder_path.
    Args:
        ref_folder_path (path): Path to reference images.
        def_folder_path (path): Path to deformed images.
        save_folder_path (path): Path to save aligned images.
        row_range (tuple): Range of rows to focus on.
        col_range (tuple): Range of columns to focus on.
    Returns:
        Tuple of row and column shift values.
    """

    if os.path.exists(save_folder_path):
        return

    files = sorted(os.listdir(ref_folder_path))
    middle_file = files[len(files) // 2]
    ref_path = os.path.join(ref_folder_path, middle_file)

    files = sorted(os.listdir(def_folder_path))
    middle_file = files[len(files) // 2]
    def_path = os.path.join(def_folder_path, middle_file)

    if not os.path.exists(save_folder_path):
        os.makedirs(save_folder_path)

    img = cv.imread(def_path, cv.IMREAD_GRAYSCALE)
    assert img is not None, "File could not be read, check correct path and file name."
    img2 = img.copy()
    template = cv.imread(ref_path, cv.IMREAD_GRAYSCALE)[row_range[0]:row_range[1], col_range[0]:col_range[1]]
    assert template is not None, "File could not be read, check correct path and file name."
    w, h = template.shape[::-1]

    # show img2
    # plt.imshow(template,cmap = 'gray')
    # plt.show()
    # 5 methods for comparison in a list
    methods = ['TM_CCOEFF', 'TM_CCOEFF_NORMED',
                'TM_CCORR_NORMED', 'TM_SQDIFF', 'TM_SQDIFF_NORMED']
    
    row_shift_mean = 0
    col_shift_mean = 0

    for meth in methods:
        img = img2.copy()
        method = getattr(cv, meth)
    
        # Apply template Matching
        res = cv.matchTemplate(img,template,method)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
    
        # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
        if method in [cv.TM_SQDIFF, cv.TM_SQDIFF_NORMED]:
            top_left = min_loc
        else:
            top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)
        
        row_shift_mean += (top_left[1] - row_range[0])
        col_shift_mean += (top_left[0] - col_range[0])

    row_shift_mean = int(row_shift_mean / len(methods))
    col_shift_mean = int(col_shift_mean / len(methods))

    # go through every image in the folder and shift it by using the shift_img function
    for filename in tqdm(os.listdir(def_folder_path), desc="Shifting images"):
        if filename.endswith(".tif"):
            img = cv.imread(os.path.join(def_folder_path, filename), cv.IMREAD_GRAYSCALE)
            __shift_img(img, row_shift_mean, col_shift_mean, os.path.join(save_folder_path, filename))

    # return row and column shift values
    return row_shift_mean, col_shift_mean