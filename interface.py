# -*- coding: utf-8 -*-
# @Author: xguan
# @Software: PyCharm

import gradio as gr
from style import js,css,theme
from action_function import show_params,video_inference

gr.set_static_paths(["head.png"]) #使用到的静态文件要添加到列表中



with gr.Blocks(theme=theme,fill_width=True,title="gradio and YOLO",js=js,css=css) as video_processing:
    #gr.Markdown("""# 在线视频推理""")
    with gr.Row():
        with gr.Column():
            with gr.Tab("选择视频"):
                # 选择不同的视频源将会显示不同的组件
                source_radio = gr.Radio(["视频文件", "摄像头", "URL"], label="选择视频源", value="视频文件")
                input_video = gr.File(label="上传视频文件", file_types=["video"], visible=True)
                webcam_input = gr.Textbox(label="摄像头设备", placeholder="输入摄像头设备ID (如: 0) 或留空使用默认摄像头", visible=False)
                with gr.Row():
                    url_input = gr.Textbox(label="输入URL地址", visible=False,
                                           placeholder="RTSP,RTMP,TCP或视频流的IP地址",
                                           interactive=True,scale=15)
                    # confirm_btn = gr.Button("确定",elem_classes="confirm",visible=False,scale=1,min_width=100)

                # 返回组件参见https://www.gradio.app/guides/blocks-and-event-listeners#updating-component-configurations
                @source_radio.select(inputs=source_radio, outputs=[input_video, webcam_input, url_input])
                def show_or_hidden(selected):
                    if selected == "视频文件":
                        return gr.File(visible=True), gr.Textbox(visible=False), gr.Textbox(visible=False)
                    elif selected == "摄像头":
                        return gr.File(visible=False), gr.Textbox(visible=True), gr.Textbox(visible=False)
                    else:  # URL
                        return gr.File(visible=False), gr.Textbox(visible=False), gr.Textbox(visible=True)

            with gr.Tab("选择模型"):
                model_name = gr.Dropdown(["yolo11n", "yolo11s", "yolo11m", "yolo11l"], label="模型列表",
                                         value="yolo11n",
                                         interactive=True)
                device = gr.Dropdown(["auto","cpu","cuda:0"], label="计算设备", value="auto", interactive=True)

            with gr.Accordion(label="参数设置",open=False):
                with gr.Row():
                    conf = gr.Slider(0, 1, value=0.5, label="置信度大小",interactive=True)
                    iou = gr.Slider(0, 1, value=0.7, label="IoU阈值")
                with gr.Row():
                    classes = gr.Textbox(label="检测类别(留空=全部, 例: 0,2,5)", placeholder="留空检测全部类别，或输入用逗号分隔的类别ID")
                    save = gr.Radio([True, False], value=False, label="将推理结果视频自动保存在服务端")

            with gr.Row():
                start_btn = gr.Button("开始推理", variant="primary", scale=2)
                stop_btn = gr.Button("停止推理", variant="stop", scale=1)

        with gr.Column():
            output_image = gr.Image(label="推理结果", height=400)
            process_info = gr.Button(variant="secondary", visible=False)
            with gr.Accordion(label="参数信息", open=True):
                params = gr.JSON(label="当前配置")
            with gr.Accordion(label="系统信息", open=False):
                system_info = gr.HTML("""
                <div style="padding: 10px; background-color: #f0f0f0; border-radius: 5px;">
                    <h4>🔧 系统状态</h4>
                    <p>• 支持视频格式: MP4, AVI, MOV, MKV</p>
                    <p>• 支持网络流: RTSP, RTMP, HTTP</p>
                    <p>• 支持摄像头: 本地USB摄像头</p>
                    <p>• YOLO版本: YOLOv11</p>
                </div>
                """)

    run_event = start_btn.click(fn=show_params, inputs=[input_video,webcam_input,url_input,model_name,device,conf,iou,classes,save],
                    outputs=[params], api_name="detector").then(fn=video_inference, inputs=[model_name,device,input_video,webcam_input,url_input,conf,iou,classes,save],outputs=[process_info,output_image])

    # 停止按钮用于取消正在进行的推理事件
    stop_btn.click(fn=None, inputs=None, outputs=None, cancels=[run_event])

if __name__ == "__main__":
    video_processing.launch(server_port=9993)
