#!/usr/bin/env python3
import subprocess
import json
import re
import sys
import logging

logging.basicConfig(level=logging.DEBUG)

def get_resolution(url):
    try:
        result = subprocess.check_output(['ffprobe', '-user_agent', 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36', '-timeout', '5000', '-select_streams', 'v', '-show_streams', '-v', 'quiet', '-of', 'json', '-i', url])
        info = json.loads(result.decode('utf-8'))

        for stream in info['streams']:
            if stream['codec_type'] == 'video':
                resolution = (stream['width'], stream['height'])
                avg_frame_rate = stream.get('avg_frame_rate', 'N/A')
                return resolution, avg_frame_rate
    except subprocess.CalledProcessError as e:
        logging.error(f"ffprobe returned non-zero exit status: {e}")
    except Exception as e:
        logging.error(f"Error processing {url}: {e}")
    return None, None

def process_video(url):
    try:
        resolution, avg_frame_rate = get_resolution(url)
        if resolution:
            width, height = resolution
            logging.info(f"Resolution: {width}x{height}, URL: {url}")
            return f"{width}x{height}, {url}"
    except Exception as e:
        logging.error(f"Error processing {url}: {e}")
    return None

def show_progress(count, total):
    progress = count * 100 // total
    print(f"Progress: {progress}%", end='\r')

def main(baseurl):
    match = re.search(r'\[(\d+)-(\d+)\]', baseurl)
    if not match:
        print("Invalid baseurl format. It should contain [start-end]")
        return

    start, end = map(int, match.groups())

    output_file = "results.txt"
    count = 0
    with open(output_file, 'w') as f:
        for n in range(start, end + 1):
            url = baseurl.replace('[', str(n)).replace(']', '')
            result = process_video(url)
            if result:
                f.write(f"{n}[{result}]\n")
            
            count += 1
            show_progress(count, end - start + 1)

    print(f"\nResults saved to {output_file}")

if __name__ == "__main__":
    baseurl = input("Enter the base URL of the videos: ")
    main(baseurl)
