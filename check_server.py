#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查服务器状态
"""

import requests
import time

def check_server(url="http://127.0.0.1:9993", timeout=5):
    """检查服务器是否正在运行"""
    try:
        response = requests.get(url, timeout=timeout)
        if response.status_code == 200:
            print(f"✅ 服务器正在运行: {url}")
            print("🌐 请在浏览器中打开此链接访问系统")
            return True
        else:
            print(f"⚠️ 服务器响应异常，状态码: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print(f"❌ 无法连接到服务器: {url}")
        print("💡 服务器可能尚未启动或端口被占用")
        return False
    except requests.exceptions.Timeout:
        print(f"⏰ 连接超时: {url}")
        return False
    except Exception as e:
        print(f"❌ 检查服务器时出错: {e}")
        return False

def main():
    print("🔍 检查Gradio服务器状态...")
    print("等待服务器启动...")
    
    for i in range(10):  # 等待最多10秒
        if check_server():
            break
        time.sleep(1)
        print(f"⏳ 等待中... ({i+1}/10)")
    else:
        print("❌ 服务器启动超时或失败")
        print("💡 请检查是否有错误信息，或手动运行: python interface.py")

if __name__ == "__main__":
    main()
