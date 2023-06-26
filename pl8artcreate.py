import os
import pandas as pd
from PIL import Image, ImageDraw, ImageFont

csv_file = 'artists.csv'
background_image = 'background.png'  # Replace with the path to your desired background image
font_type = 'Roboto-Bold.ttf'  # Replace with the path to your desired font file
font_size = 120
font_color = (255, 255, 255)  # RGB color for the font (white in this example)
border_color = (0, 0, 0)  # RGB color for the border (black in this example)
border_width = 2

df = pd.read_csv(csv_file)
artists = df['Artist'].tolist()

# Create the "images" directory if it doesn't exist
os.makedirs('images', exist_ok=True)

for artist in artists:
    image = Image.open(background_image)
    text_layer = Image.new('RGBA', image.size, (0, 0, 0, 0))
    font = ImageFont.truetype(font_type, font_size)
    draw = ImageDraw.Draw(text_layer)

    text_width, text_height = draw.textsize(artist, font=font)

    # Calculate the position for the text
    x = (image.width - text_width) // 2
    y = (image.height - text_height) // 2

    # Draw the border
    for dx in range(-border_width, border_width + 1):
        for dy in range(-border_width, border_width + 1):
            draw.text((x + dx, y + dy), artist, font=font, fill=border_color)

    # Draw the text
    draw.text((x, y), artist, font=font, fill=font_color)

    result = Image.alpha_composite(image.convert('RGBA'), text_layer)
    # Save the image in the "images" directory with the artist's name as the filename
    image_path = os.path.join('images', f'{artist}.png')
    result.save(image_path)

png_folder = 'images'

# Path to the folder where the converted JPG images will be saved
jpg_folder = 'jpgs'

# Create the output JPG folder if it doesn't exist
os.makedirs(jpg_folder, exist_ok=True)

# Iterate over PNG files in the folder
for filename in os.listdir(png_folder):
    if filename.endswith('.png'):
        # Open the PNG image
        png_path = os.path.join(png_folder, filename)
        image = Image.open(png_path)
        
        # Convert PNG image to JPG format
        jpg_filename = os.path.splitext(filename)[0] + '.jpg'
        jpg_path = os.path.join(jpg_folder, jpg_filename)
        image.convert('RGB').save(jpg_path, 'JPEG')
        
        # Close the image
        image.close()

        # Optional: Remove the original PNG file
        # os.remove(png_path)