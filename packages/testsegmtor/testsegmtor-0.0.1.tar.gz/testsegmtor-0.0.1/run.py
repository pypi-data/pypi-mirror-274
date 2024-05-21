# run.py

import os
import subprocess
import sys

def process_image(input_image_path, output_directory):
    if not os.path.exists(input_image_path):
        print(f"Error: The input image path '{input_image_path}' does not exist.")
        sys.exit(1)

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    executable = "./image_processor"
    
    # Construct the command
    command = [executable, input_image_path, output_directory]

    try:
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(result.stdout.decode())
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr.decode()}")
        sys.exit(1)

