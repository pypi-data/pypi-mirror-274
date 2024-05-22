def whisper_segments_to_dict(segments):  # 转换dict
    segments = list(segments)
    segments_dict = {
        'text': ' '.join([segment.text for segment in segments]),
        'segments': [{
                'id': segment.id,
                'seek': segment.seek,
                'start': segment.start,
                'end': segment.end,
                'text': segment.text,
                'tokens': segment.tokens,
                'temperature': segment.temperature,
                'avg_logprob': segment.avg_logprob,
                'compression_ratio': segment.compression_ratio,
                'no_speech_prob': segment.no_speech_prob}
            for segment in segments
        ]
    }
    return segments_dict


def milliseconds_to_srt_time_format(milliseconds):  # 将毫秒表示的时间转换为SRT字幕的时间格式
    seconds, milliseconds = divmod(milliseconds, 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"


def generate_srt_from_result(result):  # 将whisper返回内容，格式化为SRT字幕的形式
    segments = result['segments']
    srt_content = ''
    segment_id = 1
    for segment in segments:
        start_time = int(segment['start'] * 1000)
        end_time = int(segment['end'] * 1000)
        text = segment['text']

        index = 30
        words = text.split()
        if len(words) <= 2:
            if len(words) > index:
                text = text[:index] + "\n" + text[index:]
        srt_content += f"{segment_id}\n"
        srt_content += f"{milliseconds_to_srt_time_format(start_time)} --> {milliseconds_to_srt_time_format(end_time)}\n"
        srt_content += f"{text}\n\n"
        segment_id += 1
    return srt_content


def generate_srt_from_result_2(result, font, font_size, font_color):  # 格式化为SRT字幕的形式
    segments = result['segments']
    srt_content = ''
    segment_id = 1
    for segment in segments:
        start_time = int(segment['start'] * 1000)
        end_time = int(segment['end'] * 1000)
        text = segment['text']

        index = 30
        words = text.split()
        if len(words) <= 2:  # "伪"中文检测
            if len(words) > index:
                text = text[:index] + "\n" + text[index:]
        srt_content += f"{segment_id}\n"
        srt_content += f"{milliseconds_to_srt_time_format(start_time)} --> {milliseconds_to_srt_time_format(end_time)}\n"
        srt_content += f"<font color={font_color}><font face={font}><font size={font_size}> {text}\n\n"
        segment_id += 1
    return srt_content

