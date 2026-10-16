# YOLOv8 裂缝检测项目

基于 YOLOv8 的裂缝检测模型训练与推理服务，包含数据集校验、模型训练、FastAPI 推理接口。

## 功能

- 数据集图片与标注文件配对校验
- YOLOv8 裂缝检测模型训练
- FastAPI 提供裂缝检测接口
- 返回裂缝数量、边界框和置信度

## 环境要求

建议使用 Python 3.8+。项目依赖已整理在 `requirements.txt` 中。

安装依赖：

```bash
pip install -r requirements.txt
```

## 目录结构

```text
yolo-demo/
├── crack_demo_dataset/          # 数据集
│   ├── images/
│   │   ├── train/
│   │   └── val/
│   └── labels/
│       ├── train/
│       └── val/
├── weights/                     # 存放模型权重的目录
├── runs/                        # 训练过程与结果输出目录
├── crack.yaml                   # 数据集配置文件
├── requirements.txt             # 项目依赖环境
├── check_dataset.py             # 数据集校验脚本
├── yolo_detect_demo.py          # 模型训练脚本
├── yolo_server.py               # FastAPI 推理服务
├── yolov8s.pt                   # 预训练权重
└── README.md
```

## 数据集准备

数据集需为 YOLO 格式，每张图片对应一个同名的 `.txt` 标注文件。

图片支持格式：

- `.jpg`
- `.jpeg`
- `.png`

标注文件格式：

- `.txt`

`crack.yaml` 示例：

```yaml
path: ./crack_demo_dataset
train: images/train
val: images/val
nc: 1
names: ['crack']
```

## 数据集校验

运行：

```bash
python check_dataset.py
```

脚本会分别校验训练集和验证集，检查图片与标注文件是否一一对应。

如果存在不匹配，会输出独有文件并抛出异常。

## 模型训练

运行：

```bash
python yolo_detect_demo.py
```

主要参数说明（可在代码中修改）：

- `data="crack.yaml"`：数据集配置文件
- `epochs=50`：训练轮次
- `imgsz=640`：输入图片尺寸
- `batch=4`：批次大小
- `device=0`：使用 GPU，CPU 训练请注释掉该行
- `workers=0`：Windows 系统建议设为 0，避免多进程报错
- `amp=False`：关闭混合精度训练，避免自动下载额外权重
- `project="runs/train"`：训练结果保存目录
- `name="crack_exp"`：本次训练实验名称

训练完成后，最佳权重保存在：

```text
runs/train/crack_exp/weights/best.pt
```

## 启动推理服务

修改 `yolo_server.py` 中的模型路径，将其替换为你实际训练得到的 `best.pt` 路径（建议使用相对路径或部署环境的绝对路径）：

```python
model = YOLO(r"runs/train/crack_exp/weights/best.pt")
```

启动服务：

```bash
python yolo_server.py
```

服务默认运行在：

```text
http://127.0.0.1:8001
```

## 接口说明

- URL: `/detect_crack`
- Method: `POST`
- Content-Type: `multipart/form-data`
- 参数: `file`，上传的图片文件

返回示例：

```json
{
  "crack_count": 2,
  "cracks": [
    {
      "bbox": [x1, y1, x2, y2],
      "conf": 0.87
    }
  ]
}
```

字段说明：

- `crack_count`：检测到的裂缝数量
- `cracks`：每个裂缝的边界框坐标和置信度
- `bbox`：`[x1, y1, x2, y2]`
- `conf`：置信度

## 调用示例

使用 curl：

```bash
curl -X POST "http://127.0.0.1:8001/detect_crack" -F "file=@test.jpg"
```

使用 Python requests：

```python
import requests

url = "http://127.0.0.1:8001/detect_crack"
files = {"file": open("test.jpg", "rb")}
res = requests.post(url, files=files)
print(res.json())
```

## 注意事项

- 训练前请确保数据集路径正确，图片与标签文件名完全一致。
- Windows 下训练时建议设置 `workers=0`。
- 如果没有 NVIDIA 显卡，请注释掉 `device=0`，使用 CPU 训练。
- 建议将 `venv/`、`__pycache__/`、`runs/` 等无需上传的目录加入 `.gitignore`。

## 许可证

本项目仅供学习交流使用。