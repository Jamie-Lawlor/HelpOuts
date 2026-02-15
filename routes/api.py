from flask import Blueprint, render_template, request, redirect, session
import requests
import os
from db.database import db
from db.models import Users
import uuid
from PIL import Image
import io
import boto3
from dotenv import load_dotenv
import os
load_dotenv()


api_blueprint = Blueprint("api", __name__, template_folder="templates")

s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_S3_ACCESS_KEY"),
    aws_secret_access_key=os.getenv("AWS_S3_SECRET_KEY"),
    region_name="eu-west-1"
)

@api_blueprint.route("/imageUpload", methods=["POST"])
def image_upload():
    # getlist returns a list of files but we only want one, 
    # the below checks ensure there are only 1 image
    images = request.files.getlist("image")
    if not images or images[0].filename == "": 
        return {"error": "No image uploaded"}, 400
    
    if len(images) > 1: 
        return {"error": "Only one image can be uploaded"}, 400
    
    profile_picture = images[0] 
    
    # use PIL to verify the file is actually an image file
    try:
        image = Image.open(profile_picture)
        image.load() 
        image = Image.open(profile_picture)
        image.thumbnail((500, 500)) # this size is still to be decided

    except Exception as e:
        return {"error": "Uploaded file is not a valid image"}, 400
    
    # if this stage is reached the uploaded file is 100%
    # a valid image
    profile_picture.filename = "profile_picture.jpg"
    
    # send image to AiClipse for verification
    # try: 
    #     response = requests.post(
    #         os.getenv("AI_CLIPSE_URL"),
    #         headers={
    #             "X-API-KEY": os.getenv("AI_CLIPSE_API_KEY")
    #         },
    #         files={
    #             "file": (
    #                 profile_picture.filename,
    #                 profile_picture.stream,
    #                 profile_picture.mimetype
    #             )
    #         }
    #     )
    #     data = response.json()
    #     verdict = data["verdict"]
    #     accuracy = data["confidence"]
    #     label = data["label"]
    #     # if we want to reject an image and do something different
    #     # it will go here, for now image is sent to aws and the 
    #     # link is written to db
    # except Exception as e:
    #     print(f"ERROR: {e}")
    #     return {"error": "Error validating image"}
    
    # send image to AWS S3
    try:
        # if we want to store different sized images it would be 
        # done here with multiple keys
        object_key = (
            f"{session.get('id')}/profile-picture/profile-picture.jpg"
        )

        profile_picture.stream.seek(0) 
        s3.upload_fileobj(
            profile_picture.stream,
            os.getenv("AWS_S3_BUCKET"),
            object_key,
            ExtraArgs={
                "ContentType": "image/jpg",
            },
        )
    except Exception as e:
        print(f"ERROR: {e}")
        return {"error": "Error uploading image to S3"}
    
    db_profile_picture_url = f"{os.getenv('AWS_S3_BASE_URL')}{object_key}"
    
    
    return {
        "message": "Image uploaded successfully",
        "filename": profile_picture.filename,
        "user_id": session.get("id"),
        "S3_KEY": object_key,
        "profile_url": db_profile_picture_url,
        # "verdict": verdict,
        # "accuracy": accuracy,
        # "label": label
    }, 200
    
    
@api_blueprint.route("/testUpload")
def test_upload():
    test_user_id = uuid.uuid4()
    test_valid_user_id = 1
    session["id"] = test_valid_user_id
    return render_template("test_space/image_upload.html")