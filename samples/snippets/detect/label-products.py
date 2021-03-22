#import * from detect
import pandas as pd
import re
import os
from __future__ import print_function
from google.cloud import vision

#image_uri = 'gs://cloud-vision-codelab/otter_crossing.jpg'
#
# path = "C:\\Users\\heinz\\Yagora GmbH\\Ievgen Kyrda - Crawler\\images\\foodnewsgermany_images/CLhW-4CsVui.jpg"
images_path = "C:\\Users\\heinz\\Yagora GmbH\\Ievgen Kyrda - Crawler\\images\\foodnewsgermany_images/"
file_names = os.listdir(os.path.dirname(images_path))
    


file_paths = [images_path + f for f in files]

logos = [detect_logos(f) for f in file_paths]

texts = [detect_text(f)[0].description for f in file_paths]
# remove line break symbols
texts = [x.replace("\n", ", ") for x in texts]

contained = []
contained[1] = "test"
for i in range(len(logos)):
    for j in logos[i]:
        if j.lower() in texts[i].lower():
            contained.append(logos[i])
        else:
            contained.append(None)

detect_df = pd.DataFrame(
    list(zip(file_names, texts, logos, contained)),
    columns = ["files", "texts", "logos", "probable_brand"]
)
detect_df

# other ideas:
# if logo in existing logos, add logo
