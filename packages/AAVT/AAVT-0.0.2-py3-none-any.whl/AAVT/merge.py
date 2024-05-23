import os
import subprocess


def merge(video_name: str, srt_name: str, output_path: str = None, font: str = "system", font_size: int = 18,
          font_color: str = "HFFFFFF", subtitle_model: str = "硬字幕", quality: str = "medium", crf: int = 23):
    """
    将视频文件与字幕文件合并,支持多种编码器预设以调整编码速度和质量。

    -- 参数

    - **video_name**: 输入视频文件的路径。
    - **srt_name**: 输入字幕文件的路径。
    - **output_path**: 输出视频文件的路径，默认值为当前目录。
    - **font**: 字幕字体名称，默认值为 'system'。
    - **font_size**: 字幕字体大小，默认值为 18。
    - **font_color**: 字幕字体颜色，默认值为 'HFFFFFF'（白色，ASS 格式）。
    - **subtitle_model**: 字幕模式，默认值为 '硬字幕'。
    - **quality**: 编码器预设，默认值为 `medium`。可选值包括：
          - `ultrafast`: 最快的编码速度，但质量最低，文件最大。
          - `superfast`: 非常快的编码速度，质量和文件大小有所提升。
          - `veryfast`: 很快的编码速度，适用于实时编码或需要快速处理的情况。
          - `faster`: 比较快的编码速度，质量进一步提高。
          - `fast`: 快速编码速度，质量较好。
          - `medium`: 默认预设，编码速度和质量的平衡点。
          - `slow`: 较慢的编码速度，输出质量更高，文件更小。
          - `slower`: 更慢的编码速度，质量进一步提高。
          - `veryslow`: 非常慢的编码速度，质量最高，文件最小。
          - `placebo`: 极慢的编码速度，质量微小提升，不推荐使用，除非对质量有极高要求且不在意编码时间。
    - **crf**: 恒定速率因子，CRF 值的范围通常为 0 到 51，数值越低，质量越高。建议值：
          - `0`: 无损压缩，质量最高，文件最大。
          - `18`: 视觉上接近无损，非常高的质量，文件较大。
          - `23`: 默认值，质量和文件大小的平衡点。
          - `28`: 较低的质量，文件较小。

    -- 返回值

    - None
    """

    if output_path is None:
        output_path = os.getcwd().replace("\\", "/")

    def check_cuda_support():
        try:
            result = subprocess.run(["ffmpeg", "-hwaccels"], capture_output=True, text=True)
            return "cuda" in result.stdout
        except Exception as e:
            print(f" GPU 加速不可用，请检查 CUDA 是否配置成功！")
            return False

    cuda_supported = check_cuda_support()

    if subtitle_model == "硬字幕":
        if cuda_supported:
            command = f"""ffmpeg -hwaccel cuda -i {video_name} -lavfi "subtitles={srt_name}:force_style='FontName={font},FontSize={font_size},PrimaryColour=&H{font_color}&,Outline=1,Shadow=0,BackColour=&H9C9C9C&,Bold=-1,Alignment=2'" -preset {quality} -c:v h264_nvenc -crf {crf} -y -c:a copy output.mp4"""
        else:
            command = f"""ffmpeg -i {video_name} -lavfi "subtitles={srt_name}:force_style='FontName={font},FontSize={font_size},PrimaryColour=&H{font_color}&,Outline=1,Shadow=0,BackColour=&H9C9C9C&,Bold=-1,Alignment=2'" -preset {quality} -c:v libx264 -crf {crf} -y -c:a copy output.mp4"""
    else:
        if cuda_supported:
            command = f"""ffmpeg -hwaccel cuda -i {video_name} -i {srt_name} -c:v h264_nvenc -crf {crf} -y -c:a copy -c:s mov_text -preset {quality} output.mp4"""
        else:
            command = f"""ffmpeg -i {video_name} -i {srt_name} -c:v libx264 -crf {crf} -y -c:a copy -c:s mov_text -preset {quality} output.mp4"""

    subprocess.run(command, shell=True, cwd=output_path)

    return None
