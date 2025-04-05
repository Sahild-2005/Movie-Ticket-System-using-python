from PIL import Image, ImageDraw, ImageFont
import os

def create_placeholder_image(text, filename, size=(300, 450), bg_color=(0, 0, 0), text_color=(255, 255, 255)):
    # Create a new image with the given size and background color
    image = Image.new('RGB', size, bg_color)
    draw = ImageDraw.Draw(image)
    
    # Add text
    text = text.upper()
    # Calculate text size and position
    text_bbox = draw.textbbox((0, 0), text)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    # Position text in the center
    x = (size[0] - text_width) // 2
    y = (size[1] - text_height) // 2
    
    # Draw text
    draw.text((x, y), text, fill=text_color)
    
    # Save the image
    image.save(filename)

def main():
    # Create images directory if it doesn't exist
    if not os.path.exists('images'):
        os.makedirs('images')
    
    # Create placeholder image for Premalu
    filename = 'images/premalu.jpg'
    create_placeholder_image('Premalu', filename)
    print(f'Created placeholder image for Premalu')

if __name__ == '__main__':
    main() 