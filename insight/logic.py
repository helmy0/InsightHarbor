import os

from openai import OpenAI
from dotenv import *
load_dotenv()
client = OpenAI(api_key=os.getenv("OpenAI_API_Key"))


def getGPTexplanation():
    content = ("You are an image model which describes an image based on keywords given to you. You shall take in the "
               "given keywords and geegrate the prompt"
               )
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
             "content": content},
            {"role": "user", "content": "mountain beach water sky sand trees coastline seascape landscape nature"}
        ]
    )


    return completion.choices[0].message


print(getGPTexplanation())
