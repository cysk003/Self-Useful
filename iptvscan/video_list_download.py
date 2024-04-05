import requests
import os
import json
from urllib.parse import urlparse

def download_data(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.content
        else:
            print(f"Failed to download data from {url}. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error downloading data from {url}: {e}")
        return None

def main():
    # 提示用户输入链接
    input_link = input("请输入一个链接进行访问：")
    
    # 获取数据
    print(f"正在访问链接：{input_link}")
    data = download_data(input_link)
    if not data:
        print("无法获取数据。")
        return

    # 解析JSON
    try:
        json_data = json.loads(data)
    except json.JSONDecodeError as e:
        print(f"无法解析JSON数据：{e}")
        return

    # 获取所有url
    urls = [value for key, value in json_data.items() if key == 'url']
    print(f"从JSON数据中提取到的URL列表：{urls}")
    
    # 遍历url，下载数据并保存到本地
    for url in urls:
        try:
            print(f"正在访问链接：{url}")
            response = requests.get(url)
            if response.status_code == 200:
                # 获取文件名
                filename = os.path.basename(urlparse(url).path)
                print(f"文件名：{filename}")
                # 删除已存在的文件
                if os.path.exists(filename):
                    os.remove(filename)
                    print(f"已删除已存在的文件：{filename}")
                # 保存数据到文件
                with open(filename, 'wb') as f:
                    f.write(response.content)
                print(f"已保存数据到文件：{filename}")
            else:
                print(f"无法下载数据：{url}，状态码：{response.status_code}")
        except Exception as e:
            print(f"下载数据时发生错误：{e}")

if __name__ == "__main__":
    main()
