from pathlib import Path
from PIL import Image
import pytesseract
from config import CONFIG
import os
import numpy as np
import cv2

def run_ocr(results, public_url: Path):
    """
    receive process_images (image_service.py) results then run ocr
    """

    for item in results:
        img_path = public_url / item["image_virtual_path"].lstrip("/")
        try:
            img = image_transform(img_path)
            img = Image.fromarray(img)
            text = pytesseract.image_to_string(img, lang="eng+chi_tra") # English + Chinese traditional(chi_tra)(繁體), or you can select Chinese simplified(簡體) :)

        except Exception as e:
            text = f"OCR failed: {e}"

        item["ocr_text"] = text
        item["cropped_image"] = item.pop("image_virtual_path")
    return results

def image_transform(img_path):
    img = Image.open(img_path).convert('L') # gray scale
    arr = np.array(img)

    
    _, bin_arr = cv2.threshold(arr, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU) # binary
    
    # set kernel size (maybe KS set 5 is better then 3)
    kernel_rect = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5)) # 矩形
    kernel_cross = cv2.getStructuringElement(cv2.MORPH_CROSS, (5, 5)) # 十字
    kernel_ellipse = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)) # 橢圓 (?

    
    eroded = cv2.erode(bin_arr, kernel_rect, iterations=1) # erode
    dilated = cv2.dilate(bin_arr, kernel_rect, iterations=1) # dilate  
    opened = cv2.morphologyEx(bin_arr, cv2.MORPH_OPEN, kernel_rect, iterations=1) # Opening (erode + dilate)
    closed = cv2.morphologyEx(bin_arr, cv2.MORPH_CLOSE, kernel_rect, iterations=1) # Close (dilate + erode)

    return eroded