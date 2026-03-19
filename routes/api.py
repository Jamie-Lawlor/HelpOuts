from flask import Blueprint, render_template, request, redirect, session, jsonify
import requests
import os
from db.database import db
from db.models import Users, JobLocation, Communities
import uuid
from PIL import Image
import io
import boto3
from dotenv import load_dotenv
import os
import PIL
load_dotenv()


api_blueprint = Blueprint("api", __name__, template_folder="templates")

s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_S3_ACCESS_KEY"),
    aws_secret_access_key=os.getenv("AWS_S3_SECRET_KEY"),
    region_name=os.getenv("AWS_REGION")
)

@api_blueprint.route("/uploadProfilePicture/<int:user_id>", methods=["POST"])
def update_profile_picture(user_id):

    user = Users.query.filter_by(id=user_id).first()
    if not user:
        return {"error": "User not found"}, 404

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
    except Exception as e:
        return {"error": "Uploaded file is not a valid image"}, 400
    
    # if this stage is reached the uploaded file is 100%
    # a valid image
    profile_picture.filename = "profile_picture.jpg"
    
    # send image to AiClipse for verification
    verdict = ""
    verification_status = "skipped"
    try:
        profile_picture.stream.seek(0)
        response = requests.post(
            os.getenv("AI_CLIPSE_URL_TEMP"),
            headers={
                "X-API-KEY": os.getenv("AI_CLIPSE_API_KEY")
            },
            files={
                "file": (
                    profile_picture.filename,
                    profile_picture.stream,
                    profile_picture.mimetype
                )
            },
        )

        # print("HERE" + response.status_code)
        # print("HERE" + response.text)
        if response.ok:
            try:
                data = response.json()
                verdict = data.get("verdict")
                accuracy = data.get("confidence")
                verification_status = "success"
            except ValueError:
                print("AiClipse is experiencing issues. Skipping verification.")
        else:
            print("AiClipse request failed. Skipping verification.")

    except Exception as e:
        print(f"AiClipse is experiencing issues. Skipping verification: {e}")
    
    
    # send image to AWS S3
    try:

        # define image sizes to be created
        img_sizes = {
            "s": (60, 60),
            "m": (150, 150),
            "l": (500, 500)
        }
        resized_images = {}
        base_img = Image.open(profile_picture)
        base_img = base_img.convert("RGB")

        # created resized images based on dict above
        for size_label, size in img_sizes.items():
            resized = base_img.copy()
            resized = resized.resize((size[0], size[1]), Image.LANCZOS)
            resized_images[size_label] = resized

        # loop resized images and upload to s3 with matching label in the key
        for size_label, resized_image in resized_images.items():
            object_key = (
                f"{user_id}/profile-picture/profile-picture-{size_label}.jpg"
            )
            # change PIL image to file object for upload
            resized_image_file = io.BytesIO()
            resized_image.save(resized_image_file, format="JPEG", quality=90)
            resized_image_file.seek(0)

            s3.upload_fileobj(
                resized_image_file,
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
    
    # update users profile picure url in the db
    user.profile_picture = db_profile_picture_url
    db.session.commit()

    
    return {
        "message": "Image uploaded successfully",
        "filename": profile_picture.filename,
        "user_id": user_id,
        "profile_url": db_profile_picture_url,
        "verification_status": verification_status,
        "verdict": verdict,
        "accuracy": accuracy,
    }, 200
    

@api_blueprint.route("/getJobMap/<int:job_id>", methods=["GET"])
def get_job_map(job_id):   

    location = JobLocation.query.filter_by(job_id=job_id).first()
    if not location:
        return jsonify({"error": "Location not found"}), 404

    return jsonify({
        "job_id": job_id,
        "lat": location.lat,
        "lng": location.lng,
        "icon_id": location.icon_id
    }), 200

@api_blueprint.route("/getCommunityMap/<int:community_id>", methods=["GET"])
def get_community_map(community_id):   

    community = Communities.query.filter_by(id=community_id).first()
    if not community:
        return jsonify({"error": "Location not found"}), 404

    return jsonify({
        "community": community_id,
        "lat": community.lat,
        "lng": community.lng,
        "icon_id": community.profile_picture
    }), 200

@api_blueprint.route("/testMap")
def test_map():
    # test_user_id = uuid.uuid4()
    # test_valid_user_id = 1
    # session["user_id"] = test_valid_user_id
    return render_template("test_space/testMaps.html")

@api_blueprint.route("/testUpload")
def test_upload():
    test_user_id = uuid.uuid4()
    test_valid_user_id = 1
    session["user_id"] = test_valid_user_id
    return render_template("test_space/image_upload.html")