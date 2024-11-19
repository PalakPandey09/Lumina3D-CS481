# from PIL import Image

# # Open the image
# img = Image.open('uidahologo.bmp')

# # Rotate the image by 90 degrees (or any angle you need)
# img_rotated = img.rotate(90, expand=True)  # 'expand=True' ensures the image size is adjusted for rotation

# # Get the dimensions of the rotated image
# rotated_width, rotated_height = img_rotated.size

# # Calculate the new size, maintaining the aspect ratio
# aspect_ratio = rotated_width / rotated_height

# # Fit within 64x32 while maintaining the aspect ratio
# if aspect_ratio > 2:  # Too wide, resize width to 64
#     new_width = 64
#     new_height = int(64 / aspect_ratio)
# else:  # Fit height to 32
#     new_height = 32
#     new_width = int(32 * aspect_ratio)

# # Resize the image to the new size while maintaining aspect ratio
# img_resized = img_rotated.resize((new_width, new_height))

# # Create a new blank image (black background) with the full size of the LED panel (64x32)
# final_image = Image.new("RGB", (64, 32))

# # Paste the resized image onto the blank background, centering it
# x_offset = (64 - new_width) // 2
# y_offset = (32 - new_height) // 2
# final_image.paste(img_resized, (x_offset, y_offset))

# # Save the final image
# final_image.save('uidahologo_resized.bmp')

# print("Image rotated, resized, and centered, saved as uidahologo_resized.bmp")
from PIL import Image

def process_image(input_file, output_file, rotate_angle=90, target_width=64, target_height=32):
    # Open the image
    img = Image.open(input_file)

    # Rotate the image by the specified angle
    img_rotated = img.rotate(rotate_angle, expand=True)  # 'expand=True' ensures the image size is adjusted for rotation

    # Get the dimensions of the rotated image
    rotated_width, rotated_height = img_rotated.size

    # Calculate the new size, maintaining the aspect ratio
    aspect_ratio = rotated_width / rotated_height

    # Fit within target dimensions while maintaining the aspect ratio
    if aspect_ratio > (target_width / target_height):  # Too wide, resize width to target_width
        new_width = target_width
        new_height = int(target_width / aspect_ratio)
    else:  # Fit height to target_height
        new_height = target_height
        new_width = int(target_height * aspect_ratio)

    # Resize the image to the new size while maintaining aspect ratio
    img_resized = img_rotated.resize((new_width, new_height))

    # Create a new blank image (black background) with the full size of the LED panel
    final_image = Image.new("RGB", (target_width, target_height))

    # Paste the resized image onto the blank background, centering it
    x_offset = (target_width - new_width) // 2
    y_offset = (target_height - new_height) // 2
    final_image.paste(img_resized, (x_offset, y_offset))

    # Save the final image
    final_image.save(output_file)

    print(f"Image processed: rotated, resized, and centered, saved as {output_file}")

# Example usage
# process_image('uidahologo.bmp', 'uidahologo_resized.bmp')

process_image('joevandal.bmp', 'joevandal_resized.bmp')
