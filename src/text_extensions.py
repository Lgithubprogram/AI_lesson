from exceptiongroup import print_exception
from zhipuai import ZhipuAI

url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"

def text_extension(text):
    client = ZhipuAI(api_key="b69f0e809e6601a4ca5c9d9407b8ce2b.Nwpl24uMiaVFZ6Im")    # 请填写您自己的APIKey
    response = client.chat.completions.create(
        model="glm-4-plus",  # 请填写您要调用的模型名称
        messages=[
            {"role": "user",
             "content": "I heard that you are a great writer, I will give you a sentence and expand the short story by 100 words"},
            {"role": "assistant", "content": "Of course, please provide your sentences"},
            {"role": "user", "content": text},
        ],
    )
    ex_text = response.choices[0].message.content
    return ex_text
#测试代码
# text = "i am a good boy"
#
# print(
#     text_extension(text)
# )