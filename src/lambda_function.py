import json
import boto3

s3 = boto3.resource('s3')
rekognition = boto3.client('rekognition')


def extractFaces(image, bucket):
    response = rekognition.detect_faces(
        Image={
            'S3Object': {
                'Bucket': bucket,
                'Name': image
            }
        },
        Attributes=['ALL']
    )
    return response


def detectFaces(faces):
    faceDetails = []
    for face in faces:
        faceDetail = {
            'BoundingBox': face['BoundingBox'],
            'Gender': face['Gender'],
            'AgeRange': face['AgeRange'],
            'Smile': face['Smile'],
            'Emotions': face['Emotions'],
            'Beard': face['Beard'],
            'Eyeglasses': face['Eyeglasses'],
            'EyesOpen': face['EyesOpen'],
            'MouthOpen': face['MouthOpen'],
            'Mustache': face['Mustache'],
            'Pose': face['Pose'],
            'Quality': face['Quality'],
            'Sunglasses': face['Sunglasses'],
            'Confidence': face['Confidence'],
        }
        faceDetails.append(faceDetail)
    return faceDetails


def lambda_handler(event, context):
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        image = record['s3']['object']['key']
        imageFaces = extractFaces(image, bucket)
        print(f"Detalles de los rostros detectados en la imagen: {image}\n")
        for index, faceDetail in enumerate(detectFaces(imageFaces['FaceDetails']), start=1):
            print(f"Rostro {index}:")
            for attribute, value in faceDetail.items():
                print(f"{attribute}: {json.dumps(value)}")
            print()

    return {
        'statusCode': 200,
    }
