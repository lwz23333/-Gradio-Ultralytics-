#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速测试脚本 - 验证系统是否可以正常启动
"""

def test_gradio_interface():
    """测试Gradio界面是否可以创建"""
    print("🧪 测试Gradio界面创建...")
    try:
        import gradio as gr
        from style import theme, js, css
        
        # 测试主题是否正常
        print(f"✅ 主题类型: {type(theme)}")
        
        # 测试简单界面创建
        with gr.Blocks(theme=theme, js=js, css=css) as demo:
            gr.Markdown("# 测试界面")
            gr.Button("测试按钮")
        
        print("✅ Gradio界面创建成功")
        return True
    except Exception as e:
        print(f"❌ Gradio界面创建失败: {e}")
        return False

def test_yolo_model():
    """测试YOLO模型加载"""
    print("\n🤖 测试YOLO模型...")
    try:
        from ultralytics import YOLO
        model = YOLO("yolo11n.pt")
        print("✅ YOLO模型加载成功")
        return True
    except Exception as e:
        print(f"❌ YOLO模型加载失败: {e}")
        return False

def test_action_functions():
    """测试处理函数"""
    print("\n⚙️ 测试处理函数...")
    try:
        from action_function import show_params, video_inference
        print("✅ 处理函数导入成功")
        return True
    except Exception as e:
        print(f"❌ 处理函数导入失败: {e}")
        return False

def main():
    """主函数"""
    print("🚀 快速系统测试")
    print("=" * 40)
    
    tests = [
        test_gradio_interface,
        test_yolo_model,
        test_action_functions
    ]
    
    passed = 0
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 40)
    print(f"📊 测试结果: {passed}/{len(tests)} 通过")
    
    if passed == len(tests):
        print("🎉 系统测试通过！可以启动应用了")
        print("💡 运行命令: python run.py")
    else:
        print("⚠️ 部分测试失败，请检查错误信息")

if __name__ == "__main__":
    main()
