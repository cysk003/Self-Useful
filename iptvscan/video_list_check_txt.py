# 使用 pip 安装 requests 库，用于进行 HTTP 请求
# pip install requests

# 使用 pip 安装 beautifulsoup4 库，用于解析 HTML 内容
# pip install beautifulsoup4

# 使用 pip 安装 tqdm 库，用于显示处理进度条
# pip install tqdm

# 注：确保在运行代码之前安装了上述依赖。


import requests
import subprocess
import re
from tqdm import tqdm
from urllib.parse import urlparse

def get_last_path_segment(url):
    parsed_url = urlparse(url)
    path_segments = parsed_url.path.split('/')
    last_segment = path_segments[-1] if path_segments[-1] else path_segments[-2]
    return last_segment

def get_video_urls_from_webpage(url):
    response = requests.get(url)
    video_urls = re.findall(r'(https?://[^\s"]+)', response.text)
    return video_urls

def test_video_url(url):
    command = ['ffprobe', '-v', 'error', '-show_entries', 'stream=width,height,avg_frame_rate', '-of', 'default=noprint_wrappers=1', url]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    video_info = {}
    if result.returncode == 0:
        width_match = re.search(r'width=(\d+)', result.stdout)
        height_match = re.search(r'height=(\d+)', result.stdout)
        frame_rate_match = re.search(r'avg_frame_rate=([\d\/]+)', result.stdout)
        if width_match and height_match and frame_rate_match:
            width = int(width_match.group(1))
            height = int(height_match.group(1))
            if width > 0 and height > 0:
                video_info['width'] = width
                video_info['height'] = height
                frame_rate_str = frame_rate_match.group(1)
                frame_rate_parts = frame_rate_str.split('/')
                if len(frame_rate_parts) == 2 and int(frame_rate_parts[1]) != 0:
                    video_info['frame_rate'] = int(frame_rate_parts[0]) / int(frame_rate_parts[1])
                else:
                    video_info['frame_rate'] = None
    return video_info

def process_webpage_content(webpage_content, video_url, video_info, test_success):
    lines = webpage_content.split('\n')
    for i, line in enumerate(lines):
        if video_url in line:
            if test_success:
                resolution = f"[{video_info['width']}x{video_info['height']}]"
                lines[i] = re.sub(re.escape(video_url), f'{resolution}, {video_url}', line)
            else:
                # 在视频信息测试失败时，将 '###' 添加到行的最前边
                lines[i] = f'###{line}'
            break
    modified_content = '\n'.join(lines)
    return modified_content


def main():
    webpage_url = input("请输入要请求的网页URL: ")
    last_segment = get_last_path_segment(webpage_url)
    video_urls = get_video_urls_from_webpage(webpage_url)
    
    if not video_urls:
        print("未找到视频链接。")
        return
    
    print(f"找到以下视频链接：{video_urls}")
    webpage_content = requests.get(webpage_url).text
    
    with tqdm(total=len(video_urls), desc="处理进度", unit="个") as progress_bar:
        for video_url in video_urls:
            video_info = test_video_url(video_url)
            test_success = bool(video_info)
            webpage_content = process_webpage_content(webpage_content, video_url, video_info, test_success)
            progress_bar.update(1)
            progress_bar.set_postfix({"当前链接": video_url})
    
    with open(f"processed_webpage_{last_segment}.txt", "w", encoding="utf-8") as f:
        f.write(webpage_content)
    
    print(f"处理完成，并已保存到 processed_webpage_{last_segment}.txt 文件中。")

if __name__ == "__main__":
    main()
