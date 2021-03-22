
from detect import (detect_logos, detect_text)
import pandas as pd
import re
import os
#from __future__ import print_function
from google.cloud import vision


images_path = "C:\\Users\\heinz\\Yagora GmbH\\Ievgen Kyrda - Crawler\\images\\foodnewsgermany_images/"
file_names = os.listdir(os.path.dirname(images_path))

file_paths = [images_path + f for f in file_names]

logos = [detect_logos(f) for f in file_paths]

texts = [detect_text(f)[0].description for f in file_paths]
# remove line break symbols
texts = [x.replace("\n", ", ") for x in texts]

contained = []
#contained[1] = "test"
for i in range(len(logos)): # loop over future rows of df
    tmp = []
    for j in logos[i]: # for every logo-row, check if in text
        if j.lower() in texts[i].lower():
            tmp.append(logos[i])
        else:
            tmp.append(None)
    contained.append(tmp)

detect_df = pd.DataFrame(
    list(zip(file_names, texts, logos, contained, file_paths)),
    columns = ["files", "texts", "logos", "probable_brand", "file_path"]
)
detect_df

# other ideas:
# if logo in existing logos, add logo



from PIL import Image
from io import BytesIO
from IPython.display import HTML
import base64


pd.set_option('display.max_colwidth', -1)

def get_thumbnail(path):
    i = Image.open(path)
    i.thumbnail((150, 150), Image.LANCZOS)
    return i


def image_base64(im):
    if isinstance(im, str):
        im = get_thumbnail(im)
    with BytesIO() as buffer:
        im.save(buffer, 'jpeg')
        return base64.b64encode(buffer.getvalue()).decode()

def image_formatter(im):
    return f'<img src="data:image/jpeg;base64,{image_base64(im)}">'

#dogs['file'] = dogs.id.map(lambda id: f'../input/train/{id}.jpg')

detect_df['image'] = detect_df.file_path.map(lambda f: get_thumbnail(f))

HTML(detect_df.to_html(formatters={'image': image_formatter}, escape=False))