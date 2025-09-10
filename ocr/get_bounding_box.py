from ultralytics import YOLO
import os

class BoundingBox():
    def __init__(self, yolo_model_weights, image_dir):
        self.yolo_model_weights = yolo_model_weights
        self.image_dir = image_dir
        self.model = YOLO(self.yolo_model_weights)
        self.image_files = [f for f in os.listdir(self.image_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        print(f'Number of images: {len(self.image_files)}')

    def __len__(self):
        return len(self.image_files)
    
    def __getitem__(self, idx):
        image_path = os.path.join(self.image_dir, self.image_files[idx])
        # n, s = self.get_bounding_box(image_path)
        r = self.get_bounding_box(image_path)
        return r
    
    def get_bounding_box(self, image_path):
        results = self.model.predict(image_path)
        names = (results[0].boxes.cls).cpu().numpy().astype(int)
        site = results[0].boxes.xyxy.cpu().numpy()
        # print(f'names: {names}')
        return [
            {
                "source": image_path,
                "label": names[cls_idx], 
                "box": tuple(box)
            } 
            for cls_idx, box in zip(names, site)
        ]
        # return names, site
    """
        N_x1 = site[0][0].astype(int)
        N_y1 = site[0][1].astype(int)
        N_x2 = site[0][2].astype(int)
        N_y2 = site[0][3].astype(int)

        P_x1 = site[1][0].astype(int)
        P_y1 = site[1][1].astype(int)
        P_x2 = site[1][2].astype(int)
        P_y2 = site[1][3].astype(int)

        E_x1 = site[2][0].astype(int)
        E_y1 = site[2][1].astype(int)
        E_x2 = site[2][2].astype(int)
        E_y2 = site[2][3].astype(int)

        Z_x1 = site[3][0].astype(int)
        Z_y1 = site[3][1].astype(int)
        Z_x2 = site[3][2].astype(int)
        Z_y2 = site[3][3].astype(int)

        # return (N_x1, N_y1, N_x2, N_y2), (P_x1, P_y1, P_x2, P_y2), (E_x1, E_y1, E_x2, E_y2), (Z_x1, Z_y1, Z_x2, Z_y2)
    """