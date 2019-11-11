from constants import BG_COLOR, NEW_HEIGHT, DEBUG
from helpers import read_mask_image, get_mask, remove_background, crop_to_content, resize_image, random_filename

mask_image = read_mask_image("test/mask.png", DEBUG)
mask = get_mask(mask_image, BG_COLOR, DEBUG)
transparent_image = remove_background("test/test.jpg", mask, DEBUG)
cropped_image = crop_to_content(transparent_image, DEBUG)
resized_image = resize_image(cropped_image, height=NEW_HEIGHT, debug=DEBUG)

resized_image.save(random_filename(".", ".png"))
