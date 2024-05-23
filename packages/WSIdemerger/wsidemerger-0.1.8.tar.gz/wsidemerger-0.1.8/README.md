
# WSIdemerger

WSIdemerger is a Python package for extracting image patches from SVS files and performing color normalization.

## Installation

You can install the package using pip:

```sh
pip install WSIdemerger
```

## Usage

### Extract Patches from SVS

```python
from WSIdemerger.Patches_generation import extract_patches_from_svs

input_path = 'path_to_your_svs_file'
output_path = 'path_to_output_directory'
excel_path = 'path_to_output_excel_file'
patch_size = 512
target_magnification = 20
saturation_threshold = 50

extract_patches_from_svs(input_path, output_path, excel_path, patch_size, target_magnification, saturation_threshold)
```

### Normalize Images

```python
from WSIdemerger.Colour_standardisation import normalize_images

input_folder = 'path_to_input_images'
reference_image_path = 'path_to_reference_image'
output_folder = 'path_to_output_directory'

normalize_images(input_folder, reference_image_path, output_folder)
```
