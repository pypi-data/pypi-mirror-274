import os
import cv2
import base64
from openai import OpenAI
from w.whisper_openai import whisper_openai
from w.whisper_faster import whisper_faster
from .utils.srt import generate_srt_from_result


def blog(video_path: str, api_key: str, base_url: str = "https://api.openai.com/v1", vision: str = "视频作者",
         whisper_model: str = "api", local_model: str = None, temperature: float = 0.8, output_path: str = None) -> str:
    file_name = os.path.basename(video_path)
    if file_name.split('.')[-1] != "mp4":
        raise TypeError("仅支持对MP4格式的视频文件进行生成！")

    if whisper_model not in ['api', 'faster', 'local']:
        raise ValueError("whisper_model 是非法值，只能是 api 、faster 、local 其中一个！")

    if whisper_model == "local":
        if local_model is None:
            raise ValueError("当你使用本地模型转录时，本地模型路径不允许为空！")

    if output_path is None:
        output_path = os.getcwd().replace("\\", "/")

    blog_directory = os.path.join(output_path, 'blog')
    if not os.path.exists(blog_directory):
        os.makedirs(blog_directory)

    def extract_frames(video_path, output_dir):
        video = cv2.VideoCapture(video_path)
        timestamp = 0
        while True:
            ret, frame = video.read()
            if not ret:
                break
            current_timestamp = video.get(cv2.CAP_PROP_POS_MSEC) / 1000  # 转换为秒
            if int(current_timestamp) > timestamp:
                timestamp = int(current_timestamp)
                cv2.imwrite(f'{output_dir}/frame_{timestamp}.png', frame)
        video.release()

    def openai_api(key, base, model, text, tem, system_message):
        client = OpenAI(api_key=key, base_url=base)
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": text}
            ],
            temperature=tem)
        answer = response.choices[0].message.content
        return answer

    def encode_image(path):
        with open(path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    print("*** AVTB 视频生成博客 ***")

    # 对视频每一秒提取一张视频截图
    print("正在提取视频帧...")
    extract_frames(video_path, blog_directory)
    print("视频帧提取完成！\n")

    # Whisper生成文本
    print("正在处理文本...")
    if whisper_model == "api":
        result = whisper_openai(video_path, api_key, base_url, "whisper-1")
    elif whisper_model == "faster":
        result = whisper_faster(video_path, "tiny", "cpu")
    else:
        result = whisper_faster(video_path, local_model, "cpu")

    # GPT4o生成文章
    text = result['text']
    content = openai_api(api_key, base_url, "gpt-4o",
                         "请你将下面的内容，以" + vision + "的视角，写成一篇文章" + text, temperature,
                         "你是一位写作高手！")
    print("文本处理完成！\n")

    # GPT4o选择适合的图片
    print("正在选择图片...")
    num = len(os.listdir(blog_directory))
    srt_content = generate_srt_from_result(result)
    choose_photos = openai_api(api_key, base_url, "gpt-4o", "现在有一个视频文件，约：" + str(
        num) + "秒，现在它被提取出每秒钟的截图并以frame_1的格式依次命名,即" + str(
        num) + "张图片。现在，请仔细阅读下面的字幕内容，根据下面的srt字幕的内容，返回你认为写一篇关于该字幕的博客的最重要的几个秒数（对应的图片，并仔细检查选择图片名称是否超过，第" + str(
        num) + "张），请你仔细选择最重要的图片，不要太多，因为我将会把这几个图片作为我的博客的图片内容，请给出你认为最重要的几张图片，你的回答只需给出['frame_1'，'frame_30'，'frame_46']这样的list格式！\n字幕内容：" + srt_content,
                               temperature, "你是一位完全听从用户的博客助手！")
    list_result = eval(choose_photos)
    list_result = [item + '.png' for item in list_result]

    all_files = os.listdir(blog_directory)
    for name in list_result:
        if name not in all_files:
            raise EOFError("很抱歉，检测到本次大模型选取的图片有误！我会努力减少这种错误，请重新尝试！")

    for file in all_files:
        if file not in list_result:
            os.remove(os.path.join(blog_directory, file))
    print("图片选择完成！\n")

    # 图片转base64
    print("正在合并最终文章...")
    image_list = [{"type": "text",
                   "text": "请以" + vision + "的视角写一篇基于下面内容的博客，选择你认为重要的图片插入到文章合适的地方，你只需要返回markdown格式代码，文章的排版必须高质量，逻辑清晰、引人入胜。图片尽可能不要相邻，图片从前到后的名称依次为"
                           + str(list_result) + "，文本内容如下：" + content}]
    for i in range(len(list_result)):
        image_path = blog_directory + '/' + list_result[i]
        base64_image = encode_image(image_path)
        image_list.append({
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}",
            }})

    # GPT4o生成博客
    client = OpenAI(api_key=api_key, base_url=base_url)
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": image_list}],
        temperature=temperature
    )
    answer = response.choices[0].message.content
    print("文章已生成完毕！\n" + "文章内容:\n" + answer)

    answer = answer.replace("```markdown\n", "")
    answer = answer.rstrip("`")

    with open(video_path + 'output.md', 'w', encoding='utf-8') as file:
        file.write(answer)

    return answer
