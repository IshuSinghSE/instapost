import os
import requests
from urllib.parse import urlparse

class Downloader:
    def __init__(self, base_dir):
        self.base_dir = base_dir
        os.makedirs(base_dir, exist_ok=True)

    def download_files(self, urls, dates):
        image_dir = os.path.join(self.base_dir, "images")
        video_dir = os.path.join(self.base_dir, "videos")
        os.makedirs(image_dir, exist_ok=True)
        os.makedirs(video_dir, exist_ok=True)

        image_counter = 1
        video_counter = 1

        for index, url in enumerate(urls):
            try:
                response = requests.get(url, stream=True, timeout=10)
                response.raise_for_status()
                url_path = urlparse(url).path
                file_extension = os.path.splitext(url_path)[1]
                if file_extension.lower() in {'.jpg', '.jpeg', '.png', '.gif'}:
                    file_name = f"{dates[index]}-img-{image_counter}.png"
                    destination_folder = image_dir
                    image_counter += 1
                elif file_extension.lower() in {'.mp4', '.avi', '.mkv', '.mov'}:
                    file_name = f"{dates[index]}-vid-{video_counter}.mp4"
                    destination_folder = video_dir
                    video_counter += 1
                else:
                    file_name = f"{dates[index]}{file_extension}"
                    destination_folder = self.base_dir
                file_path = os.path.join(destination_folder, file_name)
                with open(file_path, 'wb') as file:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            file.write(chunk)
                print(f"Downloaded: {file_path}")
            except requests.RequestException as e:
                print(f"Error downloading {url}: {e}")
