import os
import numpy as np
import pydicom
import nibabel as nib
import time
from tqdm import tqdm
import sys


def dicom_to_nifti(dicom_folder: str, nifti_file: str, nifti_folder: str):

    """
    This function is used to convert DICOM files to NIfTI files.
    :param dicom_folder: The input DICOM directory.
    :param nifti_file: The output NIfTI filename.
    :param nifti_folder: The output NIfTI directory.
    """

    if not os.path.exists(dicom_folder):
        os.makedirs(dicom_folder)

    if not os.path.exists(nifti_folder):
        os.makedirs(nifti_folder)

    if not os.listdir(dicom_folder):
        print('No DICOM files found in the input directory.')
        sys.exit(-1)

    # Load DICOM files
    dicom_files = [pydicom.dcmread(os.path.join(dicom_folder, f)) for f in os.listdir(dicom_folder) if
                   f.endswith('.dcm')]

    # Sort DICOM files based on their ImagePositionPatient attribute
    dicom_files.sort(key=lambda x: float(x.ImagePositionPatient[2]))

    # Initialize progress bar
    progress_bar = tqdm(total=len(dicom_files), desc='Converting DICOM to NIfTI', unit='slice')

    # Extract DICOM pixel data
    dicom_slices = []
    for d in dicom_files:
        dicom_slices.append(d.pixel_array)
        time.sleep(0.1)
        progress_bar.update(1)  # Update progress bar

    dicom_slices = np.array(dicom_slices)

    # Create NIfTI image
    nifti_image = nib.Nifti1Image(dicom_slices, np.eye(4))  # Use identity affine matrix as placeholder

    # Save NIfTI file
    nib.save(nifti_image, os.path.join(nifti_folder, nifti_file))

    # Close progress bar
    progress_bar.close()