from PIL import Image
import os
from werkzeug.utils import secure_filename
from gp import app

def add_profile_pic(pic_upload, patient_id):
    filename = pic_upload.filename
    # Grab extension type .jpg or .png
    ext_type = filename.split('.')[-1]

    # Construct the base file name
    storage_filename = str(patient_id)
    base_filepath = os.path.join(app.config["UPLOAD_FOLDER"], storage_filename)

    # Find the next available filename that doesn't conflict with existing files
    counter = 1
    # Generate the initial filepath
    filepath = f"{base_filepath}.{ext_type}"
    # Loop until a unique file name is found
    while True:
        # Check if any file exists with the current counter regardless of extension
        existing_files = [f for f in os.listdir(app.config["UPLOAD_FOLDER"]) if f.startswith(f"{storage_filename}_{counter}")]
        if not existing_files and not os.path.exists(filepath):
            break
        counter += 1
        filepath = f"{base_filepath}_{counter}.{ext_type}"

    # Secure the filename without the path
    secure_filename_only = secure_filename(os.path.basename(filepath))
    secure_filepath = os.path.join(app.config["UPLOAD_FOLDER"], secure_filename_only)
    print(secure_filepath)
    
    # Open the picture and save it
    pic = Image.open(pic_upload)
    
    # Adjust the size as needed
    output_size = (500, 500)
    pic.thumbnail(output_size)
    
    # Save the resized image
    pic.save(secure_filepath)
    
    # Return the filename only
    return secure_filename_only
