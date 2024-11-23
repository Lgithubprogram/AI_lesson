# from transformers import pipeline
# from zhipuai import ZhipuAI
# import requests
# import random
# from hashlib import md5
#
# # 加载图像描述模型
# def img2text(image_file):
#     """
#     将图片转换为描述文本
#     参数:
#         image_file: 上传的图片文件对象 (BytesIO 或文件路径)
#     返回:
#         描述文本 (str)
#     """
#     model = pipeline("image-to-text", model="Salesforce/blip-image-captioning-base", device=0)
#     text = model(image_file, max_new_tokens=50)[0]["generated_text"]
#     return text
#
# def text_extension(text):
#     """
#     扩展文本为故事
#     参数:
#         text: 图片生成的初始文本
#     返回:
#         扩展后的故事文本
#     """
#     client = ZhipuAI(api_key="###")  # 请填写您自己的 API Key
#     response = client.chat.completions.create(
#         model="glm-4-plus",
#         messages=[
#             {"role": "user", "content": "Expand the following sentence into a 300-word story:"},
#             {"role": "assistant", "content": "Please provide the sentence."},
#             {"role": "user", "content": text},
#         ],
#     )
#     extended_text = response.choices[0].message.content
#     return extended_text
#
# def baidu_api(query, from_lang, to_lang):
#     """
#     调用百度翻译 API 翻译文本
#     参数:
#         query: 待翻译的文本
#         from_lang: 源语言 (如 'en')
#         to_lang: 目标语言 (如 'zh')
#     返回:
#         翻译后的文本
#     """
#     appid = '20241112002201004'
#     appkey = 'rRqX2uzmWqLqplMV_M6c'
#
#     endpoint = 'http://api.fanyi.baidu.com'
#     path = '/api/trans/vip/translate'
#     url = endpoint + path
#
#     # 生成签名
#     def make_md5(s, encoding='utf-8'):
#         return md5(s.encode(encoding)).hexdigest()
#
#     salt = random.randint(32768, 65536)
#     sign = make_md5(appid + query + str(salt) + appkey)
#
#     # 请求参数
#     headers = {'Content-Type': 'application/x-www-form-urlencoded'}
#     payload = {'appid': appid, 'q': query, 'from': from_lang, 'to': to_lang, 'salt': salt, 'sign': sign}
#
#     # 发送请求
#     response = requests.post(url, params=payload, headers=headers)
#     result = response.json()
#
#     # 返回翻译结果
#     return result["trans_result"][0]['dst']
import requests
import random
from hashlib import md5

def baidu_api(query, from_lang, to_lang):
    """
    调用百度翻译 API 翻译文本
    :param query: 待翻译的文本
    :param from_lang: 源语言 (如 'en')
    :param to_lang: 目标语言 (如 'zh')
    :return: 翻译后的文本
    """
    appid = '20241112002201004'  # 替换为您的百度翻译 API App ID
    appkey = 'rRqX2uzmWqLqplMV_M6c'  # 替换为您的百度翻译 API Key

    endpoint = 'http://api.fanyi.baidu.com'
    path = '/api/trans/vip/translate'
    url = endpoint + path

    # 生成签名
    def make_md5(s, encoding='utf-8'):
        return md5(s.encode(encoding)).hexdigest()

    salt = random.randint(32768, 65536)
    sign = make_md5(appid + query + str(salt) + appkey)

    # 请求参数
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    payload = {'appid': appid, 'q': query, 'from': from_lang, 'to': to_lang, 'salt': salt, 'sign': sign}

    # 发送请求
    response = requests.post(url, params=payload, headers=headers)
    result = response.json()

    # 返回翻译结果
    return result["trans_result"][0]['dst']

