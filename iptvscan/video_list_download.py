import requests
import os
import json
from urllib.parse import urlparse
import datetime

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

def save_to_file(data, filename):
    try:
        with open(filename, 'wb') as f:
            f.write(data)
        return True
    except Exception as e:
        print(f"Error saving data to file {filename}: {e}")
        return False

def main():
    # 设置日志文件
    log_file = open("log.txt", "a")
    
    # 记录运行时间
    now = datetime.datetime.now()
    log_file.write(f"运行时间: {now.strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # 提示用户输入链接
    input_link = input("请输入一个链接进行访问：")
    log_file.write(f"输入链接: {input_link}\n")
    
    # 获取数据
    log_file.write("正在获取数据...\n")
    print("正在获取数据...")
    data = download_data(input_link)
    if not data:
        log_file.write("无法获取数据。\n")
        print("无法获取数据。")
        return

    # 解析JSON
    try:
        log_file.write("正在解析JSON数据...\n")
        print("正在解析JSON数据...")
        json_data = json.loads(data)
    except json.JSONDecodeError as e:
        log_file.write(f"无法解析JSON数据：{e}\n")
        print(f"无法解析JSON数据：{e}")
        return

    # 获取所有url
    urls = [item["url"] for item in json_data.get("lives", []) if "url" in item]
    if not urls:
        log_file.write("JSON数据中未找到符合条件的URL。\n")
        print("JSON数据中未找到符合条件的URL。")
        return
    log_file.write(f"从JSON数据中提取到的URL列表：{urls}\n")
    print(f"从JSON数据中提取到的URL列表：{urls}")
    
    # 遍历url，下载数据并保存到本地
    for url in urls:
        try:
            log_file.write(f"正在访问链接：{url}\n")
            print(f"正在访问链接：{url}")
            response = requests.get(url)
            if response.status_code == 200:
                # 获取文件名
                filename = os.path.basename(urlparse(url).path)
                log_file.write(f"文件名：{filename}\n")
                print(f"文件名：{filename}")
                # 删除已存在的文件
                if os.path.exists(filename):
                    os.remove(filename)
                    log_file.write(f"已删除已存在的文件：{filename}\n")
                    print(f"已删除已存在的文件：{filename}")
                # 保存数据到文件
                if save_to_file(response.content, filename):
                    log_file.write(f"已保存数据到文件：{filename}\n")
                    print(f"已保存数据到文件：{filename}")
                else:
                    log_file.write(f"保存数据到文件失败：{filename}\n")
                    print(f"保存数据到文件失败：{filename}")
            else:
                log_file.write(f"无法下载数据：{url}，状态码：{response.status_code}\n")
                print(f"无法下载数据：{url}，状态码：{response.status_code}")
            except Exception as e:
                log_file.write(f"下载数据时发生错误：{e}\n")
                print(f"下载数据时发生错误：{e}")

    # 关闭日志文件
    log_file.close()

if __name__ == "__main__":
    main()
