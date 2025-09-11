# (This is in iPython)
import spam.DIC
import spam.deformation
import numpy as np
import tifffile

import spam.scripts
import spam.scripts.deformImage
import spam.scripts.reg

original_data_folder = '../../../../bigdisk/mrogala/DIC/DATA_DIC_PROCESSED'

voxel_size_G16057_K13_5 = 0.01324579  # in mm
voxel_size_G16060_K12_5 = 0.01401936
voxel_size_G16060_P7_5 = 0.01401936
voxel_size_G16057_P4_5 = 0.01325482


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

transformation_G16057_K13_5_1 = {'t': [round(x / voxel_size_G16057_K13_5, 2) for x in [-0.003, -0.042, -0.011]], 'r': [0, 0, 0]}
transformation_G16057_K13_5_2 = {'t': [round(x / voxel_size_G16057_K13_5, 2) for x in [-0.008, -0.084, -0.014]], 'r': [0, 0, 0]}
transformation_G16057_K13_5_3 = {'t': [round(x / voxel_size_G16057_K13_5, 2) for x in [-0.013, -0.124, -0.021]], 'r': [0, 0, 0]}

transformation_G16060_P7_5_1 = {'t': [round(x / voxel_size_G16060_P7_5, 2) for x in [0.010, -0.137, -0.014]], 'r': [0, 0, 0]}
transformation_G16060_P7_5_3 = {'t': [round(x / voxel_size_G16060_P7_5, 2) for x in [0.023, -0.352, -0.030]], 'r': [0, 0, 0]}

transformation_G16057_P4_5_1 = {'t': [round(x / voxel_size_G16057_P4_5, 2) for x in [0.013, -0.038, -0.012]], 'r': [-0.03, -0.01, -0.04]}
transformation_G16057_P4_5_2 = {'t': [round(x / voxel_size_G16057_P4_5, 2) for x in [0.015, -0.078, -0.018]], 'r': [-0.04, -0.02, -0.08]}
transformation_G16057_P4_5_3 = {'t': [round(x / voxel_size_G16057_P4_5, 2) for x in [0.022, -0.120, -0.018]], 'r': [-0.03, -0.02, -0.11]}


transformation_G16060_K12_5_1 = {'t': [round(x / voxel_size_G16060_K12_5, 2) for x in [0.009, -0.137, 0.003]], 'r': [-0.06, -0.02, 0.02]}
transformation_G16060_K12_5_2 = {'t': [round(x / voxel_size_G16060_K12_5, 2) for x in [0.004, -0.252, 0.005]], 'r': [-0.07, -0.04, 0.02]}
transformation_G16060_K12_5_3 = {'t': [round(x / voxel_size_G16060_K12_5, 2) for x in [0.003, -0.361, 0.005]], 'r': [-0.08, -0.06, 0.03]}
transformation_G16060_K12_5_4 = {'t': [round(x / voxel_size_G16060_K12_5, 2) for x in [-0.008, -0.436, -0.006]], 'r': [-0.09, -0.08, 0.04]}


# Phi = spam.deformation.computePhi(transformation_G16057_K13_5_1)
# image_stack = tifffile.imread('res/G16057_K13_5/1.tif')
# result = spam.DIC.deform.applyPhi(image_stack, Phi)
# tifffile.imwrite('../../../../bigdisk/mrogala/DIC/DATA_DIC_PROCESSED/3D_TIFF_ALIGNED_NEW/G16057_K13_5/G16057_K13_5_1_load.tif', result.astype(np.uint8))
# tifffile.imwrite('../../../../bigdisk/mrogala/DIC/DATA_DIC_PROCESSED/3D_TIFF_ALIGNED_NEW/G16057_K13_5/G16057_K13_5_1_load_slice1000.tif', result[999].astype(np.uint8))
# print("done 1")

# Phi = spam.deformation.computePhi(transformation_G16057_K13_5_2)
# image_stack = tifffile.imread('res/G16057_K13_5/2.tif')
# result = spam.DIC.deform.applyPhi(image_stack, Phi)
# tifffile.imwrite('../../../../bigdisk/mrogala/DIC/DATA_DIC_PROCESSED/3D_TIFF_ALIGNED_NEW/G16057_K13_5/G16057_K13_5_2_load.tif', result.astype(np.uint8))
# tifffile.imwrite('../../../../bigdisk/mrogala/DIC/DATA_DIC_PROCESSED/3D_TIFF_ALIGNED_NEW/G16057_K13_5/G16057_K13_5_2_load_slice1000.tif', result[999].astype(np.uint8))
# print("done 2")

# Phi = spam.deformation.computePhi(transformation_G16057_K13_5_3)
# image_stack = tifffile.imread('res/G16057_K13_5/3.tif')
# result = spam.DIC.deform.applyPhi(image_stack, Phi)
# tifffile.imwrite('../../../../bigdisk/mrogala/DIC/DATA_DIC_PROCESSED/3D_TIFF_ALIGNED_NEW/G16057_K13_5/G16057_K13_5_3_load.tif', result.astype(np.uint8))
# tifffile.imwrite('../../../../bigdisk/mrogala/DIC/DATA_DIC_PROCESSED/3D_TIFF_ALIGNED_NEW/G16057_K13_5/G16057_K13_5_3_load_slice1000.tif', result[999].astype(np.uint8))
# print("done 3")


# Phi = spam.deformation.computePhi(transformation_G16060_P7_5_1)
# image_stack = tifffile.imread('res/G16060_P7_5/1.tif')
# result = spam.DIC.deform.applyPhi(image_stack, Phi)
# tifffile.imwrite('../../../../bigdisk/mrogala/DIC/DATA_DIC_PROCESSED/3D_TIFF_ALIGNED_NEW/G16060_P7_5/G16060_P7_5_1_load.tif', result.astype(np.uint8))
# tifffile.imwrite('../../../../bigdisk/mrogala/DIC/DATA_DIC_PROCESSED/3D_TIFF_ALIGNED_NEW/G16060_P7_5/G16060_P7_5_1_load_slice1000.tif', result[999].astype(np.uint8))
# print("done 4")

Phi = spam.deformation.computePhi(transformation_G16060_P7_5_2)
image_stack = tifffile.imread('res/G16060_P7_5/2.tif')
result = spam.DIC.deform.applyPhi(image_stack, Phi)
tifffile.imwrite('../../../../bigdisk/mrogala/DIC/DATA_DIC_PROCESSED/3D_TIFF_ALIGNED_NEW/G16060_P7_5/G16060_P7_5_2_load.tif', result.astype(np.uint8))
tifffile.imwrite('../../../../bigdisk/mrogala/DIC/DATA_DIC_PROCESSED/3D_TIFF_ALIGNED_NEW/G16060_P7_5/G16060_P7_5_2_load_slice1000.tif', result[999].astype(np.uint8))
print("done 5")

# Phi = spam.deformation.computePhi(transformation_G16060_P7_5_3)
# image_stack = tifffile.imread('res/G16060_P7_5/3.tif')
# result = spam.DIC.deform.applyPhi(image_stack, Phi)
# tifffile.imwrite('../../../../bigdisk/mrogala/DIC/DATA_DIC_PROCESSED/3D_TIFF_ALIGNED_NEW/G16060_P7_5/G16060_P7_5_3_load.tif', result.astype(np.uint8))
# tifffile.imwrite('../../../../bigdisk/mrogala/DIC/DATA_DIC_PROCESSED/3D_TIFF_ALIGNED_NEW/G16060_P7_5/G16060_P7_5_3_load_slice1000.tif', result[999].astype(np.uint8))
# print("done 6")

# Phi = spam.deformation.computePhi(transformation_G16057_P4_5_1)
# image_stack = tifffile.imread('res/G16057_P4_5/1.tif')
# result = spam.DIC.deform.applyPhi(image_stack, Phi)
# tifffile.imwrite('../../../../bigdisk/mrogala/DIC/DATA_DIC_PROCESSED/3D_TIFF_ALIGNED_NEW/G16057_P4_5/G16057_P4_5_1_load.tif', result.astype(np.uint8))
# tifffile.imwrite('../../../../bigdisk/mrogala/DIC/DATA_DIC_PROCESSED/3D_TIFF_ALIGNED_NEW/G16057_P4_5/G16057_P4_5_1_load_slice700.tif', result[699].astype(np.uint8))
# tifffile.imwrite('../../../../bigdisk/mrogala/DIC/DATA_DIC_PROCESSED/3D_TIFF_ALIGNED_NEW/G16057_P4_5/G16057_P4_5_1_load_slice1000.tif', result[999].astype(np.uint8))
# tifffile.imwrite('../../../../bigdisk/mrogala/DIC/DATA_DIC_PROCESSED/3D_TIFF_ALIGNED_NEW/G16057_P4_5/G16057_P4_5_1_load_slice1300.tif', result[1299].astype(np.uint8))
# print("done 1")

# Phi = spam.deformation.computePhi(transformation_G16057_P4_5_2)
# image_stack = tifffile.imread('res/G16057_P4_5/2.tif')
# result = spam.DIC.deform.applyPhi(image_stack, Phi)
# tifffile.imwrite('../../../../bigdisk/mrogala/DIC/DATA_DIC_PROCESSED/3D_TIFF_ALIGNED_NEW/G16057_P4_5/G16057_P4_5_2_load.tif', result.astype(np.uint8))
# tifffile.imwrite('../../../../bigdisk/mrogala/DIC/DATA_DIC_PROCESSED/3D_TIFF_ALIGNED_NEW/G16057_P4_5/G16057_P4_5_2_load_slice700.tif', result[699].astype(np.uint8))
# tifffile.imwrite('../../../../bigdisk/mrogala/DIC/DATA_DIC_PROCESSED/3D_TIFF_ALIGNED_NEW/G16057_P4_5/G16057_P4_5_2_load_slice1000.tif', result[999].astype(np.uint8))
# tifffile.imwrite('../../../../bigdisk/mrogala/DIC/DATA_DIC_PROCESSED/3D_TIFF_ALIGNED_NEW/G16057_P4_5/G16057_P4_5_2_load_slice1300.tif', result[1299].astype(np.uint8))
# print("done 2")

# Phi = spam.deformation.computePhi(transformation_G16057_P4_5_3)
# image_stack = tifffile.imread('res/G16057_P4_5/3.tif')
# result = spam.DIC.deform.applyPhi(image_stack, Phi)
# tifffile.imwrite('../../../../bigdisk/mrogala/DIC/DATA_DIC_PROCESSED/3D_TIFF_ALIGNED_NEW/G16057_P4_5/G16057_P4_5_3_load.tif', result.astype(np.uint8))
# tifffile.imwrite('../../../../bigdisk/mrogala/DIC/DATA_DIC_PROCESSED/3D_TIFF_ALIGNED_NEW/G16057_P4_5/G16057_P4_5_3_load_slice700.tif', result[699].astype(np.uint8))
# tifffile.imwrite('../../../../bigdisk/mrogala/DIC/DATA_DIC_PROCESSED/3D_TIFF_ALIGNED_NEW/G16057_P4_5/G16057_P4_5_3_load_slice1000.tif', result[999].astype(np.uint8))
# tifffile.imwrite('../../../../bigdisk/mrogala/DIC/DATA_DIC_PROCESSED/3D_TIFF_ALIGNED_NEW/G16057_P4_5/G16057_P4_5_3_load_slice1300.tif', result[1299].astype(np.uint8))
# print("done 3")

# Phi = spam.deformation.computePhi(transformation_G16060_K12_5_1)
# image_stack = tifffile.imread('res/G16060_K12_5/1.tif')
# result = spam.DIC.deform.applyPhi(image_stack, Phi)
# tifffile.imwrite('../../../../bigdisk/mrogala/DIC/DATA_DIC_PROCESSED/3D_TIFF_ALIGNED_NEW/G16057_P4_5/G16057_P4_5_1_load.tif', result.astype(np.uint8))
# tifffile.imwrite('../../../../bigdisk/mrogala/DIC/DATA_DIC_PROCESSED/3D_TIFF_ALIGNED_NEW/G16057_P4_5/G16057_P4_5_1_load_slice700.tif', result[699].astype(np.uint8))
# tifffile.imwrite('../../../../bigdisk/mrogala/DIC/DATA_DIC_PROCESSED/3D_TIFF_ALIGNED_NEW/G16057_P4_5/G16057_P4_5_1_load_slice1000.tif', result[999].astype(np.uint8))
# tifffile.imwrite('../../../../bigdisk/mrogala/DIC/DATA_DIC_PROCESSED/3D_TIFF_ALIGNED_NEW/G16057_P4_5/G16057_P4_5_1_load_slice1300.tif', result[1299].astype(np.uint8))
# print("done 1")