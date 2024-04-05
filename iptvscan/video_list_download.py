import requests
import os
import json
from urllib.parse import urlparse
import datetime
import logging

def setup_logging():
    logging.basicConfig(filename='log.txt', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def download_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # 抛出异常，如果请求失败
        return response.content
    except requests.exceptions.RequestException as e:
        logging.error(f"下载数据时发生错误：{e}")
        return None

def save_to_file(data, filename):
    try:
        with open(filename, 'wb') as f:
            f.write(data)
        return True
    except Exception as e:
        logging.error(f"保存数据到文件失败：{filename}, 错误：{e}")
        return False

def main():
    setup_logging()

    # 记录运行时间
    now = datetime.datetime.now()
    logging.info(f"运行时间: {now.strftime('%Y-%m-%d %H:%M:%S')}")

    # 提示用户输入链接
    input_link = input("请输入一个链接进行访问：")
    logging.info(f"输入链接: {input_link}")

    # 获取数据
    logging.info("正在获取数据...")
    data = download_data(input_link)
    if not data:
        logging.info("无法获取数据。")
        return

    # 解析JSON
    try:
        logging.info("正在解析JSON数据...")
        json_data = json.loads(data)
    except json.JSONDecodeError as e:
        logging.error(f"无法解析JSON数据：{e}")
        return

    # 获取所有url
    urls = [item["url"] for item in json_data.get("lives", []) if "url" in item]
    if not urls:
        logging.info("JSON数据中未找到符合条件的URL。")
        return
    logging.info(f"从JSON数据中提取到的URL列表：{urls}")

    # 遍历url，下载数据并保存到本地
    for url in urls:
        try:
            logging.info(f"正在访问链接：{url}")
            response = requests.get(url)
            response.raise_for_status()
            filename = os.path.basename(urlparse(url).path)
            logging.info(f"文件名：{filename}")
            if os.path.exists(filename):
                os.remove(filename)
                logging.info(f"已删除已存在的文件：{filename}")
            if save_to_file(response.content, filename):
                logging.info(f"已保存数据到文件：{filename}")
            else:
                logging.info(f"保存数据到文件失败：{filename}")
        except requests.exceptions.RequestException as e:
            logging.error(f"下载数据时发生错误：{e}")

if __name__ == "__main__":
    main()
