import json

from django.shortcuts import render, redirect
from .logic import AWSImageAnalyzer, OpenAIClient, analyze_image_and_generate_description
from .forms import InsightRequest

import os
import boto3
from botocore.exceptions import NoCredentialsError
from dotenv import load_dotenv

load_dotenv() # Load environment variables from .env file

from django.core.files.storage import FileSystemStorage

def home(request):
    context = {}
    if request.method == 'POST':
        useS3 = True
        print("Successeded")

        image = request.FILES['image']
        filename = image.name

        if useS3 is False:
            fs = FileSystemStorage(location='static/imgs/')
            filename = fs.save(image.name, image)
        else:
            # Init AWS S3 boto client
            try:
                print("Uploading to S3")
                bucket = 'insight-harbor'
                s3_client = boto3.client('s3')

                # Upload image to S3
                s3_client.upload_fileobj(image, bucket, image.name)
            except Exception as e:
                print(f"Failure to upload image to S3"
                      f" \n Exception{e}")

        context = {
            'filename': filename,
        }
        print(filename)
        return redirect('result',filename=filename)  # redirect to the result view

    return render(request, "home.html")


def result(request, filename):

    try:
        print('Analyzing image and generating description')
        description, keywords = analyze_image_and_generate_description(filename)
    except Exception as e:
        print(f"Failed to analyze image and generate description"
              f"\n Exception: {e}")
        return render(request, "error.html")
    presigned_url = generate_presigned_url('insight-harbor', filename)
    context = {
        'filename': presigned_url,
        'description': description,
        'labels': keywords,
    }
    return render(request, "result.html", context)


def generate_presigned_url(bucket_name, object_name, expiration=3600):
    """
    Generate a presigned URL to share an S3 object

    :param bucket_name: string
    :param object_name: string
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Presigned URL as string. If error, returns None.
    """

    # Generate a presigned URL for the S3 object
    s3_client = boto3.client('s3')
    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_name},
                                                    ExpiresIn=expiration)
    except NoCredentialsError:
        print("No AWS credentials found")
        return None
    # The response contains the presigned URL
    return response