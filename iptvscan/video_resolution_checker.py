import subprocess
import json
import re
from tqdm import tqdm

def get_resolution(url):
    try:
        result = subprocess.check_output(['ffprobe', '-user_agent', 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36', '-timeout', '5000', '-select_streams', 'v', '-show_streams', '-v', 'quiet', '-of', 'json', '-i', url])
        info = json.loads(result.decode('utf-8'))
        for stream in info.get('streams', []):
            if stream.get('codec_type') == 'video':
                width = int(stream.get('width', 0))
                height = int(stream.get('height', 0))
                if width > 0 and height > 0:
                    return width, height, True
        return None, None, False
    except Exception:
        return None, None, False

def process_urls(baseurl):
    match = re.match(r'(.+)\[(\d+)-(\d+)\](.+)', baseurl)
    if not match:
        print("Invalid baseurl format. It should contain [start-end]")
        return

    prefix, start, end, suffix = match.groups()
    start = start.zfill(len(end))
    total_urls = int(end) - int(start) + 1
    success_count = 0
    failure_count = 0

    with open("results.txt", 'w') as f:
        for n in tqdm(range(int(start), int(end) + 1), desc="Processing URLs", total=total_urls):
            url = f"{prefix}{str(n).zfill(len(end))}{suffix}"
            width, height, success = get_resolution(url)
            if success:
                success_count += 1
                video_info = f"{n} [{width}x{height}], {url}"
                print(f"Processed URL {n}/{total_urls} - {video_info}")
                f.write(video_info + "\n")
            else:
                failure_count += 1

    print(f"Results saved to results.txt | Success: {success_count} | Failure: {failure_count}")

if __name__ == "__main__":
    baseurl = input("Enter baseurl: ")
    process_urls(baseurl)
