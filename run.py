#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
启动脚本 - Gradio YOLO 视频推理系统
"""

import os
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """检查Python版本"""
    if sys.version_info < (3, 8):
        print(" 错误: 需要Python 3.8或更高版本")
        sys.exit(1)
    print(f" Python版本: {sys.version}")

def install_requirements():
    """安装依赖包"""
    requirements_file = Path("requirements.txt")
    if requirements_file.exists():
        print("📦 正在安装依赖包...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
            print(" 依赖包安装完成")
        except subprocess.CalledProcessError as e:
            print(f" 依赖包安装失败: {e}")
            return False
    return True

def download_model():
    """下载YOLO模型"""
    model_file = Path("yolo11n.pt")
    if not model_file.exists():
        print(" 正在下载YOLO11n模型...")
        try:
            from ultralytics import YOLO
            # 这会自动下载模型
            model = YOLO("yolo11n.pt")
            print(" 模型下载完成")
        except Exception as e:
            print(f" 模型下载可能失败，但系统仍可运行: {e}")

def main():
    """主函数"""
    print(" 启动 Gradio YOLO 视频推理系统")
    print("=" * 50)
    
    # 检查Python版本
    check_python_version()
    
    # 安装依赖
    if not install_requirements():
        sys.exit(1)
    
    # 下载模型
    download_model()
    
    # 将Gradio临时/静态文件目录置于当前项目目录，避免写入C盘临时目录
    project_root = Path(__file__).resolve().parent
    tmp_dir = project_root / "tmp"
    static_dir = project_root / "static"
    tmp_dir.mkdir(exist_ok=True)
    static_dir.mkdir(exist_ok=True)
    os.environ["GRADIO_TEMP_DIR"] = str(tmp_dir)
    # 允许Gradio访问当前目录，便于直接读取/写入本地文件
    allowed_paths = [str(project_root)]

    # 启动应用
    print(" 正在启动Web应用...")
    print(" 服务将在 http://127.0.0.1:9993 启动")
    print(" 按 Ctrl+C 停止服务")
    print("-" * 50)
    
    try:
        from interface import video_processing
        video_processing.launch(
            server_port=9993,
            share=False,  # 设置为True可以生成公共链接
            inbrowser=True,  # 自动打开浏览器
            show_api=False,  # 简化界面
            quiet=False,  # 显示启动信息
            allowed_paths=allowed_paths
        )
    except KeyboardInterrupt:
        print("\n 用户中断，正在关闭服务...")
    except Exception as e:
        print(f" 启动失败: {e}")
        print(" 请检查端口9993是否被占用，或尝试直接运行: python interface.py")
        sys.exit(1)

if __name__ == "__main__":
    main()
