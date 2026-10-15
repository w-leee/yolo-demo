import os

def check_pair(img_root, label_root):
    exts = [".jpg", ".jpeg", ".png"]
    img_names = set()
    for f in os.listdir(img_root):
        name, ext = os.path.splitext(f)
        if ext.lower() in exts:
            img_names.add(name)
    label_names = set()
    for f in os.listdir(label_root):
        name, ext = os.path.splitext(f)
        if ext == ".txt":
            label_names.add(name)
    only_img = img_names - label_names
    only_label = label_names - img_names
    print(f"图片独有文件：{only_img if only_img else '无'}")
    print(f"标注独有文件：{only_label if only_label else '无'}")
    return len(only_img) == 0 and len(only_label) == 0

if __name__ == "__main__":
    print("===== 训练集校验 =====")
    ok_train = check_pair("crack_demo_dataset/images/train", "crack_demo_dataset/labels/train")
    print("===== 验证集校验 =====")
    ok_val = check_pair("crack_demo_dataset/images/val", "crack_demo_dataset/labels/val")
    all_ok = ok_train and ok_val
    print("\n✅ 全部配对成功？", all_ok)
    if not all_ok:
        raise Exception("数据集图片与标注不匹配，请检查文件名！")
