#!/usr/bin/env python3
import subprocess
import json
import re
import sys

def get_resolution(url):
    try:
        # 使用 ffprobe 获取视频信息
        result = subprocess.check_output(['ffprobe', '-user_agent', 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36', '-timeout', '5000', '-select_streams', 'v', '-show_streams', '-v', 'quiet', '-of', 'json', '-i', url])
        info = json.loads(result.decode('utf-8'))

        # 提取分辨率和帧率
        for stream in info.get('streams', []):
            if stream.get('codec_type') == 'video':
                resolution = (stream.get('width'), stream.get('height'))
                avg_frame_rate = stream.get('avg_frame_rate', 'N/A')
                return resolution, avg_frame_rate
    except Exception as e:
        print(f"Error processing {url}: {e}")
    return None, None

def main(baseurl):
    # 提取起始和结束索引
    match = re.search(r'\[(\d+)-(\d+)\]', baseurl)
    if not match:
        print("Invalid baseurl format. It should contain [start-end]")
        sys.exit(1)
    start, end = map(int, match.groups())

    output_file = "results.txt"
    count = 0
    with open(output_file, 'w') as f:
        # 遍历范围内的视频文件
        for n in range(start, end + 1):
            url = baseurl.replace('[', str(n)).replace(']', '')
            resolution, avg_frame_rate = get_resolution(url)
            if resolution:
                width, height = resolution
                print(f"{n}[{width}x{height}], {url}")
                f.write(f"{n}[{width}x{height}], {url}\n")
            
            # 更新进度
            count += 1
            progress = count * 100 // (end - start + 1)
            print(f"Progress: {progress}%", end='\r')

    print(f"\nResults saved to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <baseurl>")
        sys.exit(1)
    main(sys.argv[1])
