import os
import uuid
from PIL import Image

SOURCE_DIR = 'image_data'
WEB_DIR = 'web_images'
POD_DIR = 'pod_images'

os.makedirs(WEB_DIR, exist_ok=True)
os.makedirs(POD_DIR, exist_ok=True)

mapping = []

for root, _, files in os.walk(SOURCE_DIR):
    for fname in files:
        if not fname.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
            continue
        path = os.path.join(root, fname)
        uid = str(uuid.uuid4())
        img = Image.open(path)
        pod_path = os.path.join(POD_DIR, f'{uid}{os.path.splitext(fname)[1]}')
        img.save(pod_path)
        web_path = os.path.join(WEB_DIR, f'{uid}.webp')
        img.save(web_path, format='WEBP', quality=85)
        mapping.append(f'{path},{pod_path},{web_path}\n')

with open('image_mapping.csv', 'w') as f:
    f.writelines(mapping)
print(f'Processed {len(mapping)} images.')
