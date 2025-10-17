# -*- coding: utf-8 -*-
# @Author: xguan
# @Software: PyCharm

import gradio as gr

# 使用简化的主题配置，兼容新版本Gradio
theme = gr.themes.Default(
    primary_hue="rose",
    neutral_hue="slate",
)

js = """
function createGradioAnimation() {
    var container = document.createElement('div');
    container.id = 'gradio-animation';
    container.style.fontSize = '2em';
    container.style.fontWeight = 'bold';
    container.style.textAlign = 'center';
    container.style.marginBottom = '20px';
    container.style.backgroundImage = 'url("file=head.png")';
    container.style.backgroundSize = "contain";
    container.style.backgroundRepeat = 'no-repeat';

    var text = '在线视频推理';
    for (var i = 0; i < text.length; i++) {
        (function(i){
            setTimeout(function(){
                var letter = document.createElement('span');
                letter.style.opacity = '0';
                letter.style.transition = 'opacity 0.5s';
                letter.innerText = text[i];

                container.appendChild(letter);

                setTimeout(function() {
                    letter.style.opacity = '1';
                }, 50);
            }, i * 250);
        })(i);
    }

    var gradioContainer = document.querySelector('.gradio-container');
    gradioContainer.insertBefore(container, gradioContainer.firstChild);

    return 'Animation created';
}
"""
css = """
.confirm {background-color: #d4e7fe !important}
"""