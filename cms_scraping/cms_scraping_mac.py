import requests
import logging

# 设置日志记录
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(message)s')

def get_data_from_api(host):
    base_url = f'{host}/api.php/provide/vod/?ac=list&ac=videolist&t=&pg={{}}&h=&ids=&wd='

    try:
        response = requests.get(base_url.format(1))
        response.raise_for_status()  # 如果请求失败，会抛出异常

        data = response.json()
        pagecount = data.get('pagecount')

        if pagecount is None:
            logging.error("数据中没有'pagecount'键")
            return

        for page in range(1, pagecount + 1):
            url = base_url.format(page)
            response = requests.get(url)
            response.raise_for_status()

            data = response.json()
            vod_list = data.get('list')

            if vod_list is None:
                logging.error("数据中没有'list'键")
                continue

            for item in vod_list:
                vod_name = item.get('vod_name')
                type_name = item.get('type_name')
                vod_play_url = item.get('vod_play_url')
                vod_play_url = vod_play_url.split('$')[-1]

                vod_name_with_type = f"[{type_name}] {vod_name}"
                result = f"{vod_name_with_type},{vod_play_url}"

                print(result)
                logging.info(result)

                with open('result.txt', 'a') as file:
                    file.write(result + '\n')

            progress = (page / pagecount) * 100
            print(f"当前进度: {page}/{pagecount} ({progress:.2f}%)")

    except requests.RequestException as e:
        logging.error(f"请求失败: {str(e)}")
    except (KeyError, ValueError) as e:
        logging.error(f"数据解析错误: {str(e)}")

    print("结果已保存在result.txt文件中")

if __name__ == "__main__":
    host = input("请输入主机名（默认为http://www.9191md.me）: ") or 'http://www.9191md.me'
    get_data_from_api(host)
