import os
import SimpleITK as sitk
from tqdm import tqdm
import time
import sys


def image_to_nifti(input_image_dir: str, output_nii_dir: str, output_nii_filename: str):
    """
    This function is used to convert ndarray images to a nifti data.
    :param input_image_dir: The input image directory.
    :param output_nii_dir: The output nifti directory.
    :param output_nii_filename: The output nifti filename.
    :return: None
    """

    if not os.listdir(input_image_dir):
        print(f"No files in the image folder.")
        sys.exit(-1)

    # get lists of image files
    image_files = []
    for files in tqdm(os.listdir(input_image_dir), ascii=True, desc="Get-Files-from-Directory"):
        if files.endswith('.jpeg') or files.endswith('.jpg') or files.endswith('.png'):
            image_files.append(os.path.join(input_image_dir, files))
        else:
            print(f"Invalid image file {files}, please check the file format.\n"
                  f"The format of the input image file must be JPG or PNG.\n")
        time.sleep(0.1)

    # sort the list of images files
    image_files.sort()

    # create an empty list to store the images
    image_list = []

    # Read each ndarray of images and append them to the list
    for files in tqdm(image_files, ascii=True, desc="read-images"):
        image = sitk.ReadImage(files)
        image_list.append(image)

    if image_list:
        # Create a 3D image volume from the list of images
        image_volume = sitk.JoinSeries(image_list)

        # Write the 3D image volume to a single NIFTI file
        sitk.WriteImage(image_volume, os.path.join(output_nii_dir, output_nii_filename))
    else:
        print("No valid image files found in the directory.")

        time.sleep(0.5)