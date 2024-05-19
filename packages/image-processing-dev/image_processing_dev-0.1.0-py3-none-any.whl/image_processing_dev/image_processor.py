from PIL import Image

def crop_image(input_image_path, output_image_path, crop_area):
    """
    Crops the image to the specified area and saves it.

    :param input_image_path: str, path to the input image
    :param output_image_path: str, path to save the cropped image
    :param crop_area: tuple, the crop rectangle as a (left, upper, right, lower)-tuple
    """
    image = Image.open(input_image_path)
    cropped_image = image.crop(crop_area)
    cropped_image.save(output_image_path)

def convert_to_black_and_white(input_image_path, output_image_path):
    """
    Converts the image to black and white and saves it.

    :param input_image_path: str, path to the input image
    :param output_image_path: str, path to save the black and white image
    """
    image = Image.open(input_image_path)
    bw_image = image.convert('L')
    bw_image.save(output_image_path)

def apply_sepia_filter(input_image_path, output_image_path):
    """
    Applies a sepia filter to the image and saves it.

    :param input_image_path: str, path to the input image
    :param output_image_path: str, path to save the sepia-filtered image
    """
    image = Image.open(input_image_path)
    sepia_image = image.convert('RGB')

    # Get pixel data
    pixel_data = sepia_image.load()

    # Apply sepia coefficients to each pixel
    for y in range(sepia_image.size[1]):
        for x in range(sepia_image.size[0]):
            r, g, b = pixel_data[x, y]
            sepia_r = int(r * 0.393 + g * 0.769 + b * 0.189)
            sepia_g = int(r * 0.349 + g * 0.686 + b * 0.168)
            sepia_b = int(r * 0.272 + g * 0.534 + b * 0.131)
            # Clamp the values to be between 0 and 255
            pixel_data[x, y] = (
                min(sepia_r, 255),
                min(sepia_g, 255),
                min(sepia_b, 255)
            )

    sepia_image.save(output_image_path)
