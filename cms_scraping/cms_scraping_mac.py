import requests
import logging
import time

logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(message)s')

def process_item(item):
    vod_name = item.get('vod_name')
    type_name = item.get('type_name')
    vod_play_url = item.get('vod_play_url')
    
    vod_name_with_type = f"[{type_name}] {vod_name}"
    vod_play_url = vod_play_url.replace('$', ',')
    result = f"{vod_name_with_type} {vod_play_url}"

    print(result)
    logging.info(result)

    with open('result.txt', 'a') as file:
        file.write(result + '\n')

def make_request(url, headers):
    try:
        response = requests.get(url, headers=headers, verify=True)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logging.error(f"请求错误: {str(e)}")
        print(f"请求错误: {str(e)}")
    except ValueError as e:
        logging.error(f"数据解析错误: {str(e)}")
        print(f"数据解析错误: {str(e)}")
    except Exception as e:
        logging.error(f"发生未知错误: {str(e)}")
        print(f"发生未知错误: {str(e)}")
    return None

def get_data_from_api(host):
    base_url = f'{host}/api.php/provide/vod/?ac=list&ac=videolist&t=&pg={{}}&h=&ids=&wd='
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'
    }

    try:
        response = make_request(base_url.format(1), headers)
        if response is None:
            return

        pagecount = response.get('pagecount')
        if pagecount is None:
            logging.error("数据中没有'pagecount'键")
            return

        for page in range(1, pagecount + 1):
            url = base_url.format(page)
            response = make_request(url, headers)
            if response is None:
                continue

            vod_list = response.get('list')
            if vod_list is None:
                logging.error("数据中没有'list'键")
                continue

            for item in vod_list:
                process_item(item)

            progress = (page / pagecount) * 100
            print(f"当前进度: {page}/{pagecount} ({progress:.2f}%)")
            time.sleep(5)

    except Exception as e:
        logging.error(f"发生未知错误: {str(e)}")
        print(f"发生未知错误: {str(e)}")

    print("结果已保存在result.txt文件中")

if __name__ == "__main__":
    hosts = {
        1: 'http://www.9191md.me',
        2: 'https://apiyutu.com'
    }

    print("目前支持的主机名选项：")
    for key, value in hosts.items():
        print(f"{key}: {value}")

    choice = input("请输入主机名代号（默认为1）: ")

    host = hosts.get(int(choice), 'http://www.9191md.me')
    get_data_from_api(host)
