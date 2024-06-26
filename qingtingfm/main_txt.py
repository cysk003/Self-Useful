import requests
import json
import math
import urllib.parse


class QingtingFM(object):
    def __init__(self, username, password):
        self.username = urllib.parse.quote_plus(username)
        self.password = urllib.parse.quote_plus(password)

    def get_category_channels(self):
        categories_url = 'http://rapi.qingting.fm/categories?type=channel'
        response = requests.get(categories_url)
        categories = json.loads(response.text)['Data']
        return categories

    def parse_channel_data(self, channel_data, category_title):
        channels = []
        for data in channel_data:
            try:
                title = data['title']
                description = data.get('description', 'null')
            except KeyError:
                description = 'null'
            address = f'http://lhttp.qingting.fm/live/{data["content_id"]}/64k.mp3'
            channels.append({
                'Title': title,
                'Description': description,
                'Address': address,
                'Category': category_title
            })
        return channels

    def start(self):
        channels_by_category = {}
        total_channels = 0
        categories = self.get_category_channels()
        for category in categories:
            category_title = category['title']
            category_id = category['id']
            channels_url = f'http://rapi.qingting.fm/categories/{category_id}/channels?with_total=true'
            response = requests.get(channels_url)
            data = json.loads(response.text)['Data']
            total_channels += data['total']
            channels = []
            for page in range(1, math.ceil(data['total'] / 50) + 1):
                page_url = f'http://rapi.qingting.fm/categories/{category_id}/channels?with_total=true&page={page}&pagesize=50'
                response = requests.get(page_url)
                channel_data = json.loads(response.text)['Data']['items']
                channels.extend(self.parse_channel_data(channel_data, category_title))
            channels_by_category[category_title] = channels

        # 将结果保存为文本文件
        with open('qingtingfm_data.txt', 'w', encoding='utf-8') as f:
            for category_title, channels in channels_by_category.items():
                f.write(f"Category: {category_title}\n")
                for channel in channels:
                    f.write(f"Title: {channel['Title']}, Address: {channel['Address']}\n")
                f.write('\n')

        print('Total channels crawled:', total_channels)
        print('Done')


if __name__ == '__main__':
    qtfm = QingtingFM('qtfm', 'qwe123')
    qtfm.start()
