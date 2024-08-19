import os
import time
import subprocess
import re
import sys

def extract_numeric_part(filename):
    match = re.search(r'\d+', filename)
    return int(match.group()) if match else float('inf')

def open_files_in_order(directory):
    files = sorted(
        (file for file in os.listdir(directory) if file.endswith(".png")),
        key=extract_numeric_part
    )

    for file in files:
        print('-' * 116)
        file_path = os.path.join(directory, file)

        subprocess.run(["ascii-image-converter.exe", file_path])

        time.sleep(1 / 10)
        


    sys.stdout.write("\033[K\r")
    sys.stdout.flush()
    

directory_path = r"C:\Users\Hp\Documents\workspace\youtube-dl\BadApple"
open_files_in_order(directory_path)
