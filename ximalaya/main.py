import requests
import time
import random
import hashlib
import hmac
import base64
import json

def generate_nonce():
    return ''.join([random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for _ in range(32)])

def generate_timestamp():
    return str(int(time.time() * 1000))

def generate_sig(params):
    sorted_params = sorted(params.items(), key=lambda x: x[0])
    query_string = '&'.join([f"{key}={value}" for key, value in sorted_params])
    query_string_bytes = query_string.encode('utf-8')
    base64_encoded_str = base64.b64encode(query_string_bytes).decode('utf-8')

    app_secret = 'dd7a46b12fe8a304ef17892c89ede22a'
    server_auth_static_key = 'XEbin4wC'
    sha1_key = app_secret + server_auth_static_key
    
    hmac_sha1 = hmac.new(sha1_key.encode('utf-8'), base64_encoded_str.encode('utf-8'), hashlib.sha1)
    hmac_sha1_bytes = hmac_sha1.digest()
    
    sig = hashlib.md5(hmac_sha1_bytes).hexdigest()
    return sig

def get_radio_categories():
    url = 'https://api.ximalaya.com/live/radio_categories'
    nonce = generate_nonce()
    timestamp = generate_timestamp()
    sig_params = {
        'app_key': '99b37417e1185eda1378600593b45c40',
        'client_os_type': '4',
        'nonce': nonce,
        'timestamp': timestamp,
        'server_api_version': '1.0.0',
        'device_id': '32cc6f279c7a11e9a26e0235d2b38928',
        'device_id_type': 'OAID'
    }
    sig_params['sig'] = generate_sig(sig_params)

    response = requests.get(url, params=sig_params)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print("Error:", response.status_code)
        return []

def get_radios_by_category(category_id, page=1):
    url = 'https://api.ximalaya.com/live/get_radios_by_category'
    nonce = generate_nonce()
    timestamp = generate_timestamp()
    sig_params = {
        'app_key': '99b37417e1185eda1378600593b45c40',
        'client_os_type': '4',
        'nonce': nonce,
        'timestamp': timestamp,
        'server_api_version': '1.0.0',
        'device_id': '32cc6f279c7a11e9a26e0235d2b38928',
        'device_id_type': 'OAID',
        'radio_category_id': category_id,
        'page': page
    }
    sig_params['sig'] = generate_sig(sig_params)

    response = requests.get(url, params=sig_params)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print("Error:", response.status_code)
        return {}

def get_all_radios():
    all_radios = []
    categories = get_radio_categories()
    if isinstance(categories, list):
        with open('radios.txt', 'w', encoding='utf-8') as f:
            for category in categories:
                category_name = category.get('radio_category_name', 'Unknown')
                category_id = category.get('id', 'Unknown')
                f.write(f"Category: {category_name} (ID: {category_id})\n")
                print(f"Category: {category_name} (ID: {category_id})")
                radios_response = get_radios_by_category(category_id)
                total_page = radios_response.get('total_page', 1)
                if total_page > 1:
                    for page in range(1, total_page + 1):
                        radios_response = get_radios_by_category(category_id, page=page)
                        radios = radios_response.get('radios', [])
                        for radio in radios:
                            radio_name = radio.get('radio_name', 'Unknown')
                            rate64_aac_url = radio.get('rate64_aac_url', 'Unknown')
                            print(f"Radio Name: {radio_name}, Rate64 AAC URL: {rate64_aac_url}")
                            f.write(f"Radio Name: {radio_name}, Rate64 AAC URL: {rate64_aac_url}\n")
                            all_radios.append({'radio_name': radio_name, 'rate64_aac_url': rate64_aac_url})
                else:
                    radios = radios_response.get('radios', [])
                    for radio in radios:
                        radio_name = radio.get('radio_name', 'Unknown')
                        rate64_aac_url = radio.get('rate64_aac_url', 'Unknown')
                        print(f"Radio Name: {radio_name}, Rate64 AAC URL: {rate64_aac_url}")
                        f.write(f"Radio Name: {radio_name}, Rate64 AAC URL: {rate64_aac_url}\n")
                        all_radios.append({'radio_name': radio_name, 'rate64_aac_url': rate64_aac_url})
    else:
        print("Error: Unexpected data type for categories")
    
    print(f"Total Radios: {len(all_radios)}")
    return all_radios

if __name__ == '__main__':
    get_all_radios()
    print("电台播放URL已保存到文件 radio_urls.txt 中。")
