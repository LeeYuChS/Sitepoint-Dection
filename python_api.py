from fastapi import FastAPI, Form
from pathlib import Path
from config import CONFIG
from services.image_service import run_process_images
from services.ocr_service import run_ocr

storage_root = Path(CONFIG.server_image_path)
public_url = Path(CONFIG.server_public_url)
app = FastAPI()

@app.post("/inference_batch")
def inference_batch(datetime_folder: str = Form(...)):
    folder = storage_root / datetime_folder
    if not folder.exists():
        return {"ok": False, "message": f"folder not found: {folder}"}

    # yolo and cut images
    results = run_process_images(str(public_url), str(folder), datetime_folder)
    # OCR
    results = run_ocr(results, public_url)
        
    return {
        "ok": True,
        "datetime_folder": datetime_folder,
        "results": results,
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
