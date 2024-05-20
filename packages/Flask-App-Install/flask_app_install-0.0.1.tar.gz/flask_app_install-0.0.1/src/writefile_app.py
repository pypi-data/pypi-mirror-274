import os
from app import create_app

# Define the directory and file name
dir_name = 'app'

# Create the directory if it doesn't exist
if not os.path.exists(dir_name):
    os.makedirs(dir_name)

# Define the full file path
file_path = os.path.join(dir_name)

# Write to the folder
with open(file_path, 'w') as my_folder:
    my_folder.write(create_app())
