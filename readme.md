# Cropping images and segmentation masks to 64x64x32 using Confs


## Steps for generation of a cropped dataset (e.g. "FET_20_40_TBR_348_homogen_v1_646432" based on "FET_20_40_TBR_348_homogen_v1")

### General information 
* Prerequisite: Having an uncropped base_dataset (specify in config.py, e.g. "FET_20_40_TBR_348_homogen_v1") containing the images and the following dirs: "tumor_ROIs", "GT_masks" and "brain_ROIs" (see step 2 in deepMedic_nuk repo)

1. Set "base_dataset" in config.py
2. Use create_cropped_dataset.py
3. Use brain_ROI_ones.py (sets every voxel in the brain_ROIs to 1 to force DeepMedic to train on whole 64x64x32 image when use_tumor_ROIs is set to False)

## Steps for cropping segmentation masks obtained from SegmentationValidationApplication

1. Set "base_dataset" in config.py 
1. Copy dir with segmentation masks (e.g. "single_threshold_BG_1.6_heterogen" or "Segmented_BG") into a new dir "threshold-based" in your base_dataset dir
1. Add dirs with segmentation masks in methods list to e.g. "methods = ["single_threshold_BGMax_0.27_heterogen", "Segmented_BG]" in "crop_segmentation_masks.py".
1. Run "crop_segmentation_masks.py"

