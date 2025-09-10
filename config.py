import os
import torch
from datetime import datetime
from pathlib import Path

"""
    all config parameters and path setting    
    last modify: 2025-08-27-17:43
"""

class Config:
    def __init__(self):
        self.root_path = r"F:\20250711_backup\Intern\GIS\Project\YOLO-Miaoli"
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.timestamp = datetime.now().strftime("%y%m%d%H%M")

        # --------------------------------------- YOLO TRAINING SETTING head --------------------------------------- #
        # DatasetSpliter set
        self.dataset_path = os.path.join(self.root_path, "Type4_datasets") # get all train/valid images folder
        self.test_size = 0.2

        # YOLO training set
        self.nowdate = "2509021411"
        self.data_path = os.path.join(self.root_path, self.nowdate + ".yaml") # for yolo .yaml file
        
        self.log_path = f'./{self.nowdate}/logs'
        self.model_name = 'yolo12n.pt'
        self.epochs = 64
        self.batch_size = 32
        self.optimizer = 'Adam'
        self.img_size = 640
        self.learning_rate = 0.0001
        self.verbose = True
        self.seed = 42
        self.validation = True

        # generate data yaml
        self.yaml_path = os.path.join(self.root_path, self.nowdate + ".yaml") # for yolo .yaml file
        self.train_images_dir = os.path.join(self.dataset_path, "images/train")
        self.val_images_dir = os.path.join(self.dataset_path, "images/val")
        self.names = ['E', 'N', 'PointName', 'Z']
        # --------------------------------------- YOLO TRAINING SETTING tail --------------------------------------- #



        # ----------------------------------------- PYTHON API SETTING head ---------------------------------------- #
        # gui / ocr parameters
        self.best_model_weight = r"F:\20250711_backup\Intern\GIS\Project\YOLO-Miaoli\2509021411\logs\train\weights\best.pt"
        self.ocr_path = os.path.join(self.root_path, "OCR")

        # Server path
        self.server_image_path = Path(r"F:\20250711_backup\Intern\GIS\Project\YOLO-Miaoli\Miaoli-WebForm-OCR\Miaoli-WebForm-OCR\App_Data\NEZData\Uploads")
        self.server_public_url = Path(r"F:\20250711_backup\Intern\GIS\Project\YOLO-Miaoli\Miaoli-WebForm-OCR\Miaoli-WebForm-OCR")
        # ----------------------------------------- PYTHON API SETTING tail ---------------------------------------- #


CONFIG = Config()

