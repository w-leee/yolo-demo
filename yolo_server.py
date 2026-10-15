# yolo_server.py
from fastapi import FastAPI, UploadFile
from ultralytics import YOLO
import cv2
import numpy as np

app = FastAPI(title="裂缝检测服务")

# ========= 这里替换成你训练好best.pt的绝对路径 =========
model = YOLO(r"D:\WorkSpace\yolo\yolo-demo\runs\detect\runs\train\crack_exp\weights\best.pt")

@app.post("/detect_crack")
async def detect_crack(file: UploadFile):
    img_bytes = await file.read()
    arr = np.frombuffer(img_bytes, np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)

    results = model(img, conf=0.35)[0]
    crack_list = []
    for box in results.boxes:
        xyxy = box.xyxy.cpu().numpy()[0].tolist()
        conf = float(box.conf[0])
        crack_list.append({
            "bbox": xyxy,
            "conf": conf
        })
    return {
        "crack_count": len(crack_list),
        "cracks": crack_list
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("yolo_server:app", host="127.0.0.1", port=8001)
