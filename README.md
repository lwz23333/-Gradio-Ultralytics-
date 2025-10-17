# Gradio + Ultralytics YOLO 实时/离线视频推理系统

一个基于 Gradio 的轻量 Web 界面，集成 Ultralytics YOLO（YOLOv8/YOLO11）进行本地文件、摄像头与网络流（RTSP/RTMP/HTTP 等）的目标检测推理。支持参数可视化配置、实时结果展示与可选的本地保存。

> 如需快速体验：直接运行 `python run.py`，浏览器会自动打开 `http://127.0.0.1:9993`。

---

## 功能特性
- 本地视频/摄像头/网络流的实时目标检测
- 一键启动脚本，自动安装依赖并下载 YOLO 模型
- 多模型选择：`yolo11n / yolo11s / yolo11m / yolo11l`（速度与精度可权衡）
- 参数在线可视化配置：置信度、IoU 阈值、类别过滤、是否保存结果等
- 结果可选本地保存到 `tmp/`，便于复盘与分享
- 简洁的 UI 布局与可定制主题/样式（CSS/JS/HTML）

---

## 环境要求
- Python 3.8+
- 可选：NVIDIA GPU + CUDA（用于大幅加速推理）

> GPU/CPU 都可运行。若使用 GPU，请安装与你 CUDA 匹配的 `torch/torchvision` 版本。

---

## 快速开始

### 方法一：一键启动（推荐）
```bash
python run.py
```
启动脚本将：
- 检查 Python 版本
- 自动安装 `requirements.txt` 依赖
- 自动下载 `yolo11n.pt`（首次）
- 启动 Web 服务（默认端口 `9993`）并自动打开浏览器

运行成功后，访问：`http://127.0.0.1:9993`

### 方法二：手动运行
```bash
# 安装依赖
pip install -r requirements.txt

# 直接运行界面
python interface.py
```

---

## 使用说明
- 选择视频源：
  - 本地文件（MP4/AVI/MOV 等）
  - 摄像头（输入设备 ID，如 `0`）
  - 网络流（RTSP/RTMP/HTTP URL）
- 选择模型：
  - `yolo11n` 最快，适合低资源/快速预览
  - `yolo11s` 速度/精度平衡
  - `yolo11m` 更高精度，速度中等
  - `yolo11l` 最高精度，速度最慢
- 调整参数：
  - 置信度阈值、IoU 阈值、类别过滤、是否保存结果等
- 可选保存：勾选后将推理结果帧/视频保存至 `tmp/`

> 前端实时显示通过生成器 `stream=True` 实现逐帧输出；图像通道会从 OpenCV BGR 转为 RGB 以适配 Gradio。

---

## 目录结构（节选）
```
.
├── run.py                  # 一键启动脚本（安装依赖、下载模型、启动服务）
├── interface.py            # Gradio 页面与交互逻辑
├── action_function.py      # 推理/处理相关函数
├── requirements.txt        # 依赖清单
├── style.css / style.js    # 可选自定义样式与脚本
├── tmp/                    # 运行时生成的临时/输出文件（可在 .gitignore 中忽略）
├── mdimages/               # README/文档中的图片资源
└── README.md               # 本文件
```

---

## 依赖
核心依赖如下，完整见 `requirements.txt`：
```
gradio>=4.40.0
ultralytics>=8.3.0
opencv-python>=4.6.0
torch>=1.12.0
torchvision>=0.13.0
numpy>=1.23.0
Pillow>=9.2.0
```

> 需要 GPU 时请参考 PyTorch 官方文档选择与你 CUDA 匹配的版本。

---

## 常见问题 FAQ
- 推不动到 GitHub：仓库中含有超大文件（如 `.mp4`, `.pt`）会被拒绝，请在 `.gitignore` 忽略或改用 Git LFS，并清理历史后再推送。
- 端口被占用：修改 `run.py` 中的 `server_port`，或直接运行 `python interface.py` 并通过参数配置端口。
- 第一次加载模型慢：首次会自动下载权重；可预先将 `yolo11*.pt` 放在项目根目录。
- 网络流无法打开：确认 URL、权限与网络连通性；必要时降低分辨率/码率。

---

## 许可协议
本项目遵循开源许可证（见 `LICENSE`）。Ultralytics YOLO 遵循其各自的上游许可与使用条款。

---

## 致谢
- [Ultralytics](https://ultralytics.com/) 提供易用的 YOLO 推理接口
- [Gradio](https://www.gradio.app/) 让 ML Web UI 的搭建变得简单

如果对你有帮助，欢迎 Star 支持！