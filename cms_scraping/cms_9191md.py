import requests
from tqdm import tqdm
import time

api_url = 'http://www.9191md.me/api.php/provide/vod/'
api_params = {
    'ac': 'list',
    'ac': 'videolist',
    't': '',
    'pg': 1
}

session = requests.Session()

response = session.get(api_url, params=api_params)
if response.status_code == 200:
    data = response.json()
    page_count = data['pagecount']

    with open('movie_links.txt', 'a') as file:
        for page_num in tqdm(range(1, page_count + 1), desc="Processing Pages"):
            api_params['pg'] = page_num

            try:
                response = session.get(api_url, params=api_params)
                response.raise_for_status()

                movie_data = response.json()

                for movie in movie_data['list']:
                    movie_name = movie['vod_name']
                    movie_link = movie['vod_play_url'].split('$')[1]  # 获取播放链接
                    type_name = movie['type_name']

                    file.write(f'[{type_name}]{movie_name}, {movie_link}\n')
                    print(f'【{type_name}】{movie_name}, {movie_link}')

                time.sleep(5)  # 延时5秒
            except Exception as e:
                print(f'获取第 {page_num} 页数据失败: {e}')

    print('所有影片链接已保存到文本文件中')
else:
    print('获取影片列表失败')
