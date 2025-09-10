from ultralytics import YOLO
import os
import shutil
import torch
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config import CONFIG
from utils import remove_dir_and_create_dir

# from ..Config import CONFIG
# import Config

def train():
    device = CONFIG.device
    model = YOLO(CONFIG.model_name).to(device)
    print(f"---------------------version: {CONFIG.model_name}---------------------")

    remove_dir_and_create_dir(CONFIG.log_path)
    results = model.train(
        data=CONFIG.data_path,
        epochs=CONFIG.epochs,
        batch=CONFIG.batch_size,
        optimizer=CONFIG.optimizer,
        imgsz=CONFIG.img_size,
        lr0=CONFIG.learning_rate,
        verbose=CONFIG.verbose,
        seed=CONFIG.seed,
        val=CONFIG.validation,
        project=CONFIG.log_path,  # Save direction of YOLO is "project", not "save_dir"
        exist_ok=True,
        workers=4
    )
    
if __name__ == '__main__':
    train()