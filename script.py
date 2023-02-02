import os
import imghdr
from PIL import Image

# Input folder containing the images
input_folder = '../water color potrait of a person close up'

# Output folder to save the upscaled and cropped images
output_folder = '../water color potrait of a person close up/upscaled'

# Minimum DPI for upscaling
min_dpi = 300

# Number of pixels to crop from left and right edges
crop_px = 10

# Create output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Iterate over all files in the input folder
for filename in os.listdir(input_folder):
    file_path = os.path.join(input_folder, filename)
    # Check if the file is a directory
    if os.path.isdir(file_path):
        print(f"{file_path} is a directory, skipping.")
        continue
    # Check if the file is an image
    if imghdr.what(file_path):
        # Open image
        im = Image.open(file_path)
        # Check if the file ends with .webp
        if filename.endswith('.webp'):
            # Convert to jpeg
            im = im.convert("RGB")
            # Save the image to the same location
            im.save(f'{input_folder}/{os.path.splitext(filename)[0]}.jpg', "JPEG")
            # Delete the original webp image
            os.remove(f'{input_folder}/{filename}')
        try:
            # Get current DPI
            current_dpi = im.info['dpi']
        except KeyError:
            # If the image doesn't have DPI information, set it to a default value
            current_dpi = (72, 72)
        # Upscale the image if its DPI is less than the minimum DPI
        if current_dpi[0] < min_dpi:
            # Calculate the scaling factor
            scale_factor = min_dpi / current_dpi[0]
            # Resize the image
            im = im.resize((round(im.width * scale_factor), round(im.height * scale_factor)))
            # Set the DPI to the minimum DPI
            im.info['dpi'] = (min_dpi, min_dpi)
        # Crop the left and right edges
        im = im.crop((crop_px, crop_px, im.width - crop_px, im.height - crop_px))
        # Save the image to the output folder
        im.save(os.path.join(output_folder, filename), dpi=(300,300), quality=75)
    else:
        print(f"{file_path} is not an image.")