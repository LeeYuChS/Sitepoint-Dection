from ocr.split_four_image import process_images

def run_process_images(public_url: str, folder: str, datetime_folder: str):
    """
    call "process_images"  for python api
    """
    results = process_images(public_url, folder, datetime_folder)
    return results
