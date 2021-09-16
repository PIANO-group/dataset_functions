import os
import SimpleITK as sitk
import glob
from tqdm import tqdm

from config import datasets_path

dataset_name = "FET_20_40_TBR_348_homogen_v1_646432"
os.chdir(os.path.join(datasets_path, dataset_name, "brain_ROIs"))

output_dir = "brain_ROIs"
if not os.path.isdir(os.path.join("..", output_dir)):
    os.makedirs(os.path.join("..", output_dir))

overwrite = True
brain_ROIs_list = glob.glob("*.nii")

binary_filter = sitk.BinaryThresholdImageFilter()
binary_filter.SetLowerThreshold(-1)
binary_filter.SetUpperThreshold(0.3)
binary_filter.SetInsideValue(1)
binary_filter.SetOutsideValue(0)

for filename in tqdm(brain_ROIs_list):
    output_name = filename

    if not overwrite and os.path.isfile(os.path.join(output_dir, output_name)):
        continue

    image = sitk.ReadImage(filename)
    ROI = binary_filter.Execute(image)
    sitk.WriteImage(ROI, os.path.join("..", output_dir, output_name))
