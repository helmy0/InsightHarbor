import os

from openai import OpenAI
from dotenv import *
import boto3

load_dotenv()
openAIclient = OpenAI(api_key=os.getenv("OpenAI_API_Key"))


def getGPTexplanation():
    content = ("You are an image model which describes an image based on keywords given to you. You shall take in the "
               "given keywords and geegrate the prompt"
               )
    completion = openAIclient.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
             "content": content},
            {"role": "user", "content": "mountain beach water sky sand trees coastline seascape landscape nature"}
        ]
    )

    return completion.choices[0].message


def detect_labels(photo, bucket):
    session = boto3.Session(profile_name='InsightHarbor',
                            )
    client = session.client('rekognition')

    response = client.detect_labels(Image={'S3Object': {'Bucket': bucket, 'Name': photo}},
                                    MaxLabels=10,
                                    # Uncomment to use image properties and filtration settings
                                    # Features=["GENERAL_LABELS", "IMAGE_PROPERTIES"],
                                    # Settings={"GeneralLabels": {"LabelInclusionFilters":["Cat"]},
                                    # "ImageProperties": {"MaxDominantColors":10}}
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

    return len(response['Labels'])



photo = 'test-image-coastline-mountains.jpg'
bucket = 'insight-harbor'
label_count = detect_labels(photo, bucket)
print("Labels detected: " + str(label_count))


