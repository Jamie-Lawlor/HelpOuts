from flask import Blueprint, render_template, request, redirect, session
from db.database import db
import uuid
from PIL import Image
import io

api_blueprint = Blueprint("api", __name__, template_folder="templates")


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
    
    # S3 integrate will go here
    S3_key = f"{session.get('id')}/{profile_picture.filename}"
    
    return {
        "message": "Image uploaded successfully",
        "filename": profile_picture.filename,
        "user_id": session.get("id"),
        "S3_KEY": S3_key
    }, 200
    
    
@api_blueprint.route("/testUpload")
def test_upload():
    test_user_id = uuid.uuid4()
    session["id"] = test_user_id
    return render_template("test_space/image_upload.html")