import os
from faster_whisper import WhisperModel
from .utils.srt import whisper_segments_to_dict
from .utils.srt import generate_srt_from_result


def whisper_faster(file_path: str, model: str, device: str = "cpu", prompt: str = None, lang: str = "auto", beam_size: int = 5,
                   vad: bool = False, min_vad: int = 500, srt: float = False, output_path: str = None) -> dict:
    """
    使用 Faster Whisper 模型进行音频转录

    -- 参数

    - **file_path**: 要识别的音频文件的路径。
    - **model**: Whisper 模型，支持 `tiny`, `tiny.en`, `base`, `base.en`, `small`, `small.en`, `medium`, `medium.en`, `large-v1`, `large-v2`, `large-v3`, `large`, `distil-small.en`, `distil-medium.en`, `distil-large-v2`, `distil-large-v3`。
    - **device**: 运行设备，可以是 `cpu` 或 `cuda`，默认值为 `cpu`。
    - **prompt**: Faster Whisper 提示词，默认值为 `None`。
    - **lang**: 指定语言，`auto` 表示自动检测语言，默认值为 `auto`。
    - **beam_size**: 束搜索宽度，影响解码过程中的候选数量，默认值为 `5`。
    - **vad**: 是否使用声音活动检测，默认值为 `False`。
    - **min_vad**: 声音活动检测的最小持续时间（毫秒），默认值为 `500`。
    - **srt**: 是否直接输出 SRT 字幕，默认值为 `False`。
    - **output_path**: SRT 字幕输出位置，如 `D://Chenyme-AAVT/output/`，默认值为 `None`。

    -- 返回值

    - **Dict**: 包含转录文本和可能的其他信息的字典，或 SRT 字幕文件。

    """

    if model not in ['tiny', 'tiny.en', 'base', 'base.en', 'small', 'small.en', 'medium', 'medium.en', 'large-v1', 'large-v2', 'large-v3', 'large', 'distil-small.en', 'distil-medium.en', 'distil-large-v2', 'distil-large-v3']:
        print("*** Faster Whisper 本地模型加载模式 ***")
    else:
        print("*** Faster Whisper 调用模式 ***")
    print(f"- 运行模型：{model}")
    print(f"- 运行方式：{device}")
    print(f"- VAD辅助：{vad}")
    if device is None:
        device = "cpu"
    if prompt is None:
        prompt = "Don’t make each line too long."
    if output_path is None:
        output_path = os.getcwd().replace("\\", "/")
    if device not in ["cuda", "cpu"]:
        raise ValueError("device 参数只能是 ‘cuda’,'cpu' 中的一个")

    model = WhisperModel(model, device)

    if lang == "auto" and vad is False:
        segments, _ = model.transcribe(file_path,
                                       initial_prompt=prompt,
                                       beam_size=beam_size,
                                       )
    elif lang == "auto" and vad is True:
        segments, _ = model.transcribe(file_path,
                                       initial_prompt=prompt,
                                       beam_size=beam_size,
                                       vad_filter=vad,
                                       vad_parameters=dict(min_silence_duration_ms=min_vad)
                                       )
    elif vad is False:
        segments, _ = model.transcribe(file_path,
                                       initial_prompt=prompt,
                                       language=lang,
                                       beam_size=beam_size,
                                       )
    elif vad is True:
        segments, _ = model.transcribe(file_path,
                                       initial_prompt=prompt,
                                       language=lang,
                                       beam_size=beam_size,
                                       vad_filter=vad,
                                       vad_parameters=dict(min_silence_duration_ms=min_vad)
                                       )
    result = whisper_segments_to_dict(segments)

    if srt is True:
        srt_content = generate_srt_from_result(result)
        with open(output_path + "/original_output.srt", 'w', encoding='utf-8') as srt_file:
            srt_file.write(srt_content)
        print(f"- 原始字幕已保存在：{output_path}\n")

    return result
