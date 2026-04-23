from flask import Blueprint, render_template, request, redirect, session, jsonify
import requests
import os
from db.database import db
from db.models import Users, JobLocation, Communities, Logs, Jobs, Projects, MapIcon
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
    region_name=os.getenv("AWS_REGION")
)


# --------------------
# Profile Picture Routes
# --------------------
@api_blueprint.route("/uploadProfilePicture/<int:user_id>", methods=["POST"])
def upload_profile_picture(user_id):
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
                f"users/{user_id}/profile-picture/profile-picture-{size_label}.jpg"
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

    # LOGS
    log = Logs (
        user_id = user_id,
        action = "Updated Profile Picture",
        target = "Profile"
    )
    db.session.add(log)
    db.session.commit()
    
    return {
        "message": "Image uploaded successfully",
        "filename": profile_picture.filename,
        "user_id": user_id,
        "profile_url": db_profile_picture_url
    }, 200


@api_blueprint.route("/verifiedUpload/<int:user_id>", methods=["POST"])
def verified_upload(user_id):

    user = Users.query.filter_by(id=user_id).first()
    if not user:
        return {"error": "User not found"}, 404
    
    is_community = request.form.get("isCommunity")
    print(f"IS COMMUNITY: {is_community}")


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
    accuracy = ""
    try:
        profile_picture.stream.seek(0)
        response = requests.post(
            os.getenv("AI_CLIPSE_URL"),
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
            key = ""
            if is_community == "True": 
                key = f"communities/{user.community_id}/profile-picture/profile-picture-{size_label}.jpg"
            else: 
                key = f"users/{user_id}/profile-picture/profile-picture-{size_label}.jpg"
            object_key = (key)
            
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

    # LOGS
    log = Logs (
        user_id = user_id,
        action = "Updated Profile Picture",
        target = "Profile"
    )
    db.session.add(log)
    db.session.commit()
    
    return {
        "message": "Image uploaded successfully",
        "filename": profile_picture.filename,
        "user_id": user_id,
        "profile_url": db_profile_picture_url,
        "verification_status": verification_status,
        "verdict": verdict,
        "accuracy": accuracy
    }, 200


# --------------------
# Project Routes
# --------------------
@api_blueprint.route("/uploadProjectImage/<int:project_id>", methods=["POST"])
def upload_project_image(project_id):
    # Check project exists
    projectExists = Projects.query.filter_by(id=project_id)
    if not projectExists:
        return jsonify({"error": "Project not found", "success": False}), 404
    
    image = request.files.getlist("images")
    # Validate image file
    if not image: 
        return jsonify({"error": "No image uploaded", "success": False}), 400
    
    image = image[0]
    try:
        img = Image.open(image)
        img.load() 
        img = Image.open(image)
    except Exception as e:
        return jsonify({"error": f"Uploaded file {image.filename} is not a valid image", "success": False}), 400
    img.seek(0)
    img = img.convert("RGB")
        
    try:
        # escpaing file names to fix uploaded key issue - https://ssojet.com/escaping/url-escaping-in-python#pythons-urllibparse-module
        image.filename = f"project-thumbnail.jpg"
        object_key = f"projects/{project_id}/{image.filename}"
        
        image_file = io.BytesIO()
        img.save(image_file, format="JPEG", quality=90)
        image_file.seek(0)

        s3.upload_fileobj(
            image_file,
            os.getenv("AWS_S3_BUCKET"),
            object_key,
            ExtraArgs={
                "ContentType": "image/jpg",
            },
        )
        
    except Exception as e:
        print(f"ERROR: {e}")
        return jsonify({"error": f"Error uploading image {image.filename} to S3", "success": False}), 400
       
            
    return jsonify({"message": "Uploading project thumbnail", "success": True}), 200


@api_blueprint.route("/deleteProjectImages/<int:project_id>", methods=["DELETE"])
def delete_project_images(project_id):


    image_url = f"{os.getenv('AWS_S3_BASE_URL')}projects/{project_id}/project-thumbnail.jpg"
    object_key = image_url.split(f"{os.getenv('AWS_S3_BASE_URL')}")[-1]
    try:
        s3.delete_object(Bucket=os.getenv("AWS_S3_BUCKET"), Key=object_key)
    except Exception as e:
        print(f"ERROR: {e}")
        return jsonify({"error": f"Error deleting image at {image_url}"}), 400
        
    return jsonify({"message": "Images deleted successfully"}), 200


# --------------------
# Job Routes
# --------------------
@api_blueprint.route("/uploadJobImage/<int:job_id>", methods=["POST"])
def upload_job_image(job_id):
    print("UPLOAD JOB IMAGE API CALLED")
    # Check job exists
    jobExists = Jobs.query.filter_by(id=job_id).first()
    if not jobExists:
        return jsonify({"error": "Job not found", "success": False}), 404
    
    images = request.files.getlist("images")
    print("2")
    # Validate image file
    if not images or images[0].filename == "": 
        return jsonify({"error": "No image uploaded", "success": False}), 400
    
    print("3")
    
    if len(images) == 0:
        return jsonify({"error": "No images uploaded", "success": False}), 400
    else: 
        for index, image in enumerate(images):
       
            try:
                img = Image.open(image)
                img.load() 
                img = Image.open(image)
            except Exception as e:
                return jsonify({"error": f"Uploaded file {image.filename} is not a valid image"}), 400
            img.seek(0)
            img = img.convert("RGB")
            
            try:
                # escpaing file names to fix uploaded key issue - https://ssojet.com/escaping/url-escaping-in-python#pythons-urllibparse-module
                image.filename = f"{index}.jpg"
                object_key = f"jobs/{jobExists.id}/{image.filename}"
                
                image_file = io.BytesIO()
                img.save(image_file, format="JPEG", quality=90)
                image_file.seek(0)

                s3.upload_fileobj(
                    image_file,
                    os.getenv("AWS_S3_BUCKET"),
                    object_key,
                    ExtraArgs={
                        "ContentType": "image/jpg",
                    },
                )
                
            except Exception as e:
                print(f"ERROR: {e}")
                return {"error": f"Error uploading image {image.filename} to S3"}, 400
        return jsonify({"message": "Uploading multiple job images", "success": True}), 200


@api_blueprint.route("/getJobImages/<int:job_id>", methods=["GET"])
def get_job_images(job_id):
    job = Jobs.query.filter_by(id=job_id).first()
    if not job:
        return jsonify({"error": "Job not found"}), 404
    
    # Requesting images from S3 https://stackoverflow.com/questions/60355683/how-to-access-aws-s3-data-using-boto3
    # response = s3.get_object(Bucket=os.getenv("AWS_S3_BUCKET"), Key=f"jobs/{job.job_title}/")
    # https://docs.aws.amazon.com/boto3/latest/reference/services/s3/client/list_objects.html

    response = s3.list_objects(
        Bucket=os.getenv("AWS_S3_BUCKET"),
        Prefix=f"jobs/{job_id}/"
    )
    image_urls = []
    
    # Check if any files were actually found
    if 'Contents' in response:
        for obj in response['Contents']:
            key = obj['Key']
            if key != response['Prefix']:
                # Construct the public URL
                url = f"https://{os.getenv('AWS_S3_BUCKET')}.s3.{os.getenv('AWS_REGION')}.amazonaws.com/{key}"
                image_urls.append(url)
    else:
        return jsonify({"error": "No images found for this job", "success": False}), 404
    
    
    return jsonify({"images": image_urls, "success": True}), 200

@api_blueprint.route("/getJobImage/<int:job_id>", methods=["GET"])
def get_job_image(job_id):
    job = Jobs.query.filter_by(id=job_id).first()
    if not job:
        return jsonify({"error": "Job not found"}), 404

    response = s3.list_objects(
        Bucket=os.getenv("AWS_S3_BUCKET"),
        Prefix=f"jobs/{job_id}/"
    )
    
    if 'Contents' in response:
        for obj in response['Contents']:
            key = obj['Key']
            
            if key != f"jobs/{job_id}/":
                url = f"https://{os.getenv('AWS_S3_BUCKET')}.s3.{os.getenv('AWS_REGION')}.amazonaws.com/{key}"
                return jsonify({"image": url, "success": True}), 200

    return jsonify({"error": "No images found for this job", "success": False}), 404


@api_blueprint.route("/deleteJobImages/<int:job_id>", methods=["DELETE"])
def delete_job_images(job_id):

    images, _ = get_job_images(job_id)

    if _ != 200:
        return jsonify({"error": "No images found for this job", "success": False}), 404
    
    image_urls = images.get_json().get("images", [])
    for url in image_urls: 
        object_key = url.split(f"{os.getenv('AWS_S3_BASE_URL')}")[-1]
        try:
            s3.delete_object(Bucket=os.getenv("AWS_S3_BUCKET"), Key=object_key)
        except Exception as e:
            print(f"ERROR: {e}")
            return jsonify({"error": f"Error deleting image at {url}"}), 400
        
    return jsonify({"message": "Images deleted successfully"}), 200


# --------------------
# Map Routes
# --------------------
@api_blueprint.route("/getJobMap/<int:job_id>", methods=["GET"])
def get_job_map(job_id):   

    location = JobLocation.query.filter_by(job_id=job_id).first()
    if not location:
        return jsonify({"error": "Location not found"}), 404
    icon_url = MapIcon.query.filter_by(id=location.icon_id).first()
    print("HERE")
    print(icon_url.icon_url)
    return jsonify({
        "job_id": job_id,
        "lat": location.lat,
        "lng": location.lng,
        "icon_url": icon_url.icon_url
    }), 200


@api_blueprint.route("/getCommunityMap/<int:community_id>", methods=["GET"])
def get_community_map(community_id):   

    community = Communities.query.filter_by(id=community_id).first()
    if not community:
        return jsonify({"error": "Location not found"}), 404

    return jsonify({
        "community": community_id,
        "name": community.name,
        "lat": community.lat,
        "lng": community.lng,
        "icon_url": os.getenv('AWS_S3_BASE_URL') + f"communities/{community_id}/profile-picture/profile-picture-m.jpg"
    }), 200


# --------------------
# Test Routes
# --------------------
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