# (This is in iPython)
import spam.DIC
import spam.deformation
import numpy as np
import tifffile
import os

import spam.scripts
import spam.scripts.deformImage
import spam.scripts.reg

original_data_folder = '../../../../bigdisk/mrogala/DIC/DATA_DIC_PROCESSED'

voxel_size_G16057_K13_5 = 0.01324579  # in mm
voxel_size_G16060_K12_5 = 0.01401936
voxel_size_G16060_P7_5 = 0.01401936
voxel_size_G16057_P4_5 = 0.01325482
voxel_size_G16060_K3_5 = 0.01401936
voxel_size_G16060_P11_5 = 0.01401936
voxel_size_G16057_P12_5 = 0.01325477


lab_x = -0.011
lab_y = -0.003
lab_z = 0.042

lab_x_rot = 0.02
lab_y_rot = 0.08
lab_z_rot = -0.01

transformation_G16057_K13_5_1 = {'t': [round(x / voxel_size_G16057_K13_5, 2) for x in [lab_y, -lab_z, lab_x]], 'r': [-lab_y_rot, lab_z_rot, -lab_x_rot]}
transformation_G16057_K13_5_2 = {'t': [round(x / voxel_size_G16057_K13_5, 2) for x in [-0.008, -0.084, -0.014]], 'r': [-0.12, -0.02, -0.03]}
transformation_G16057_K13_5_3 = {'t': [round(x / voxel_size_G16057_K13_5, 2) for x in [-0.013, -0.124, -0.021]], 'r': [-0.15, -0.02, -0.03]}

transformation_G16060_P7_5_1 = {'t': [round(x / voxel_size_G16060_P7_5, 2) for x in [0.010, -0.137, -0.014]], 'r': [-0.08, -0.02, 0.04]}
transformation_G16060_P7_5_2 = {'t': [round(x / voxel_size_G16060_P7_5, 2) for x in [0.017, -0.248, -0.018]], 'r': [-0.09, -0.04, 0.03]}
transformation_G16060_P7_5_3 = {'t': [round(x / voxel_size_G16060_P7_5, 2) for x in [0.023, -0.352, -0.030]], 'r': [-0.11, -0.07, 0.02]}

transformation_G16057_P4_5_1 = {'t': [round(x / voxel_size_G16057_P4_5, 2) for x in [0.013, -0.038, -0.012]], 'r': [-0.03, -0.01, -0.04]}
transformation_G16057_P4_5_2 = {'t': [round(x / voxel_size_G16057_P4_5, 2) for x in [0.015, -0.078, -0.018]], 'r': [-0.04, -0.02, -0.08]}
transformation_G16057_P4_5_3 = {'t': [round(x / voxel_size_G16057_P4_5, 2) for x in [0.022, -0.120, -0.018]], 'r': [-0.03, -0.02, -0.11]}

transformation_G16060_K12_5_1 = {'t': [round(x / voxel_size_G16060_K12_5, 2) for x in [0.009, -0.137, 0.003]], 'r': [-0.06, -0.02, 0.02]}
transformation_G16060_K12_5_2 = {'t': [round(x / voxel_size_G16060_K12_5, 2) for x in [0.004, -0.252, 0.005]], 'r': [-0.07, -0.04, 0.02]}
transformation_G16060_K12_5_3 = {'t': [round(x / voxel_size_G16060_K12_5, 2) for x in [0.003, -0.361, 0.005]], 'r': [-0.08, -0.06, 0.03]}
transformation_G16060_K12_5_4 = {'t': [round(x / voxel_size_G16060_K12_5, 2) for x in [-0.008, -0.436, -0.006]], 'r': [-0.09, -0.08, 0.04]}

transformation_G16060_K3_5_1 = {'t': [round(x / voxel_size_G16060_K3_5, 2) for x in [-0.004, -0.211, 0.002]], 'r': [-0.01, -0.02, -0.05]}
transformation_G16060_K3_5_2 = {'t': [round(x / voxel_size_G16060_K3_5, 2) for x in [-0.011, -0.320, 0.007]], 'r': [-0.01, -0.04, -0.05]}
transformation_G16060_K3_5_3 = {'t': [round(x / voxel_size_G16060_K3_5, 2) for x in [-0.017, -0.430, 0.010]], 'r': [-0.01, -0.06, -0.05]}
transformation_G16060_K3_5_4 = {'t': [round(x / voxel_size_G16060_K3_5, 2) for x in [-0.020, -0.506, 0.013]], 'r': [-0.01, -0.08, -0.05]}

transformation_G16060_P11_5_1 = {'t': [round(x / voxel_size_G16060_P11_5, 2) for x in [0.002, -0.162, -0.009]], 'r': [-0.02, -0.02, 0.14]}
transformation_G16060_P11_5_2 = {'t': [round(x / voxel_size_G16060_P11_5, 2) for x in [-0.002, -0.279, -0.013]], 'r': [-0.01, -0.04, 0.13]}
transformation_G16060_P11_5_3 = {'t': [round(x / voxel_size_G16060_P11_5, 2) for x in [-0.011, -0.396, -0.023]], 'r': [0.01, -0.07, 0.13]}

transformation_G16057_P12_5_1 = {'t': [round(x / voxel_size_G16057_P12_5, 2) for x in [-0.002, -0.048, 0.002]], 'r': [0.05, -0.01, 0.02]}
transformation_G16057_P12_5_2 = {'t': [round(x / voxel_size_G16057_P12_5, 2) for x in [0.060, -0.136, -0.128]], 'r': [0.05, -0.24, 0.03]}
transformation_G16057_P12_5_3 = {'t': [round(x / voxel_size_G16057_P12_5, 2) for x in [-0.045, -0.173, -0.097]], 'r': [0.09, -0.24, 0.04]}
transformation_G16057_P12_5_4 = {'t': [round(x / voxel_size_G16057_P12_5, 2) for x in [-0.043, -0.170, -0.090]], 'r': [0.11, -0.24, 0.04]}


def align_images(transformation, name, num):
    os.makedirs(f'../../../../bigdisk/mrogala/DIC/DATA_DIC_PROCESSED/3D_TIFF_ALIGNED_NEW/{name}', exist_ok=True)
    Phi = spam.deformation.computePhi(transformation)
    image_stack = tifffile.imread(f'res/{name}/{num}.tif')
    result = spam.DIC.deform.applyPhi(image_stack, Phi)
    
    tifffile.imwrite(f'../../../../bigdisk/mrogala/DIC/DATA_DIC_PROCESSED/3D_TIFF_ALIGNED_NEW/{name}/{name}_{num}_load.tif', result.astype(np.uint8))
    # tifffile.imwrite(f'../../../../bigdisk/mrogala/DIC/DATA_DIC_PROCESSED/3D_TIFF_ALIGNED_NEW/G16057_P4_5/G16057_P4_5_1_load_slice700.tif', result[699].astype(np.uint8))
    # tifffile.imwrite(f'../../../../bigdisk/mrogala/DIC/DATA_DIC_PROCESSED/3D_TIFF_ALIGNED_NEW/G16057_P4_5/G16057_P4_5_1_load_slice1000.tif', result[999].astype(np.uint8))
    # tifffile.imwrite(f'../../../../bigdisk/mrogala/DIC/DATA_DIC_PROCESSED/3D_TIFF_ALIGNED_NEW/G16057_P4_5/G16057_P4_5_1_load_slice1300.tif', result[1299].astype(np.uint8))
    print(f"done {num}")

name = 'G16057_P12_5'
transformation_map = {
    1: transformation_G16057_P12_5_1,
    2: transformation_G16057_P12_5_2,
    3: transformation_G16057_P12_5_3,
    4: transformation_G16057_P12_5_4,
}

number_of_files = len(os.listdir(f'res/{name}'))

for i in range(1, number_of_files + 1):
    align_images(transformation_map[i], name, i)

print("Align done!")