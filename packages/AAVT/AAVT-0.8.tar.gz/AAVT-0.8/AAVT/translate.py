import os
import time
from openai import OpenAI
from .utils.srt import generate_srt_from_result


def translate(result: dict, api_key: str, base_url: str = None, model: str = None, local: bool = False,
              language: str = None, wait_time: float = None, srt: float = False, output_path: str = None) -> dict:
    """
    使用翻译功能进行文本翻译

    -- 参数

    - **result**: 包含待翻译文本的字典。
    - **api_key**: OpenAI API KEY。
    - **base_url**: API 代理 URL，默认值为 `None`。
    - **model**: 使用的模型名称，默认值为 `None`。
    - **local**: 是否使用本地大模型翻译，默认值为 `False`。
    - **language**: 翻译目标语言，默认值为 `None`。
    - **wait_time**: 每次请求后的等待时间（秒），默认值为 `None`。
    - **srt**: 是否直接输出 SRT 字幕，默认值为 `False`。
    - **output_path**: SRT 字幕输出位置，如 `D://Chenyme-AAVT/output/`，默认值为 `None`。

    -- 返回值

    - **Dict**: 包含翻译结果的字典。
    """

    if output_path is None:
        output_path = os.getcwd().replace("\\", "/")
    if local is True:
        if base_url is None or model is None:
            raise ValueError("Local开启时，将使用本地大模型翻译，必须填写 base_url （模型本地调用端口） 和 model （模型名称）!")
        else:
            print("*** 本地大语言模型 翻译模式 ")
    else:
        print("*** API接口 翻译模式 ***")
        if base_url is None:
            base_url = "https://api.openai.com/v1"
        if model is None:
            model = "gpt-3.5-turbo"
        if language is None:
            language = "中文"
        if wait_time is None:
            wait_time = 0.01

    print(f"- 翻译引擎：{model}")
    if base_url != "https://api.openai.com/v1":
        print(f"代理已开启，URL：{base_url}\n")
    print("- 翻译内容：\n")

    if "gpt" in model:
        client = OpenAI(api_key=api_key, base_url=base_url)
        segment_id = 0
        segments = result['segments']
        for segment in segments:
            text = segment['text']
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a professional translator" },
                    {"role": "user", "content": "Reply directly to " + language + " translation results. Note: Just give the translation results, prohibited to return anything other! Content to be translated: " + str(text)}
                ])
            answer = response.choices[0].message.content
            result['segments'][segment_id]['text'] = answer
            segment_id += 1
            print(answer)
            time.sleep(wait_time)

    else:
        if "moonshot" in model:
            client = OpenAI(api_key=api_key, base_url="https://api.moonshot.cn/v1")
        elif "glm" in model:
            client = OpenAI(api_key=api_key, base_url="https://open.bigmodel.cn/api/paas/v4/")
        elif "deepseek" in model:
            client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com/")
        elif local is True:
            client = OpenAI(api_key=api_key, base_url=base_url)
        segment_id = 0
        segments = result['segments']
        for segment in segments:
            text = segment['text']
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "你是专业的翻译专家"},
                    {"role": "user", "content": "将下面内容的翻译成" + language + "。注意：只需给出翻译后的句子，禁止出现其他任何内容！" + str(text)}
                ])
            answer = response.choices[0].message.content
            result['segments'][segment_id]['text'] = answer
            segment_id += 1
            print(answer)
            time.sleep(wait_time)

        if srt is True:
            srt_content = generate_srt_from_result(result)
            with open(output_path + "/translated_output.srt", 'w', encoding='utf-8') as srt_file:
                srt_file.write(srt_content)
            print(f"\n- 翻译字幕保存目录：{output_path}\n")

    return result
