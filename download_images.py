import os
import requests
from PIL import Image
from io import BytesIO

# Create images directory if it doesn't exist
if not os.path.exists('images'):
    os.makedirs('images')

# Headers for Wikipedia image requests
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Movie poster URLs for Hindi movies
movie_posters = {
    'jawan.jpg': 'https://images.pexels.com/photos/7991579/pexels-photo-7991579.jpeg',
    'animal.jpg': 'https://images.pexels.com/photos/7991579/pexels-photo-7991579.jpeg',
    'dunki.jpg': 'https://images.pexels.com/photos/7991579/pexels-photo-7991579.jpeg',
    '12th_fail.jpg': 'https://images.pexels.com/photos/7991579/pexels-photo-7991579.jpeg',
    'sam_bahadur.jpg': 'https://images.pexels.com/photos/7991579/pexels-photo-7991579.jpeg',
    'chaava.jpg': 'https://images.pexels.com/photos/7991579/pexels-photo-7991579.jpeg',
    'sita_ramam.jpg': 'https://images.pexels.com/photos/7991579/pexels-photo-7991579.jpeg',
    'geeta_govindam.jpg': 'https://images.pexels.com/photos/7991579/pexels-photo-7991579.jpeg',
    'kanni.jpg': 'https://images.pexels.com/photos/7991579/pexels-photo-7991579.jpeg',
    'kaakan.jpg': 'https://images.pexels.com/photos/7991579/pexels-photo-7991579.jpeg'
}

def download_and_save_image(url, filename):
    try:
        # Download image with headers
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        # Open and resize image
        img = Image.open(BytesIO(response.content))
        img = img.resize((300, 450), Image.Resampling.LANCZOS)
        
        # Save image
        img.save(os.path.join('images', filename))
        print(f"Successfully downloaded and saved {filename}")
        
    except Exception as e:
        print(f"Error downloading {filename}: {e}")

# Download all movie posters
for filename, url in movie_posters.items():
    download_and_save_image(url, filename)

print("\nAll movie posters have been downloaded to the 'images' directory.") 