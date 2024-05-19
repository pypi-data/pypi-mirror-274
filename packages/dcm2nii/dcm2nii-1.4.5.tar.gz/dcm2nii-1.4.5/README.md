## DCM2NII

*Introducing dcm2nii, a Python package designed for converting DICOM files to NIfTI format. With its user-friendly interface, efficient batch processing functionality, and metadata retention, dcm2nii streamlines the conversion process, enabling seamless viewing and sharing of medical images across different platforms and devices.*


**Project Page:** [https://github.com/cnnlabyzu/dicom2nifti](https://github.com/cnnlabyzu/dicom2nifti)

### Installation

To install, use `pip` to install this repo:

    # install from pypi
    pip install dcm2nii

    # install repo with pip
    pip install git+https://github.com/cnnlabyzu/dicom2nifti@main

    # install form local copy
    pip install path/to/local/repo


> ***Note:** It is recommended to use `dcm2nii` on **Python 3.8** or above.*

### Usage


If you need to call `dcm2nii` directly from Python

```Python
from dicom2nifti import dicom_to_nifti

dicom_to_nifti(path/to/dicom/directory, nifti_file, path/to/nifti/directory)
```


- `path/to/dicom/directory` please provide the directory path for the DICOM files. (**type:** *str*)
- `nifti_file` please provide the filename of the NifTI. (**type:** *str*)
- `path/to/nifti/directory` please provide the directory path for the NifTI file. (**type:** *str*)

> **Note:** the extension of NifTI file must end with `.nii` or `.nii.gz`.