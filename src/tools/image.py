from together import Together
import os
from dotenv import load_dotenv
load_dotenv()

def image_generation(prompt:str):
    client = Together(api_key=os.environ["TOGETHER_API_KEY"])
    response = client.images.generate(
        prompt=prompt,
        model="black-forest-labs/FLUX.1-schnell-Free",
        steps=4,
        n=1
    )
    if response and response.data:
        return response.data[0].url