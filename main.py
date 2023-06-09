import requests
from PIL import Image
from io import BytesIO
import os

api_key = os.environ.get('OPENAI_API_KEY')

api_url = "https://api.openai.com/v1/images/generations"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

prompt = input("Enter prompt: ")

payload = {
    "prompt": prompt,
    "n": 2,
    "size": "512x512"
}

response = requests.post(api_url, json=payload, headers=headers)

if response.status_code == 200:
    result = response.json()
    images = result["data"]

    directory = r"E:\Pixel Pickle\Generated Images"
    os.makedirs(directory, exist_ok=True)

    count = 1
    for image_data in images:
        image_url = image_data["url"]
        image_response = requests.get(image_url)
        image = Image.open(BytesIO(image_response.content))
        image_filename = f"generated_image_{count}.jpg"
        image_path = os.path.join(directory, image_filename)
        
        while os.path.exists(image_path):
            count += 1
            image_filename = f"generated_image_{count}.jpg"
            image_path = os.path.join(directory, image_filename)
        
        image.save(image_path)
        print(f"Generated image {count} saved as {image_path}")
        count += 1
else:
    print("Error:", response.text)