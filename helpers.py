import os
import random

from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

from constants import TRANSPARENT_COLOR


def read_mask_image(mask_path, debug=False):
    mask_image = np.array(Image.open(mask_path).convert("RGBA"))
    if debug:
        print(f"Mask image shape: {mask_image.shape}")
        plt.imshow(mask_image)
        plt.show()

    return mask_image


def get_mask(mask_image, bg_color, debug=False):
    mask = np.all(mask_image == bg_color, axis=2)
    if debug:
        print(f"Mask shape: {mask.shape}")
        plt.imshow(mask)
        plt.show()

    return mask


def remove_background(image_path, mask, debug=False):
    transparent_image = np.array(Image.open(image_path).convert("RGBA"))
    transparent_image[mask] = TRANSPARENT_COLOR
    if debug:
        print(f"Product image shape: {transparent_image.shape}")
        plt.imshow(transparent_image)
        plt.show()

    transparent_image = Image.fromarray(transparent_image)

    return transparent_image


def crop_to_content(image, debug=False):
    image_box = image.getbbox()
    cropped_image = image.crop(image_box)
    if debug:
        plt.imshow(cropped_image)
        plt.show()

    return cropped_image


def resize_image(image, width=None, height=None, debug=False):
    if width is None and height is None:
        return image

    if width is not None and height is None:
        height = int(width * image.height / image.width)

    if width is None and height is not None:
        width = int(height * image.width / image.height)

    resized_image = image.resize((width, height), resample=Image.LANCZOS)
    if debug:
        plt.imshow(resized_image)
        plt.show()

    return resized_image


def random_filename(dirname, suffixes, prefix=""):
    if not isinstance(suffixes, list):
        suffixes = [suffixes]

    suffixes = [p if p[0] == "." else "." + p for p in suffixes]

    while True:
        bname = "%09d" % random.randint(0, 999999999)
        fnames = []
        for suffix in suffixes:
            fname = os.path.join(dirname, prefix + bname + suffix)
            if not os.path.isfile(fname):
                fnames.append(fname)

        if len(fnames) == len(suffixes):
            break

    if len(fnames) == 1:
        return fnames[0]
    else:
        return fnames
