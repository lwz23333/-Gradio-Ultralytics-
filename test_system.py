#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
系统测试脚本
"""

import sys
import os
from pathlib import Path

def test_imports():
    """测试导入"""
    print(" 测试模块导入...")
    try:
        import gradio as gr
        print(f" Gradio版本: {gr.__version__}")
        
        import ultralytics
        from ultralytics import YOLO
        print(f" Ultralytics版本: {ultralytics.__version__}")
        
        import cv2
        print(f" OpenCV版本: {cv2.__version__}")
        
        import torch
        print(f" PyTorch版本: {torch.__version__}")
        print(f" CUDA可用: {torch.cuda.is_available()}")
        
        return True
    except ImportError as e:
        print(f" 导入失败: {e}")
        return False

def test_model_loading():
    """测试模型加载"""
    print("\n 测试模型加载...")
    try:
        from ultralytics import YOLO
        model = YOLO("yolo11n.pt")
        print(" YOLO11n模型加载成功")
        return True
    except Exception as e:
        print(f" 模型加载失败: {e}")
        return False

def test_interface_components():
    """测试界面组件"""
    print("\n 测试界面组件...")
    try:
        from interface import video_processing
        print(" 界面组件加载成功")
        return True
    except Exception as e:
        print(f" 界面组件加载失败: {e}")
        return False

def test_action_functions():
    """测试处理函数"""
    print("\n 测试处理函数...")
    try:
        from action_function import show_params, video_inference
        print(" 处理函数导入成功")
        return True
    except Exception as e:
        print(f" 处理函数导入失败: {e}")
        return False

def main():
    """主测试函数"""
    print(" 开始系统测试")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_model_loading,
        test_interface_components,
        test_action_functions
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f" 测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print(" 所有测试通过！系统可以正常运行")
        print(" 现在可以运行 'python interface.py' 或 'python run.py' 启动系统")
    else:
        print(" 部分测试失败，请检查依赖安装")
        sys.exit(1)

if __name__ == "__main__":
    main()
