import os
import nibabel as nib
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm
import time


def nifti_to_image(input_folder: str, output_folder: str):

    """
    This function is used to convert nifti data to png images.
    :param input_folder: The input nifti folder.
    :param output_folder: The output png folder.
    """

    # Ensure output folder exists, create if not
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    if not os.path.exists(input_folder):
        os.makedirs(input_folder)

    if not os.listdir(input_folder):
        print(f"No NIfTI files found in {input_folder}.")
        return

    # Iterate through files in input folder
    for file_name in tqdm(os.listdir(input_folder), ascii=True):
        if file_name.endswith('.nii') or file_name.endswith('.nii.gz'):
            # Load NIfTI file
            nifti_image = nib.load(os.path.join(input_folder, file_name))
            # Extract data
            data = nifti_image.get_fdata()
            # Rotate data 90 degrees clockwise
            data_rotated = np.rot90(data, k=-1)
            # Plot and save slices as PNG
            for i in range(data_rotated.shape[-1]):
                plt.imshow(data_rotated[..., i], cmap='gray')
                plt.axis('off')
                plt.savefig(os.path.join(output_folder, f'{file_name}_slice_{i}.png'), bbox_inches='tight', pad_inches=0)
                plt.close()

        time.sleep(0.1)

    print(f"Successfully converted dicom files to PNG format and saved to {output_folder}.")