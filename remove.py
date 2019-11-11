from pathlib import Path
import re

from constants import DEBUG, BG_COLOR, NEW_HEIGHT, PRODUCTS_DIRECTORY, ABOVE, BELOW, STRAIGHT, \
    ABOVE_MASK_FILE, BELOW_MASK_FILE, STRAIGHT_MASK_FILE

from helpers import read_mask_image, get_mask, remove_background, crop_to_content, resize_image, random_filename

above_pattern = re.compile("^.*?above.*$", re.IGNORECASE)
below_pattern = re.compile("^.*?below.*$", re.IGNORECASE)


def _process_image(angle, file_path, mask_file, debug=False):
    image_path = file_path.resolve()
    product_dir = image_path.parent

    if angle == ABOVE:
        output_dir = product_dir / ABOVE
    elif angle == BELOW:
        output_dir = product_dir / BELOW
    elif angle == STRAIGHT:
        output_dir = product_dir / STRAIGHT
    else:
        return
    output_dir.mkdir(exist_ok=True)

    mask_image = read_mask_image(str(product_dir / mask_file), debug)
    mask = get_mask(mask_image, BG_COLOR, debug)

    transparent_image = remove_background(str(image_path), mask, debug)
    cropped_image = crop_to_content(transparent_image, debug)
    resized_image = resize_image(cropped_image, height=NEW_HEIGHT, debug=debug)

    resized_image.save(random_filename(str(output_dir), ".png"))


for file in (Path.cwd() / PRODUCTS_DIRECTORY).rglob("*.jpg"):
    if above_pattern.fullmatch(str(file)):
        _process_image(ABOVE, file, ABOVE_MASK_FILE, debug=DEBUG)
    elif below_pattern.fullmatch(str(file)):
        _process_image(BELOW, file, BELOW_MASK_FILE, debug=DEBUG)
    else:
        _process_image(STRAIGHT, file, STRAIGHT_MASK_FILE, debug=DEBUG)
