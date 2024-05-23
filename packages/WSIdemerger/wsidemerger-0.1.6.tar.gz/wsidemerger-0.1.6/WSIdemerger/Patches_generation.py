# WSIdemerger/Patches_generation.py
import os
import pandas as pd
import openslide
from PIL import Image
import numpy as np
from skimage.color import rgb2hsv
from skimage import img_as_ubyte
import shutil
import logging
import time
from .utils import calculate_saturation, clear_output_directory, select_level_by_magnification

def extract_patches_from_svs(input_path, output_path, excel_path, patch_size=512, target_magnification=20, saturation_threshold=50):
    slide = openslide.OpenSlide(input_path)
    level = select_level_by_magnification(slide, target_magnification)
    level_downsample = slide.level_downsamples[level]
    width, height = slide.level_dimensions[level]

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    data = []
    num_patches = 0

    for x in range(0, width - patch_size + 1, patch_size):
        for y in range(0, height - patch_size + 1, patch_size):
            patch = slide.read_region((int(x * level_downsample), int(y * level_downsample)), level,
                                      (patch_size, patch_size)).convert('RGB')
            saturation = calculate_saturation(patch)
            patch_name = f'patch_{x}_{y}.png'
            is_saved = saturation >= saturation_threshold

            if is_saved:
                patch.save(os.path.join(output_path, patch_name))
                num_patches += 1

            data.append([patch_name, saturation, is_saved])

    df = pd.DataFrame(data, columns=['Patch Name', 'Saturation', 'Saved'])
    df.to_excel(excel_path, index=False)

    slide.close()

def process_svs_files(base_path, output_base, saturation_threshold, patch_size, target_magnification):
    logging.basicConfig(filename=os.path.join(output_base, 'error_log.txt'), level=logging.ERROR)
    svs_files = [os.path.join(dp, f) for dp, dn, filenames in os.walk(base_path) for f in filenames if f.endswith('.svs')]
    total_files = len(svs_files)
    start_time = time.time()

    for index, svs_file in enumerate(svs_files):
        current_file_start_time = time.time()
        folder_name = os.path.basename(os.path.dirname(svs_file))
        output_path = os.path.join(output_base, folder_name)
        excel_path = os.path.join(output_path, f'{folder_name}_patches_info.xlsx')
        clear_output_directory(output_path)
        try:
            extract_patches_from_svs(svs_file, output_path, excel_path, patch_size, target_magnification, saturation_threshold)
        except Exception as e:
            logging.error(f'处理文件 {svs_file} 时出现错误: {str(e)}')

        print(f'已处理 {index + 1}/{total_files} 文件，占总进度的 {(index + 1) / total_files * 100:.2f}%')

    total_elapsed_time = time.time() - start_time
    print(f'所有文件已处理完成，总耗时 {total_elapsed_time / 60:.2f} 分钟。')
