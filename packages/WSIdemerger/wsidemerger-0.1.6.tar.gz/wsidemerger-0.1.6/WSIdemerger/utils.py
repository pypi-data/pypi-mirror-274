# WSIdemerger/utils.py
import numpy as np
from skimage.color import rgb2hsv
from skimage import img_as_ubyte
import os
import shutil
import logging

def calculate_saturation(patch):
    patch_array = np.array(patch)
    hsv_patch = rgb2hsv(patch_array)
    saturation_channel = hsv_patch[:, :, 1]
    saturation_channel_0_255 = img_as_ubyte(saturation_channel)
    return np.mean(saturation_channel_0_255)

def clear_output_directory(output_path):
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    else:
        for filename in os.listdir(output_path):
            file_path = os.path.join(output_path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                logging.error(f'Failed to delete {file_path}. Reason: {str(e)}')

def select_level_by_magnification(slide, target_magnification):
    best_level = 0
    min_diff = float('inf')
    for i, downsample in enumerate(slide.level_downsamples):
        try:
            objective_power = float(slide.properties['openslide.objective-power'])
            current_magnification = objective_power / downsample
            magnification_diff = abs(current_magnification - target_magnification)

            if magnification_diff < min_diff:
                min_diff = magnification_diff
                best_level = i
        except KeyError:
            continue
        except ValueError:
            continue

    return best_level

