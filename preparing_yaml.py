from sklearn.model_selection import train_test_split
import os
import pandas as pd
import shutil
import sys
import yaml
from config import CONFIG
from utils import remove_dir_and_create_dir


class DatasetSplitter:
    def __init__(self, cfg, images_subdir="images", labels_subdir="labels"):
        self.Type4_path = cfg.dataset_path
        self.images_subdir = images_subdir
        self.labels_subdir = labels_subdir
        self.split_size = cfg.test_size
        self.image_path = os.path.join(self.Type4_path, self.images_subdir)
        self.label_path = os.path.join(self.Type4_path, self.labels_subdir)

        self.images=[]
        self.labels=[]
        self.images_PathDF=None
        self.labels_PathDF=None

    def collect_files(self):
        for get_file in os.listdir(self.image_path):
            if get_file.lower().endswith(('.png', '.jpg', '.jpeg')):
                self.images += [os.path.join(self.image_path, get_file)]
        self.images_PathDF = pd.DataFrame({'images': self.images})

        for get_file in os.listdir(self.label_path):
            if get_file.lower().endswith(('.txt')):
                self.labels += [os.path.join(self.label_path, get_file)]
        self.labels_PathDF = pd.DataFrame({'labels': self.labels})
    
    def spliter(self):
        self.image_train, self.image_val, self.label_train, self.label_val = train_test_split(
                                                                                self.images_PathDF, 
                                                                                self.labels_PathDF, 
                                                                                test_size=self.split_size, 
                                                                                random_state=42
                                                                            )

    def make_dir(self):
        self.image_train_path = os.path.join( self.image_path, "train")
        self.label_train_path = os.path.join( self.label_path, "train")
        self.image_val_path = os.path.join( self.image_path, "val")
        self.label_val_path = os.path.join( self.label_path, "val")

        for path in [self.image_train_path, self.label_train_path, self.image_val_path, self.label_val_path]:
            remove_dir_and_create_dir(path)
    
    def copy_files(self):
        self.image_train['images'].apply(lambda x: shutil.copy(x, self.image_train_path))
        self.label_train['labels'].apply(lambda x: shutil.copy(x, self.label_train_path))
        self.image_val['images'].apply(lambda x: shutil.copy(x, self.image_val_path))
        self.label_val['labels'].apply(lambda x: shutil.copy(x, self.label_val_path))
        

    def run_dataset_spliter(self):
        print(f"Collecting files...")
        self.collect_files()
        print(f"Spliting...")
        self.spliter()
        self.make_dir()
        self.copy_files()
        print(f"Split training / valid finished!")


def generate_data_yaml(cfg):
    data_yaml = {
        "train": cfg.train_images_dir.replace("\\", "/"),
        "val": cfg.val_images_dir.replace("\\", "/"),
        "nc": len(cfg.names),
        "names": cfg.names
    }

    with open(cfg.yaml_path, "w") as fp:
        yaml.safe_dump(data_yaml, fp, allow_unicode=True, default_flow_style=False, sort_keys=False)
    print(f"data yaml file generated successfully!")
    
    
if __name__ == "__main__":
    spliter = DatasetSplitter(CONFIG)
    spliter.run_dataset_spliter()
    
    generate_data_yaml(CONFIG)