import os
import SimpleITK as sitk
import numpy as np
import glob
import cv2
import imageio as iio

from skimage import filters
from skimage.color import rgb2gray  # only needed for incorrectly saved images
from skimage.measure import regionprops
from config import base_dataset_path
from tqdm import tqdm


methods = ["Segmented_BG", "Segmented_BGMax", "Segmented_Max"]
methods = ["single_threshold_BGMax_0.27_heterogen"]


for method in methods:

    images_path = os.path.join(base_dataset_path, "threshold-based", method)
    new_dataset_dir = os.path.join("cropped")


    new_dataset_path = os.path.join(images_path, new_dataset_dir)
    if not os.path.isdir(new_dataset_path):
        os.makedirs(new_dataset_path)

    os.chdir(base_dataset_path)
    print(f"Current working path: {os.getcwd()}")
    print(f"Saving new dataset to: {new_dataset_path}")

    images_list = glob.glob(os.path.join(images_path, "*.nii"))
    tumor_ROIs_list = glob.glob(os.path.join("tumor_ROIs", "*.nii"))
    # brain_ROIs_list = glob.glob(os.path.join("brain_ROIs", "*.nii"))
    # GT_masks_list = glob.glob(os.path.join("GT_masks", "*.nii"))
    # print(images_list[0])

    tumor_ROIs_names = [path.split(os.path.sep)[-1] for path in tumor_ROIs_list]
    # brain_ROIs_names = [path.split(os.path.sep)[-1] for path in brain_ROIs_list]
    # GT_masks_names = [path.split(os.path.sep)[-1] for path in GT_masks_list]
    print(tumor_ROIs_names[0])
    # print(brain_ROIs_names[0])
    # print(GT_masks_names[0])
    print(tumor_ROIs_names)
    print(images_list)

    mask_filter = sitk.MaskImageFilter()
    pad_filter = sitk.ConstantPadImageFilter()
    pad_filter.SetConstant(0)
    pad_filter.SetPadLowerBound([32,32,32])
    pad_filter.SetPadUpperBound([32,32,32])

    for i in tqdm(range(len(images_list))):
        img = sitk.ReadImage(images_list[i])
        tumor_ROI = sitk.ReadImage(tumor_ROIs_list[i])
        brain_nr = images_list[i].split("_")[3]
        img_name = os.path.basename(images_list[i])
        # brain_ROI_filename = "brain_ROI_" + brain_nr + ".nii"
        # if os.path.isfile(os.path.join("brain_ROIs", brain_ROI_filename)):
        #     brain_ROI = sitk.ReadImage(os.path.join("brain_ROIs", brain_ROI_filename))
        # GT_mask = sitk.ReadImage(GT_masks_list[i])
        #
        padded_img = pad_filter.Execute(img)
        padded_tumor_ROI = pad_filter.Execute(tumor_ROI)
        # if os.path.isfile(os.path.join("brain_ROIs", brain_ROI_filename)):
        #     padded_brain_ROI = pad_filter.Execute(brain_ROI)
        # padded_GT_mask = pad_filter.Execute(GT_mask)

        # tumor_ROI_np = sitk.GetArrayFromImage(tumor_ROI)
        padded_tumor_ROI_np = sitk.GetArrayFromImage(padded_tumor_ROI)
        # threshold_value = filters.threshold_otsu(tumor_ROI_np)
        threshold_value_padded = filters.threshold_otsu(padded_tumor_ROI_np)
        # print(threshold_value)
        print(threshold_value_padded)
        # labeled_foreground = (tumor_ROI_np > threshold_value).astype(int)
        labeled_foreground_padded = (padded_tumor_ROI_np > threshold_value_padded).astype(int)
        # properties = regionprops(labeled_foreground, tumor_ROI_np)
        properties_padded = regionprops(labeled_foreground_padded, padded_tumor_ROI_np)
        # center_of_mass = properties[0].centroid
        # center_of_mass = [int(i) for i in center_of_mass]
        center_of_mass_padded = properties_padded[0].centroid
        center_of_mass_padded = [int(i) for i in center_of_mass_padded]
        # weighted_center_of_mass = properties[0].weighted_centroid
        weighted_center_of_mass_padded = properties_padded[0].weighted_centroid
        # print(center_of_mass)
        print(center_of_mass_padded)

        x_new = 64
        y_new = 64
        z_new = 32

        # cms_x = center_of_mass[2]
        # cms_y = center_of_mass[1]
        # cms_z = center_of_mass[0]
        # x0 = int(cms_x - x_new/2)
        # x1 = int(cms_x + x_new/2)
        # y0 = int(cms_y - y_new/2)
        # y1 = int(cms_y + y_new/2)
        # z0 = int(cms_z - z_new/2)
        # z1 = int(cms_z + z_new/2)
        # cropped_img = img[x0:x1, y0:y1, z0:z1]
        # sitk.Show(cropped_img)

        cms_x_padded = center_of_mass_padded[2]
        cms_y_padded = center_of_mass_padded[1]
        cms_z_padded = center_of_mass_padded[0]

        x0_padded = int(cms_x_padded - x_new/2)
        x1_padded = int(cms_x_padded + x_new/2)
        y0_padded = int(cms_y_padded - y_new/2)
        y1_padded = int(cms_y_padded + y_new/2)
        z0_padded = int(cms_z_padded - z_new/2)
        z1_padded = int(cms_z_padded + z_new/2)

        cropped_padded_img = padded_img[x0_padded:x1_padded, y0_padded:y1_padded, z0_padded:z1_padded]
        # cropped_padded_tumor_ROI = padded_tumor_ROI[x0_padded:x1_padded, y0_padded:y1_padded, z0_padded:z1_padded]
        # if os.path.isfile(os.path.join("brain_ROIs", brain_ROI_filename)):
        #     cropped_padded_brain_ROI = padded_brain_ROI[x0_padded:x1_padded, y0_padded:y1_padded, z0_padded:z1_padded]
        # cropped_padded_GT_mask = padded_GT_mask[x0_padded:x1_padded, y0_padded:y1_padded, z0_padded:z1_padded]

        # sitk.Show(cropped_padded_img)
        # sitk.Show(cropped_padded_tumor_ROI)
        # sitk.Show(cropped_padded_GT_mask)


        sitk.WriteImage(cropped_padded_img, os.path.join(new_dataset_path, img_name))
        # sitk.WriteImage(cropped_padded_tumor_ROI, os.path.join(new_tumor_ROIs_path, tumor_ROIs_names[i]))
        # if os.path.isfile(os.path.join("brain_ROIs", brain_ROI_filename)):
        #     sitk.WriteImage(cropped_padded_brain_ROI, os.path.join(new_brain_ROIs_path, brain_ROI_filename))
        # sitk.WriteImage(cropped_padded_GT_mask, os.path.join(new_GT_masks_path, GT_masks_names[i]))






