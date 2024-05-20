# nfs.py
import os

class FileSystem:
    def get_file(self, path):
        try:
            with open(path, 'r') as file:
                return file.read()
        except FileNotFoundError:
            return "File not found."

    def download(self, url, destination):
        import requests
        try:
            response = requests.get(url)
            with open(destination, 'wb') as file:
                file.write(response.content)
            return f"Downloaded {url} to {destination}."
        except requests.RequestException as e:
            return f"Error downloading file: {e}"
