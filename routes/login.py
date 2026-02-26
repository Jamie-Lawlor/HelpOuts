from flask import Blueprint, render_template, request, redirect, session,jsonify
from db.database import db
from db.models import Users, Communities
from werkzeug.security import generate_password_hash
import re
import boto3
from dotenv import load_dotenv
import os
from PIL import Image
import requests
import io

load_dotenv()

login_blueprint = Blueprint("login", __name__, template_folder="templates")

s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_S3_ACCESS_KEY"),
    aws_secret_access_key=os.getenv("AWS_S3_SECRET_KEY"),
    region_name=os.getenv("AWS_REGION")
)

@login_blueprint.route("/login/")
def login():
    return render_template("login/login.html")

@login_blueprint.route("/register_page/")
def register_page():
    return render_template("login/register_account.html")


@login_blueprint.route("/helper_register_page/")
def helper_register_page():
    return render_template("login/helper_register_account.html")


@login_blueprint.route("/register", methods=["POST"])
def register():
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    email = request.form.get("email")
    location = request.form.get("location")
    password = request.form.get("password")
    confirm_password = request.form.get("confirm_password")
    user_type = request.form.get("user_type")
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
    
    profile_picture.filename = "profile_picture.jpg"

    print(first_name, last_name, email, location, password, confirm_password, user_type, images)
    if user_type =="chairperson":
        community_name = request.form.get("community_name")
        if_exists = Communities.query.filter_by(name = community_name).first()
        if if_exists:
            error = "A community with this name already exists"
            return render_template("login/register_account.html", error=error)
        else:
            community = Communities(
            name=community_name,
            area=location,
            description="",
            profile_picture="",
        )
            db.session.add(community)
            db.session.commit()
            session["community_id"] = community.id
    # check if this users already exists

    if_exists = Users.query.filter_by(email=email).first()
    if if_exists:
        # this error message is passed to the frontend and can be used to display an error to the user
        error = "A user with this email already exists"
        return render_template("login/register_account.html", error=error)

    # validate password & user details

    # https://mailtrap.io/blog/flask-contact-form/#Custom-Validation-Functions - custom validation
    if not first_name or not last_name or not email or not location or not password:
        error = "All Fields Must Be Filled Out"
        return render_template("login/register_account.html", error=error)

    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        error = "Invalid Email Entered, Please Enter an Email Like 'example@gmail.com'"
        return render_template("login/register_account.html", error=error)

    # password regular expression
    if len(password) < 8:
        error = "Invalid Password Entered, Must be More than 8 Characters"
        return render_template("login/register_account.html", error=error)
    if not re.search(r"[A-Z]", password):
        error = "Invalid Password Entered, Must have a Uppercase Letter"
        return render_template("login/register_account.html", error=error)
    if not re.search(r"[a-z]", password):
        error = "Invalid Password Entered, Must have a Lowercase Letter"
        return render_template("login/register_account.html", error=error)
    if not re.search(r"[0-9]", password):
        error = "Invalid Password Entered, Must have a Number"
        return render_template("login/register_account.html", error=error)

    if confirm_password != password:
        error = "Passwords Do Not Match, Please Try Again"
        return render_template("login/register_account.html", error=error)

    hashed_password = generate_password_hash(password)

    # key = RSA.generate(2048)
    # private_key = key
    # public_key = key.public_key
    try: 
        profile_picture.stream.seek(0)
        print("URL_TEMP: ",os.getenv("AI_CLIPSE_URL_TEMP"))
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
            }
        )
        data = response.json()
        verdict = data["verdict"]
        accuracy = data["confidence"]
        print("ACCURACY: ",accuracy)
        label = data["label"]
        # if we want to reject an image and do something different
        # it will go here, for now image is sent to aws and the 
        # link is written to db
    except Exception as e:
        print(f"ERROR: {e}")
    #     return {"error": "Error validating image"}
   
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
        for label, size in img_sizes.items():
            resized = base_img.copy()
            resized = resized.resize((size[0], size[1]), Image.LANCZOS)
            resized_images[label] = resized
        
        user = Users(
        name=first_name + " " + last_name,
        email=email,
        password=hashed_password,
        type=user_type,
        work_area=location,
        rating=0,
        # private_key = private_key,
        # public_key = public_key
    )
        
        # loop resized images and upload to s3 with matching label in the key
        for label, resized_image in resized_images.items():
            object_key = (
                f"2/profile-picture/profile-picture-{label}.jpg"
            )
            # change PIL image to file object for upload
            resized_image_file = io.BytesIO()
            resized_image.save(resized_image_file, format="JPEG", quality=90)
            resized_image_file.seek(0)
            # s3.upload_fileobj(
            #     resized_image_file,
            #     os.getenv("AWS_S3_BUCKET"),
            #     object_key,
            #     ExtraArgs={
            #         "ContentType": "image/jpg"
            #     },
            # )
    except Exception as e:
        print(f"ERROR: {e}")
        return {"error": "Error uploading image to S3"}
    
    db_profile_picture_url = f"{os.getenv('AWS_S3_BASE_URL')}{object_key}"
    print(db_profile_picture_url)
    user.profile_picture = db_profile_picture_url
    print(user.name, user.email, user.password, user.type, user.work_area, user.rating, user.profile_picture)
    db.session.add(user)
    db.session.commit()
    session["user_id"] = user.id
    session["type"] = user.type
    return redirect("/home_page/")


@login_blueprint.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect("/")

#Remove when no longer needed as test
@login_blueprint.route("/test_login_user", methods=["POST"])
def test_login_user():
    user_id = int(request.json["data"])
    user_data = Users.query.get_or_404(user_id)
    session["user_id"] = user_id
    session["profile_picture"] = user_data.profile_picture
    session["type"] = "helper"
    if session.get("community_id") is not None:
        session.pop("community_id", None)
    dataArray = [str(session["user_id"]), session["profile_picture"], session["type"]]
    print("TYPE OF USER: ", session["type"])
    return jsonify(dataArray)

#Remove when no longer needed as test
@login_blueprint.route("/test_login_admin", methods=["POST"])
def test_login_admin():
    community_id = int(request.json["data"])
    community_data = Communities.query.get_or_404(community_id)
    session["community_id"] = community_id
    session["type"] = "chairperson"
    print("SESSION: ",session["community_id"])
    session["profile_picture"] = community_data.profile_picture
    dataArray = [str(session["community_id"]), session["profile_picture"], session["type"]]
    print("TYPE OF USER: ", session["type"])
    return jsonify(dataArray)

