import os
import subprocess
import re
import sys
import concurrent.futures
import time

def extract_numeric_part(filename):
    match = re.search(r'\d+', filename)
    return int(match.group()) if match else float('inf')

def process_file(file_path):
    subprocess.run(["ascii-image-converter.exe", file_path])

def open_files_in_order(directory):
    files = sorted(
        (file for file in os.listdir(directory) if file.endswith(".png")),
        key=extract_numeric_part
    )

    #print('-' * 116)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        for file in files:
            sys.stdout.write("\033[H\r")
            sys.stdout.flush()

            future = executor.submit(process_file, os.path.join(directory, file))
            
            concurrent.futures.wait([future])

    sys.stdout.write("\033[H\r")
    sys.stdout.flush()

directory_path = r".\Frames"
open_files_in_order(directory_path)
