import sys
import os
# 获取当前文件的父目录
base_dir = os.path.dirname(os.path.abspath(__file__))
# 设置目录的路径
project_dir0 = os.path.join(base_dir, 'src')
project_dir1 = os.path.join(base_dir, 'KUN_script')
# 将项目目录添加到 sys.path
sys.path.insert(0, project_dir0)
sys.path.insert(1, project_dir1)
voice_model_config_path = os.path.join(project_dir1, "model/config.json")
voice_model_path = os.path.join(project_dir1, "model")
# # 打印路径查看是否添加成功
# print(project_dir0)
# print(project_dir1)
# print(sys.path)

# #导入模块
# try:
#     import src,KUN_script
#     print("Module imported successfully!")
# except ImportError as e:
#     print(f"Error importing module: {e}")



import streamlit as st
from PIL import Image
from pathlib import Path
import scipy.io.wavfile as wavf
import torch
import pyaudio

from src.img_to_text import load_model,img2text
from src.text_extensions import text_extension
from src.translate import baidu_api

from KUN_script.insert_model import generate
from KUN_script.utils import get_hparams_from_file, load_checkpoint
from torch import no_grad, LongTensor
from KUN_script.commons import intersperse
from KUN_script.models import SynthesizerTrn
from KUN_script.text import text_to_sequence

# 加载 hparams
hps = get_hparams_from_file(voice_model_config_path)  # 加载hparams配置文件
print("Loaded hps:", hps)  # 打印hps对象，查看是否包含 symbols
# 加载模型（只加载一次）
model_path = "D:/GitProjects/AI_lesson/blip-image-captioning-base"#替换成你的路径
model = load_model(model_path)

st.title("蔡徐坤给你讲故事")
st.write("拖拽上传图片，查看生成的文本及翻译。")

# 文件上传
uploaded_file = st.file_uploader("上传图片文件", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # 显示上传的图片eix
    image = Image.open(uploaded_file)
    st.image(image, caption="上传的图片", use_column_width=True)

    # 生成文本
    st.write("生成的文本如下：")
    with st.spinner("正在生成文本..."):
        text = img2text(image,model)
    st.success("文本生成完成！")
    st.write(text)

    # 扩展文本
    st.write("扩展后的故事如下：")
    with st.spinner("正在扩展文本..."):
        extended_text = text_extension(text)
    st.success("故事扩展完成！")
    st.write(extended_text)

    # 翻译文本
    st.write("翻译后的文本如下：")
    with st.spinner("正在翻译文本..."):
        translated_text = baidu_api(extended_text, from_lang='en', to_lang='zh')
    st.success("翻译完成！")
    st.write(translated_text)

    # 生成语音
    st.write("生成的语音如下：")
    with st.spinner("正在生成语音..."):
        audio_path = generate(voice_model_path,translated_text, language="ZH")  # 使用语音合成函数
    st.success("语音生成完成！")

    # 播放音频
    st.audio(audio_path, format="audio/wav")
