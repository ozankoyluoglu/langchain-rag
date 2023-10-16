# This script converts every .pdf in ./data folder to .txt files using pytesseract

import os
from PIL import Image
import pytesseract
from pdf2image import convert_from_path

def convert_pdf_to_png(filename):
    pages = convert_from_path(filename, 500)
    counter = 1
    for page in pages:
        image_filename = filename[:-4] + "_" + str(counter) + ".png"
        page.save(image_filename, 'PNG')
        counter += 1

# loop over every pdf file in data folder
# convert pdfs to png files
rootdir = './data'
for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        if file[-4:] == ".pdf":
            filename = os.path.join(subdir, file)
            print(f"processing {filename}.")
            # convert file to png
            convert_pdf_to_png(filename)

# loop over every png file in data folder
# convert them to ocr text
for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        if file[-4:] == ".png":
            filename = os.path.join(subdir, file)
            output = filename[:-4]+".txt"
            try:
                out = pytesseract.image_to_string(Image.open(filename))
            except RuntimeError as timeout_error:
                # Tesseract processing is terminated
                out = ""
                pass
            with open(output, 'w') as f:
                f.write(out)
                print(f"finished writing: {output}.")
