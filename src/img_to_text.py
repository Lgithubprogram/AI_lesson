from PIL import Image
from transformers import pipeline
import os
#考虑到科学上网问题

def load_model(local_model_path = None):
    """
       加载图像到文本模型，可以从本地或在线加载。
    """
    try:
        if local_model_path and os.path.exists(local_model_path):
            #使用本地模型
            return pipeline("image-to-text", model=local_model_path, device=0)
        else:
            #加载在线模型
            return pipeline("image-to-text", model = "Salesforce/blip-image-captioning-base",device=0)
    except Exception as e:
        raise RuntimeError(f"模型加载失败: {e}")

# model_path = "D:/GitProjects/AI_lesson/blip-image-captioning-base"  # 改成你的本地路径
def img2text(url,model):
    """
        将图片转换为文本描述。
    """
    try:
        # 生成文本描述
        text = model(url, max_new_tokens=50)[0]["generated_text"]
        return text
    except Exception as e:
        raise RuntimeError(f"图片转换失败: {e}")
    # img_to_text = load_model(model_path)
    #在线加载
    #img_to_text = pipeline("image-to-text", model = "Salesforce/blip-image-captioning-base",device=0)
    # img = Image.open(url)  # 查看图片是否被打开
    # img.show()  # 展示图片
    #text = img_to_text(url, max_new_tokens=50)[0]["generated_text"]

    # print(text)
    # return text
#   模块测试代码
# if __name__ == "__main__":
#     # 本地模型路径
#     model_path = "D:/GitProjects/AI_lesson/blip-image-captioning-base"
#     # 加载模型
#     img_to_text_model = load_model(local_model_path=model_path)
#
#     # 图片路径
#     image_path = "D:/GitProjects/AI_lesson/test_img/img0.jpg"
#
#     # 调用函数生成文本描述
#     result = img2text(image_path)