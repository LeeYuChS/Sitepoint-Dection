import cv2
import os 
import numpy as np
from config import CONFIG
from ocr.get_bounding_box import BoundingBox
from ultralytics import YOLO
"""
BoundingBox: for YOLO process
SplitFourImg: for cutting images and return
    [
        "image_virtual_path" (relative path)
        "source_image"
        "yolo_cls"
        "bounding_box"
    ] 
then execute ocr
"""

label_map = {
    0: "E",
    1: "N",
    2: "PointName",
    3: "Z",
    4: "Other"
} 

class SplitFourImg:
    """
    after yolo get bounding box and 
    """
    def __init__(self, bounding_box, public_url_root, datetime_folder, timestamp):
        self.bounding_box = bounding_box
        self.cut_return = []
        self.storage_root = public_url_root # server public url root
        self.datetime_folder = datetime_folder # datetime for webform 
        self.timestamp = timestamp
        self.image_cutting_save_path = os.path.join(public_url_root, "4OCR", timestamp)
        os.makedirs(self.image_cutting_save_path, exist_ok=True)

    def convert(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, (np.float32, np.float64, np.float16)):
            return float(obj)
        raise TypeError(f"Type {type(obj)} not serializable")

    def cut(self):
        for idx in range(len(self.bounding_box)):
            records = self.bounding_box[idx]
            records = sorted(records, key=lambda x: x['label'])
            for label in range(len(records)):
                img = cv2.imread(records[label]['source'])
                filename = os.path.splitext(os.path.basename(records[label]['source']))[0]
                x1, y1, x2, y2 = map(int, records[label]['box'])

                label_mapped = label_map[label]
                cropped_img = img[y1:y2, x1:x2]

                save_path = os.path.join(self.image_cutting_save_path, f"{filename}_box{label}.jpg")
                cv2.imwrite(save_path, cropped_img)
                
                # for WebForm
                relative_path = os.path.relpath(save_path, self.storage_root).replace("\\", "/")
                self.cut_return.append({
                    "image_virtual_path": f"/{relative_path}",
                    "source_image": os.path.relpath(records[label]['source'], self.storage_root).replace("\\", "/"),
                    "yolo_cls": label_mapped,
                    "bounding_box": [x1, y1, x2, y2],
                })
        return self.cut_return

def process_images(public_url_root, datetime_folder, timestamp):
    bounding_box = BoundingBox(CONFIG.best_model_weight, datetime_folder)
    split_four_img = SplitFourImg(bounding_box, public_url_root, datetime_folder, timestamp)
    return split_four_img.cut()
