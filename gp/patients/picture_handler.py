from PIL import Image
import os
from werkzeug.utils import secure_filename
from gp import app

def add_profile_pic(pic_upload, username):
    filename = pic_upload.filename
    # Grab extension type .jpg or .png
    ext_type = filename.split('.')[-1]
    storage_filename = str(username) + '.' + ext_type
    filename = secure_filename(storage_filename)
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    print(filepath)
    
    # Open the picture and save it
    pic = Image.open(pic_upload)
    
    # Play around with this size.
    output_size = (500, 500)
    pic.thumbnail(output_size)
    
    # Save the resized image
    pic.save(filepath)

    return storage_filename
