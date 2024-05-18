import os
import random
from typing import List

import numpy as np
import math
import pypdfium2
from PIL import Image, ImageOps, ImageDraw
import torch
from surya.settings import settings


def get_total_splits(image_size, processor):
    img_height = list(image_size)[1]
    max_height = settings.DETECTOR_IMAGE_CHUNK_HEIGHT
    processor_height = processor.size["height"]
    if img_height > max_height:
        num_splits = math.ceil(img_height / processor_height)
        return num_splits
    return 1


def split_image(img, processor):
    # This will not modify/return the original image - it will either crop, or copy the image
    img_height = list(img.size)[1]
    max_height = settings.DETECTOR_IMAGE_CHUNK_HEIGHT
    processor_height = processor.size["height"]
    if img_height > max_height:
        num_splits = math.ceil(img_height / processor_height)
        splits = []
        split_heights = []
        for i in range(num_splits):
            top = i * processor_height
            bottom = (i + 1) * processor_height
            if bottom > img_height:
                bottom = img_height
            cropped = img.crop((0, top, img.size[0], bottom))
            height = bottom - top
            if height < processor_height:
                cropped = ImageOps.pad(cropped, (img.size[0], processor_height), color=255, centering=(0, 0))
            splits.append(cropped)
            split_heights.append(height)
        return splits, split_heights
    return [img.copy()], [img_height]


def prepare_image(img, processor):
    new_size = (processor.size["width"], processor.size["height"])

    img.thumbnail(new_size, Image.Resampling.LANCZOS) # Shrink largest dimension to fit new size
    img = img.resize(new_size, Image.Resampling.LANCZOS) # Stretch smaller dimension to fit new size

    img = np.asarray(img, dtype=np.uint8)
    img = processor(img)["pixel_values"][0]
    img = torch.from_numpy(img)
    return img


def open_pdf(pdf_filepath):
    return pypdfium2.PdfDocument(pdf_filepath)


def get_page_images(doc, indices: List, dpi=settings.IMAGE_DPI):
    renderer = doc.render(
        pypdfium2.PdfBitmap.to_pil,
        page_indices=indices,
        scale=dpi / 72,
    )
    images = list(renderer)
    images = [image.convert("RGB") for image in images]
    return images


def slice_bboxes_from_image(image: Image.Image, bboxes):
    lines = []
    for bbox in bboxes:
        line = image.crop((bbox[0], bbox[1], bbox[2], bbox[3]))
        lines.append(line)
    return lines


def slice_polys_from_image(image: Image.Image, polys):
    image_array = np.array(image)
    lines = []
    for idx, poly in enumerate(polys):
        lines.append(slice_and_pad_poly(image, image_array, poly, idx))
    return lines


def slice_and_pad_poly(image: Image.Image, image_array: np.array, coordinates, idx):
    # Create a mask for the polygon
    mask = Image.new('L', image.size, 0)

    # Draw polygon onto mask
    coordinates = [(corner[0], corner[1]) for corner in coordinates]
    ImageDraw.Draw(mask).polygon(coordinates, outline=1, fill=1)
    bbox = mask.getbbox()

    if bbox is None:
        return None

    mask = np.array(mask)

    # We mask out anything not in the polygon
    polygon_image = image_array.copy()
    polygon_image[mask == 0] = settings.RECOGNITION_PAD_VALUE

    # Crop out the bbox, and ensure we pad the area outside the polygon with the pad value
    cropped_polygon = polygon_image[bbox[1]:bbox[3], bbox[0]:bbox[2]]
    rectangle = np.full((bbox[3] - bbox[1], bbox[2] - bbox[0], 3), settings.RECOGNITION_PAD_VALUE, dtype=np.uint8)
    rectangle[:, :] = cropped_polygon

    # Paste the polygon into the rectangle
    rectangle_image = Image.fromarray(rectangle)

    return rectangle_image

