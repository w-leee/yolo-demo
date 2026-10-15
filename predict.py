from ultralytics import YOLO

def main():
    # 修正路径！
    model = YOLO("runs/detect/runs/train/crack_exp/weights/best.pt")
    res = model("test.jpg", save=True)
    print("推理完成，结果图片保存到 runs/detect/predict")

if __name__ == "__main__":
    main()
