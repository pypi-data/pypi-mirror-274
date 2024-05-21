#!/usr/bin/env python3
import os
import zipfile

def zip_current_directory():
    current_dir = os.path.basename(os.getcwd())  # Get the base name of the current directory
    zip_filename = current_dir + ".zip"  # Construct the zip file name using the directory name

    # Check if imsmanifest.xml exists in the current directory
    if "imsmanifest.xml" in os.listdir():
        # Create a ZipFile object
        with zipfile.ZipFile(zip_filename, "w") as zipf:
            # Walk through the directory and add each file to the zip
            for foldername, subfolders, filenames in os.walk("."):
                for filename in filenames:
                    # Exclude the zip file itself from being zipped again
                    if filename != zip_filename:
                        filepath = os.path.join(foldername, filename)
                        zipf.write(filepath, os.path.relpath(filepath, "."))

        print(f"SCORM project created successfully! Zip file: {zip_filename}")
    else:
        print("imsmanifest.xml not found in the current directory.")

if __name__ == "__main__":
    zip_current_directory()

