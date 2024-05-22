import os
import sys
import cv2
from tqdm import tqdm
import pydicom
from pydicom.pixel_data_handlers.util import apply_voi_lut
import numpy as np
import time


def dicom_to_image(input_dir: str, output_dir: str, brightness: float):
    """
    This function is to convert dicom files to PNG
    :param input_dir: The directory where the dicom files are located
    :param output_dir: The directory where the png files are located
    :param brightness: Adjust the brightness of the image ndarray data
    """

    if not os.path.exists(input_dir):
        os.makedirs(input_dir)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    if not os.listdir(input_dir):
        print(f"No dicom files found in {input_dir}.")
        sys.exit(-1)


    for dicom_file_name in tqdm(os.listdir(input_dir), ascii=True, desc="dicom-to-png conversion"):
        dicom_path = os.path.join(input_dir, dicom_file_name)

        try:
            dicom_path = pydicom.dcmread(dicom_path)
            if "VOILUTSequence" in dicom_path:
                output_png_file = apply_voi_lut(arr=dicom_path.pixel_array, ds=dicom_path)

            else:
                output_png_file = dicom_path.pixel_array.astype(np.float32) * brightness

            cv2.imwrite(os.path.join(output_dir, os.path.splitext(dicom_file_name)[0] + ".png"), output_png_file)

        except pydicom.errors.InvalidDicomError as e:
            e.print(f"{dicom_path} is not a valid dicom file.", sys.stderr)

        time.sleep(0.01)

    print(f"Successfully converted dicom files to PNG format and saved to {output_dir}.")