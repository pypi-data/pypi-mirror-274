import SimpleITK as sitk
import os
import time
import sys
from glob import glob
from tqdm import tqdm

def writeSlices(series_tag_values, new_img, i, out_dir):
    image_slice = new_img[:,:,i]
    writer = sitk.ImageFileWriter()
    writer.KeepOriginalImageUIDOn()

    # Tags shared by the series.
    list(map(lambda tag_value: image_slice.SetMetaData(tag_value[0], tag_value[1]), series_tag_values))

    # Slice specific tags.
    image_slice.SetMetaData("0008|0012", time.strftime("%Y%m%d")) # Instance Creation Date
    image_slice.SetMetaData("0008|0013", time.strftime("%H%M%S")) # Instance Creation Time

    # Setting the type to MRI preserves the slice location.
    image_slice.SetMetaData("0008|0060", "MRI")  # set the type to MRI so the thickness is carried over

    # (0020, 0032) image position patient determines the 3D spacing between slices.
    image_slice.SetMetaData("0020|0032", '\\'.join(map(str,new_img.TransformIndexToPhysicalPoint((0,0,i))))) # Image Position (Patient)
    image_slice.SetMetaData("0020|0013", str(i)) # Instance Number

    # Write to the output directory and add the extension dcm, to force writing in DICOM format.
    writer.SetFileName(os.path.join(out_dir,'slice' + str(i).zfill(4) + '.dcm'))
    writer.Execute(image_slice)

def nifti_to_dicom(in_dir, out_dir):
    """
    This function is to convert only one nifti file into dicom series

    `in_dir`: the path to the one nifti file
    `out_dir`: the path to output
    """

    if not os.path.exists(in_dir):
        print(f"NIfTI file '{in_dir}' does not exist.")
        sys.exit(-1)

    os.makedirs(out_dir, exist_ok=True)

    new_img = sitk.ReadImage(in_dir)
    modification_time = time.strftime("%H%M%S")
    modification_date = time.strftime("%Y%m%d")

    direction = new_img.GetDirection()
    series_tag_values = [("0008|0031",modification_time), # Series Time
                    ("0008|0021",modification_date), # Series Date
                    ("0008|0008","DERIVED\\SECONDARY"), # Image Type
                    ("0020|000e", "1.2.826.0.1.3680043.2.1125."+modification_date+".1"+modification_time), # Series Instance UID
                    ("0020|000d", "1.2.826.0.1.3680043.2.1125.1"+modification_date+modification_time), # Study Instance UID
                    ("0020|0037", '\\'.join(map(str, (direction[0], direction[3], direction[6],# Image Orientation (Patient)
                                                        direction[1],direction[4],direction[7])))),
                    ("0008|103e", "Created-Pycad")] # Series Description

    # Write slices to output directory
    for i in tqdm(range(new_img.GetDepth()), desc='Converting slices', unit='slice'):
        writeSlices(series_tag_values, new_img, i, out_dir)

    print(f"Successfully converted {in_dir} to {out_dir}")

def nifti2dicom_mfiles(nifti_dir, out_dir=''):
    """
    This function is to convert multiple nifti files into dicom files

    `nifti_dir`: You enter the global path to all the nifti files here.
    `out_dir`: Put the path to where you want to save all the dicom files here.

    PS: Each nifti file's folders will be created automatically, so you do not need to create an empty folder for each patient.
    """

    if not os.path.exists(nifti_dir):
        print(f"NIfTI directory '{nifti_dir}' does not exist.")
        sys.exit(-1)

    images = glob(nifti_dir + '/*.nii.gz')

    for image in images:
        o_path = out_dir + '/' + os.path.basename(image)[:-7]
        os.makedirs(o_path, exist_ok=True)

        nifti_to_dicom(image, o_path)