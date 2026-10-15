from ultralytics import YOLO

def main():
    # 加载本地 yolov8s.pt 预训练权重
    model = YOLO("yolov8s.pt")

    # 开始训练
    train_results = model.train(
        data="crack.yaml",    # 数据集配置文件
        epochs=50,            # 训练轮次
        imgsz=640,            # 输入图片尺寸
        batch=4,              # 批次大小
        device=0,           # 有NVIDIA显卡就取消注释，CPU运行注释掉这一行
        workers=0,            # Windows系统建议workers=0，避免多进程报错
        amp=False,  # 新增这一行，关闭AMP，就不会去下载yolo26n.pt
        project="runs/train", # 训练结果保存目录
        name="crack_exp",
        exist_ok=True
    )
    print("训练完成！")
    print(f"结果保存在 runs/train/crack_exp")

if __name__ == "__main__":
    main()
