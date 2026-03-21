from flask import Blueprint, render_template, request, redirect, session, jsonify
from flask_login import login_user, logout_user, login_required
from db.database import db
from db.models import Users, Communities
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
import re
import boto3
from dotenv import load_dotenv
import os
from PIL import Image
import requests
import io
import os
load_dotenv()

login_blueprint = Blueprint("login", __name__, template_folder="templates")

s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_S3_ACCESS_KEY"),
    aws_secret_access_key=os.getenv("AWS_S3_SECRET_KEY"),
    region_name=os.getenv("AWS_REGION"),
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

    print(
        first_name,
        last_name,
        email,
        location,
        password,
        confirm_password,
        user_type,
        images,
    )
    if user_type == "chairperson":
        community_name = request.form.get("community_name")
        if_exists = Communities.query.filter_by(name=community_name).first()
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
            session["user_name"] = community.name
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

    if user_type == "chairperson":
        user = Users(
        name=first_name + " " + last_name,
        email=email,
        password=hashed_password,
        type=user_type,
        work_area=location,
        rating=0,
        # private_key = private_key,
        # public_key = public_key
        community_id = community.id
    )
    else:
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
        
    
    print(
        user.name,
        user.email,
        user.password,
        user.type,
        user.work_area,
        user.rating,
    )
    db.session.add(user)
    db.session.commit()
    session["user_id"] = user.id
    session["user_name"] = user.name
    session["type"] = user.type
    login_user(user)

    print(f"session id -> {session['user_id']}")
    profile_picture.stream.seek(0)
    image_verification_body = {
        "image": (profile_picture.filename, profile_picture.stream, profile_picture.mimetype)
    }
    image_verfication_response = requests.post(
        f"{os.getenv('HELPOUTS_BASE_URL_DEV')}/api/uploadProfilePicture/{user.id}",
        files=image_verification_body
    )
    # Handle AiClipse not working/ S3 issue
    # 
    # if image_verfication_response.ok:
    #     # do db commits/session
    # else:
    #     return {"error": "Image verification request failed"}, 500

    response_data = image_verfication_response.json()
    print("THIS IS THE ERROR", response_data)
    user = Users.query.get_or_404(session["user_id"])
    if response_data["verification_status"] == "skipped":
        user.verfied = False
        
    if response_data["verification_status"] == "success":
        user.verfied = True
        session["accuracy"] = response_data["accuracy"]
        print("ACCURACY IN SESSION: ", session["accuracy"])

    db.session.commit()
    return redirect("/home_page")


@login_blueprint.route("/logout")
def logout():
    logout_user()
    session.clear()
    return redirect("/")



@login_blueprint.route("/login_no_mfa", methods=["POST"])
def login_no_mfa():
    form_email = request.form.get("email")
    form_password = request.form.get("password")
    user = Users.query.filter_by(email=form_email).first()

    # check email is found
    if user is None:
        error = "Email or Password Is Incorrect"
        return render_template("login/login.html", error=error)
    
    # compare hash
    password_check = check_password_hash(user.password, form_password)
    if password_check == False:
        error = "Email or Password Is Incorrect"
        return render_template("login/login.html", error=error)
    
    # initalize session
    session["user_id"] = user.id
    session["user_name"] = user.name
    session["profile_picture"] = f"{os.getenv('AWS_S3_BUCKET')}{user.id}/profile-picture/profile-picture-m.jpg"
    session["type"] = user.type
    session["images"] = os.getenv("AWS_S3_BASE_URL")
    login_user(user)
    
    return redirect("/home_page/")
    
     



# Remove when no longer needed as test
@login_blueprint.route("/test_login_user", methods=["POST"])
def test_login_user():
    user_id = int(request.json["data"])
    user_data = Users.query.get_or_404(user_id)
    session["user_id"] = user_id
    session["user_name"] = user_data.name
     # TODO profile picture comes from S3 now, not the database
    session["profile_picture"] = user_data.profile_picture
    session["type"] = user_data.type
    if session.get("community_id") is not None:
        session.pop("community_id", None)
    # TODO profile picture comes from S3 now, not the database
    dataArray = [str(session["user_id"]), session["profile_picture"], session["type"]]
    login_user(user_data)
    print("TYPE OF USER: ", session["type"])
    return jsonify(dataArray)


# Remove when no longer needed as test
@login_blueprint.route("/test_login_admin", methods=["POST"])
def test_login_admin():
    community_id = int(request.json["data"])
    community_data = Communities.query.get_or_404(community_id)
    
    user = Users.query.filter_by(community_id=community_id, type="chairperson").first()
    session["community_id"] = community_id
    session["user_id"] = user.id
    session["user_name"] = community_data.name
    session["type"] = "chairperson"
    print("SESSION: ", session["community_id"])

     # TODO profile picture comes from S3 now, not the database * not for communities yet
    session["profile_picture"] = community_data.profile_picture
    dataArray = [
        str(session["community_id"]),
         # TODO profile picture comes from S3 now, not the database * not for communities yet
        session["profile_picture"],
        session["type"],
    ]
    login_user(user)
    print("TYPE OF USER: ", session["type"])
    return jsonify(dataArray)
