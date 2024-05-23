
import os
import cv2
import staintools
from pathlib import Path
from tqdm import tqdm

def normalize_images(input_folder, reference_image_path, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    reference_image = staintools.read_image(reference_image_path)
    reference_image = staintools.LuminosityStandardizer.standardize(reference_image)

    normalizer = staintools.StainNormalizer(method='vahadane')
    normalizer.fit(reference_image)

    image_files = [p for p in Path(input_folder).rglob('*.png')]

    for image_path in tqdm(image_files, desc="Processing Images"):
        image = staintools.read_image(str(image_path))
        image = staintools.LuminosityStandardizer.standardize(image)
        normalized_image = normalizer.transform(image)

        relative_path = image_path.relative_to(input_folder)
        save_path = Path(output_folder) / relative_path

        save_path.parent.mkdir(parents=True, exist_ok=True)

        cv2.imwrite(str(save_path), cv2.cvtColor(normalized_image, cv2.COLOR_RGB2BGR))
