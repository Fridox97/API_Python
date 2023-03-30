import os
import requests
import json
from PIL import Image

url = "http://3.216.124.50/detect_person"
path_perro = "C:\\Users\\Jeiso\\Desktop\\LO DEMAS\\perro.jpeg"
path_gato = "C:\\Users\\Jeiso\\Desktop\\LO DEMAS\\gato.jpeg"
pathperson = "People.jpg"


def send_grayscale_image_to_api(image_path, api_url):
    # Convert the image to grayscale
    with Image.open(image_path) as img:
        img = img.convert('L')

        # Save the grayscale image as a temporary file
        tmp_filename = f"{os.path.splitext(image_path)[0]}_grayscale.jpg"
        img.save(tmp_filename)

        # Create the multipart/form-data request
        files = {'image': open(tmp_filename, 'rb')}
        response = requests.post(api_url, files=files)

        # Check if the request was successful
        if response.status_code == requests.codes.ok:
            data = json.loads(response.content)
            print("Response data:", data)
            print("Image sent successfully")
        else:
            print("Error sending image: ", response.text)

        # Delete the temporary file


send_grayscale_image_to_api(path_perro, url)
send_grayscale_image_to_api(path_gato, url)
send_grayscale_image_to_api(pathperson, url)
