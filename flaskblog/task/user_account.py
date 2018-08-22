import os
import secrets
from PIL import Image

from flaskblog.app import app
from flaskblog.models import User

def save_picture(form_picture):
    picture_name = form_picture.filename
    _, f_ext = os.path.splitext(form_picture.filename)

    while len(User.query.filter_by(image_file=picture_name).all()) > 0:
        random_hex = secrets.token_hex(8)
        picture_name = random_hex + f_ext

    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_name)

    picture_size = (125,125)
    image = Image.open(form_picture)
    image.thumbnail(picture_size)
    image.save(picture_path)

    return picture_name
    
