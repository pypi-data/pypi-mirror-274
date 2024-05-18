## DICOM2IMAGE

*Introducing dicom2image, a python package for converting DICOM files to standard image formats. With its intuitive interface, batch processing capabilities, and preservation of metadata, the dicom2image package simplifies the conversion process, making it effortless to view and share medical images across various platforms and devices.*

**Project Page:** [https://github.com/cnnlabyzu/dicom2image](https://github.com/cnnlabyzu/dicom2image)

### Installation

To install, use `pip` to install this repo:

    # install from pypi
    pip install dicom2image

    # install repo with pip
    pip install git+https://github.com/cnnlabyzu/dicom2image@main

    # install form local copy
    pip install path/to/local/repo


> ***Note:** It is recommended to use `dicom2image` on **Python 3.8** or above.*

### Usage


If you need to call `dicom2image` directly from Python

```Python
from dicom2image import dicom_to_image

dicom_to_image(path / to / dicom / directory, path / to / image / directory, brightness)
```



If you need an explanation of the options at any time, simply run the `--help` flag:

    dicom2image --help

