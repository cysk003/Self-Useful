import requests
import logging
import time

logging.basicConfig(level=logging.INFO)

BASE_URLS = {
    '1': 'http://www.9191md.me/api.php/provide/vod/?ac=list&ac=videolist&t=&pg=',
    '2': 'https://apiyutu.com/api.php/provide/vod/?ac=list&ac=videolist&t=&pg='
}

def fetch_data(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logging.error(f"无法从 {url} 获取数据：{e}")
        return None

def process_data(data, output_file):
    if not data:
        return

    with open(output_file, 'a', encoding='utf-8') as f:
        for item in data.get('list', []):
            vod_name = item.get('vod_name', 'N/A')
            type_name = item.get('type_name', 'N/A')
            vod_play_url = item.get('vod_play_url', 'N/A').replace('$', ',')

            output_str = f"[{type_name}] {vod_name} {vod_play_url}"
            print(output_str)
            f.write(output_str + '\n')

    return data.get('pagecount', 0)

def get_base_url():
    print("请选择基础URL：")
    for key, value in BASE_URLS.items():
        print(f"{key}. {value}")

    choice = input("请输入您的选择 (1 或 2): ")
    return BASE_URLS.get(choice, BASE_URLS['1'])

def main():
    base_url = get_base_url()
    page_num = 1
    max_retries = 3
    retries = 0
    output_file = 'output.txt'

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('')  # 清空文件内容，准备写入新数据

    while retries < max_retries:
        url = f"{base_url}{page_num}"
        data = fetch_data(url)

        if data:
            pagecount = process_data(data, output_file)
            if pagecount and page_num < pagecount:
                page_num += 1
            else:
                break
        else:
            retries += 1
            logging.warning(f"第 {retries} 次尝试获取数据失败")
        
        time.sleep(5)  # 每次请求后延时5秒钟

        # 打印当前处理的页数
        logging.info(f"已处理页数：{page_num}/{pagecount}")

    else:
        logging.error("达到最大重试次数，停止尝试获取数据")

if __name__ == "__main__":
    main()
