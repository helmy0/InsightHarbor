import os
import json
import boto3
from openai import OpenAI
from dotenv import load_dotenv

class OpenAIClient:
    def __init__(self, api_key):

        self.client = OpenAI(api_key=api_key)

    def get_gpt_explanation(self, keywords):
        content = ("You are an image model which describes an image based on keywords given to you. You shall take in the "
                   "given keywords and generate the prompt"
                   )
        completion = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system",
                 "content": content},
                {"role": "user", "content": keywords}
            ]
        )
        message = completion.choices[0].message.content
        return message

class ImageAnalyzer:
    def __init__(self, bucket, profile_name='InsightHarbor'):
        self.session = boto3.Session(profile_name=profile_name)
        self.client = self.session.client('rekognition')
        self.bucket = bucket

    def detect_labels(self, photo):
        response = self.client.detect_labels(Image={'S3Object': {'Bucket': self.bucket, 'Name': photo}},
                                             MaxLabels=10,
                                             )
        return response

    @staticmethod
    def get_label_names(json_string):
        context = ""
        data = json.loads(json_string)
        label_names = []
        for label in data['Labels']:
            label_names.append(label['Name'])
        for word in label_names:
            context = context + " " + word
        return context

load_dotenv()
openai_client = OpenAIClient(api_key=os.getenv("OpenAI_API_Key"))
image_analyzer = ImageAnalyzer(bucket='insight-harbor')

photo = 'test-image-coastline-mountains.jpg'
response = image_analyzer.detect_labels(photo)
json_string = json.dumps(response)
key_words = ImageAnalyzer.get_label_names(json_string)
print(key_words)
print(openai_client.get_gpt_explanation(key_words))