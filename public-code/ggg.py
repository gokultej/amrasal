import os
import shutil


def extract_files(source_dir, destination_dir):
    # Create destination directory if it doesn't exist
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)
    
    # Walk through the source directory
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            # Construct paths for source and destination files
            source_file = os.path.join(root, file)
            destination_file = os.path.join(destination_dir, file)
            
            # Move the file to the destination directory
            shutil.move(source_file, destination_file)

# Example usage:
source_directory = r'D:\task3-iiit\public-code\domain_adaptation\source\datasets\cityscapes\leftImg8bit\val'  # Replace with the source directory containing subdirectories
destination_directory = r'D:\task3-iiit\public-code\domain_adaptation\source\datasets\cityscapes\leftImg8bit\val'  # Replace with the destination directory

extract_files(source_directory, destination_directory)
