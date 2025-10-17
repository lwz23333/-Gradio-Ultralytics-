# -*- coding: utf-8 -*-
# @Author: xguan
# @Software: PyCharm

import gradio as gr
import time

def show_params(source1,source2,source3,model_name,device,conf,iou,classes,save):
    # 处理三种视频源：文件、摄像头、URL
    source = source1 if source1 else (source2 if source2 else source3)
    
    # 处理不同类型的视频源
    if source is None or source == "":
        return {"错误": "请选择视频源"}
    
    # 原始视频信息
    import cv2
    try:
        # 处理文件路径、摄像头或URL
        if isinstance(source, dict):  # gr.File 可能返回字典
            source_path = source.get('path') or source.get('name')
        elif hasattr(source, 'name'):  # 如果是文件对象
            source_path = source.name
        elif source2:  # 摄像头输入
            source_path = int(source2) if source2.isdigit() else 0
        else:  # URL或其他
            source_path = source
            
        source_cap = cv2.VideoCapture(source_path)
        if not source_cap.isOpened():
            return {"错误": f"无法打开视频源: {source_path}"}
            
        source_width = int(source_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        source_height = int(source_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        source_fps = round(source_cap.get(cv2.CAP_PROP_FPS))
        source_cap.release()
        
        # 解析类别显示：空=全部；非空显示原字符串
        classes_display = classes if (isinstance(classes, str) and classes.strip() != "") else "全部类别"

        all_params = {
            "模型":model_name,
            "设备":device,
            "置信度":conf,
            "IoU":iou,
            "目标类别": classes_display,
            "原视频":{
                "位置":source_path,
                "宽度":source_width,
                "高度":source_height,
                "fps":source_fps
            }
        }
        
        if save:
            all_params["结果视频"] = "./runs/detect/predict"
            
        return all_params
        
    except Exception as e:
        return {"错误": f"获取视频信息失败: {str(e)}"}

def video_inference(model:str,device:str,source1:str,source2:str,source3:str,conf:float,iou:float,classes:int,save:bool=False):
    """
    :param model: 模型名称
    :param source1: 本地视频文件
    :param source2: 摄像头设备ID
    :param source3: 视频流的URL
    :param conf: 置信度
    :param iou: IOU
    :param classes: 选择检测的类别
    :param save: 是否自动将结果视频保存
    :return:
    """
    try:
        gr.Info(message="ℹ️ℹ️加载模型中，请耐心等待...", duration=5)
        from ultralytics import YOLO
        import cv2
        
        # 处理视频源：文件、摄像头、URL
        source = source1 if source1 else (source2 if source2 else source3)
        if source is None or source == "":
            gr.Error("请先选择视频源!")
            return
            
        # 处理文件路径、摄像头或URL
        if isinstance(source, dict):  # gr.File 可能返回字典
            source_path = source.get('path') or source.get('name')
        elif hasattr(source, 'name'):  # 如果是Gradio文件对象
            source_path = source.name
        elif source2:  # 摄像头输入
            source_path = int(source2) if source2.isdigit() else 0
        else:  # URL或其他
            source_path = source
            
        print(f"视频源: {source_path}")
        
        # 加载模型
        try:
            # 允许传入"yolo11n"或"yolo11n.pt"
            model_name = model if str(model).endswith('.pt') else f"{model}.pt"
            # 加载到指定设备
            model = YOLO(model_name)
            if device and device != "auto":
                model.to(device)
            gr.Info(message="✅ 模型加载成功!", duration=3)
        except Exception as e:
            gr.Error(f"模型加载失败: {str(e)}")
            return
            
        # 解析classes：
        # - 空串/None => None(检测全部)
        # - "0,2,5" => [0,2,5]
        # - 单个数字字符串 => [int]
        classes_list = None
        if isinstance(classes, str):
            if classes.strip() != "":
                try:
                    classes_list = [int(x.strip()) for x in classes.split(',') if x.strip() != ""]
                    if len(classes_list) == 0:
                        classes_list = None
                except Exception:
                    classes_list = None
        elif isinstance(classes, (int, float)):
            try:
                ci = int(classes)
                if ci >= 0:
                    classes_list = [ci]
            except Exception:
                classes_list = None
        
        # 开始推理：为大视频设置较小输入尺寸与可选帧抽样提升流畅度
        try:
            # 对大模型优先尝试较小输入尺寸
            imgsz = 640
            try:
                results = model(source=source_path, conf=conf, iou=iou, classes=classes_list, save=save, stream=True, imgsz=imgsz)
            except Exception as oom:
                # 显存不足时回退更小分辨率或CPU
                gr.Warning(f"推理失败，尝试降级: {str(oom)}")
                imgsz = 512
                try:
                    results = model(source=source_path, conf=conf, iou=iou, classes=classes_list, save=save, stream=True, imgsz=imgsz)
                except Exception as oom2:
                    gr.Warning("再次降级至CPU…")
                    try:
                        model.to('cpu')
                        imgsz = 480
                        results = model(source=source_path, conf=conf, iou=iou, classes=classes_list, save=save, stream=True, imgsz=imgsz)
                    except Exception as final_err:
                        gr.Error(f"推理无法启动: {str(final_err)}")
                        return
            processed_count = 0
            start_time = time.perf_counter()
            
            gr.Info(message="🚀 开始视频推理...", duration=3)

            for result in results:
                try:
                    # 可选：对超长视频做帧抽样（例如每处理2帧显示1帧）
                    # if processed_count % 2 == 1:
                    #     processed_count += 1
                    #     continue

                    result_img = result.plot()  # 将boxes打印画在原图上
                    
                    # 智能缩放：控制最大显示尺寸，避免浏览器渲染开销
                    if max(result_img.shape) > 900:
                        scale = 900 / max(result_img.shape)
                        new_w = int(result_img.shape[1] * scale)
                        new_h = int(result_img.shape[0] * scale)
                        result_img = cv2.resize(result_img, (new_w, new_h), interpolation=cv2.INTER_AREA)
                    
                    result_img = result_img[:, :, ::-1]  # 注意把推理结果的BGR图片转为RGB

                    processed_count += 1
                    consumption = round(time.perf_counter() - start_time, 1)
                    
                    # 获取检测信息
                    detections = len(result.boxes) if result.boxes is not None else 0
                    
                    status_text = f"已处理{processed_count}帧 | 耗时{consumption}秒 | 检测到{detections}个目标"
                    
                    yield gr.Button(value=status_text, visible=True), result_img
                    
                except Exception as e:
                    gr.Warning(f"处理第{processed_count+1}帧时出错: {str(e)}")
                    continue
                    
        except Exception as e:
            gr.Error(f"视频推理失败: {str(e)}")
            return
            
    except Exception as e:
        gr.Error(f"系统错误: {str(e)}")
        return

