import os

from openai import OpenAI
from dotenv import *
import json
import boto3
from dotenv import load_dotenv

load_dotenv()
openAIclient = OpenAI(api_key=os.getenv("OpenAI_API_Key"))


def getGPTexplanation(keywords):
    content = ("You are an image model which describes an image based on keywords given to you. You shall take in the "
               "given keywords and generate the prompt"
               )
    completion = openAIclient.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
             "content": content},
            {"role": "user", "content": keywords}
        ]
    )
    message = completion.choices[0].message.content
    return message


def detect_labels(photo, bucket):
    session = boto3.Session(profile_name='InsightHarbor',
                            )
    client = session.client('rekognition')

    response = client.detect_labels(Image={'S3Object': {'Bucket': bucket, 'Name': photo}},
                                    MaxLabels=10,
                                    )

    print('Detected labels for ' + photo)
    print()
    for label in response['Labels']:
        print("Label: " + label['Name'])
        print("Confidence: " + str(label['Confidence']))
        print("Instances:")

        for instance in label['Instances']:
            print(" Bounding box")
            print(" Top: " + str(instance['BoundingBox']['Top']))
            print(" Left: " + str(instance['BoundingBox']['Left']))
            print(" Width: " + str(instance['BoundingBox']['Width']))
            print(" Height: " + str(instance['BoundingBox']['Height']))
            print(" Confidence: " + str(instance['Confidence']))
            print()

        print("Parents:")
        for parent in label['Parents']:
            print(" " + parent['Name'])

        print("Aliases:")
        for alias in label['Aliases']:
            print(" " + alias['Name'])

            print("Categories:")
        for category in label['Categories']:
            print(" " + category['Name'])
            print("----------")
            print()

    if "ImageProperties" in str(response):
        print("Background:")
        print(response["ImageProperties"]["Background"])
        print()
        print("Foreground:")
        print(response["ImageProperties"]["Foreground"])
        print()
        print("Quality:")
        print(response["ImageProperties"]["Quality"])
        print()

    return response


def get_label_names(json_string):
    context = ""
    # Parse the JSON string into a Python dictionary
    data = json.loads(json_string)

    # Initialize an empty list to store the label names
    label_names = []

    for label in data['Labels']:
        label_names.append(label['Name'])

    for word in label_names:
        context = context + " " + word
    return context


photo = 'test-image-coastline-mountains.jpg'
bucket = 'insight-harbor'
response = detect_labels(photo, bucket)
json_string = json.dumps(response)
key_words = get_label_names(json_string)
print(key_words)
print(getGPTexplanation(key_words))
