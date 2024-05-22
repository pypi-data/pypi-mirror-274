import os
import subprocess
from openai import OpenAI
from .utils.srt import generate_srt_from_result


def whisper_openai(video_path: str, api_key: str, base_url: str = "https://api.openai.com/v1", model: str = "whisper-1",
                   prompt: str = None, temperature: float = 0.8, srt: float = False, output_path: str = None) -> dict:
    """
    使用 OpenAI API Whisper 接口进行音频转录

    -- 参数

    - **video_path**: 要识别的文件路径，如`D://Chenyme_AAVT/test.mp4`。
    - **api_key**: OpenAI API KEY。
    - **base_url**: OpenAI 代理 URL，默认值为 `https://api.openai.com/v1`。
    - **model**: Whisper 模型，默认值为 `whisper-1`。
    - **prompt**: Whisper 转录提示词，默认值为 `Don’t make each line too long.`。
    - **temperature**: 模型温度，默认值为 `0.8`。
    - **srt**: 是否直接输出 SRT 字幕，默认值为 `False`。
    - **output_path**: SRT 字幕输出位置，如 `D://Chenyme_AAVT/output/`。

    -- 返回值

    - **Dict**: 包含转录结果的字典。

   """

    print("*** OpenAI API 调用模式 ***")
    if base_url != "https://api.openai.com/v1":
        print(f"- 代理已开启，URL：{base_url}\n")
    if prompt is None:
        prompt = "Don’t make each line too long."
    if model not in ["whisper-1", "whisper-2", "whisper-3"]:
        raise ValueError("model 参数只能是‘whisper-1’,'whisper-2','whisper-3'中的一个")
    if output_path is None:
        output_path = os.getcwd().replace("\\", "/")

    path = os.getcwd().replace("\\", "/")
    file_name = os.path.basename(video_path)
    if file_name.split('.')[-1] == "mp4":
        command = f"ffmpeg -i {file_name} -q:a 0 -y -map a output.mp3"
        subprocess.run(command, shell=True, cwd=path)
        video_path = "output.mp3"
    elif file_name.split('.')[-1] == "mp3":
        video_path = video_path
    else:
        raise TypeError("不支持的文件格式，仅支持 mp4、mp3")

    client = OpenAI(api_key=api_key, base_url=base_url)
    audio_file = open(video_path, "rb")
    transcript = client.audio.transcriptions.create(
        model=model,
        file=audio_file,
        response_format="verbose_json",
        timestamp_granularities=["segment"],
        prompt=prompt,
        temperature=temperature
    )
    result = {'text': transcript.text, 'segments': transcript.segments}
    generate_srt_from_result(result)

    if srt is True:
        srt_content = generate_srt_from_result(result)
        with open(output_path + "/original_output.srt", 'w', encoding='utf-8') as srt_file:
            srt_file.write(srt_content)
        print(f"- 原始字幕保存目录：{output_path}\n")

    return result
