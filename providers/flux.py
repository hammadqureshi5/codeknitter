import os
import requests
from dotenv import load_dotenv

load_dotenv()

class FluxProvider:
    def __init__(self):
        self.endpoint = os.getenv("FLUX_ENDPOINT", "http://35.224.54.129:5000/generate-multi")

    async def generate(self, model: str, prompt: str, images: list = None, **kwargs):
        data = {
            "prompt": prompt
        }
        
        files = []
        if images:
            if isinstance(images, str):
                images = [images]
            
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
            for i, img_item in enumerate(images):
                if isinstance(img_item, str) and (img_item.startswith("http://") or img_item.startswith("https://")):
                    img_resp = requests.get(img_item, headers=headers, timeout=10)
                    if img_resp.status_code == 200:
                        content_type = img_resp.headers.get("Content-Type", "image/jpeg").split(";")[0]
                        files.append(("images", (f"image_{i}.jpg", img_resp.content, content_type)))
                elif isinstance(img_item, tuple):
                    files.append(("images", img_item))

        if files:
            response = requests.post(self.endpoint, data=data, files=files)
        else:
            # If no files fetched/provided, try multipart data or json
            response = requests.post(self.endpoint, data=data)

        if response.status_code != 200:
            raise Exception(f"Flux API Error ({response.status_code}): {response.text}")
        
        res_data = response.json()
        return {
            "text": str(res_data),
            "raw": res_data,
            "provider": "flux",
            "model": model
        }

    async def check_status(self, job_id: str):
        status_url = f"http://35.224.54.129:5000/status/{job_id}"
        response = requests.get(status_url)
        if response.status_code != 200:
            raise Exception(f"Flux Status Error ({response.status_code}): {response.text}")
        return response.json()
