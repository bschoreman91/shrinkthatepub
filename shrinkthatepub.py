import os
import shutil
import zipfile
from PIL import Image

def extract_files(zip_filename):
    # Create a new "extract" directory in the current directory
    extract_path = os.path.join(os.getcwd(), "extract")
    if os.path.exists(extract_path):
        # If the directory already exists, delete it and create a new one
        shutil.rmtree(extract_path)
    os.mkdir(extract_path)

    # Copy the epub file to a new file with a .zip extension
    zip_path = os.path.join(os.getcwd(), "file.zip")
    shutil.copyfile(zip_filename, zip_path)

    # Open the zip file
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        # Extract all contents to the "extract" directory
        zip_ref.extractall(extract_path)

    # Delete the temporary zip file
    os.remove(zip_path)

    print("Files have been extracted successfully!")

def replace_images(directory):
    # Create a list of all JPG and PNG files in the directory
    image_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(('.jpg', '.png')):
                image_files.append(os.path.join(root, file))

    # Replace each image file with a completely blank version
    for file in image_files:
        # Open the original image file to get its size
        with Image.open(file) as img:
            # Create a new blank image with the same size as the original
            blank_img = Image.new('RGB', img.size, color='white')
            # Save the blank image with lowest possible quality
            blank_img.save(file, optimize=True, quality=1)

    print("Images have been replaced successfully!")

def create_epub(directory, epub_filename):
    # Zip the contents of the "extract" directory into a new file with the original name and a .zip extension
    zip_filename = os.path.join(directory, epub_filename.replace('.epub', '_shrunk.zip'))
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zip_ref:
        for root, dirs, files in os.walk(directory):
            for file in files:
                if not file.endswith('.zip'):
                    zip_ref.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), directory))

    # Move the zip file to the base folder
    epub_path = os.path.join(os.getcwd(), epub_filename.replace('.epub', '_shrunk.epub'))
    shutil.move(zip_filename, epub_path)

    # Delete the extract folder
    shutil.rmtree(directory)

    print("Epub file has been created successfully!")

# Find all epub files in the current directory
epub_files = [file for file in os.listdir(os.getcwd()) if file.endswith('.epub')]

if epub_files:
    for epub_filename in epub_files:
        # Extract the files to a new "extract" directory
        extract_files(epub_filename)

        # Replace all images in the "extract" directory with completely blank versions
        extract_path = os.path.join(os.getcwd(), "extract")
        replace_images(extract_path)

        # Create a new epub file in the base directory
        create_epub(extract_path, epub_filename)
else:
    print("No epub files found in current directory!")
