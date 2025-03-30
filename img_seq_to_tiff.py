import os
import numpy as np
import cv2
import tifffile as tiff
from tqdm.notebook import tqdm
from concurrent.futures import ThreadPoolExecutor

def __load_image(img_path):
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError(f"Image {img_path} could not be read")
    return img

def create_3d_tiff(image_folder, output_path):
    """
    Create 3D TIFF from image sequence at path and save to disk.
    Args:
        image_folder (path): Path to images to create 3D TIFF from.
        output_path (path): Path to save the 3D TIFF.
    Returns:
        None
    """
    # Get list of image files in the folder
    files = sorted([os.path.join(image_folder, f) for f in os.listdir(image_folder) if f.endswith(('.png', '.jpg', '.jpeg', '.tif', '.tiff'))])
    
    # Load images in parallel and stack them into a 3D numpy array
    with ThreadPoolExecutor() as executor:
        images = list(executor.map(__load_image, files))
    
    # Convert list of images to a 3D numpy array
    stack = np.stack(images, axis=0)
    
    # Save the 3D array as a .tiff file using tifffile
    tiff.imwrite(output_path, stack)