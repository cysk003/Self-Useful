#### pip install requests tqdm

import requests
import os
import json
import datetime
import logging
from urllib.parse import urlparse
from tqdm import tqdm
import sys

def setup_logging():
    logging.basicConfig(filename='log.txt', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def download_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.content
    except requests.exceptions.RequestException as e:
        logging.error(f"Error downloading data: {e}")
        return None

def save_to_file(data, filename):
    try:
        with open(filename, 'wb') as f:
            f.write(data)
        return True
    except Exception as e:
        logging.error(f"Failed to save data to file: {filename}, Error: {e}")
        return False

def main():
    setup_logging()
    now = datetime.datetime.now()
    logging.info(f"Script started: {now.strftime('%Y-%m-%d %H:%M:%S')}")

    input_links = input("Enter one or more links to fetch (separated by commas): ").split(',')
    logging.info(f"Input links: {input_links}")

    total_links = len(input_links)
    current_link_count = 0

    for input_link in input_links:
        current_link_count += 1
        print(f"Processing link {current_link_count}/{total_links}: {input_link.strip()}")
        logging.info(f"Processing link {current_link_count}/{total_links}: {input_link.strip()}")

        data = download_data(input_link.strip())
        if not data:
            print("Failed to retrieve data.")
            continue

        try:
            json_data = json.loads(data)
        except json.JSONDecodeError as e:
            logging.error(f"Failed to parse JSON data: {e}")
            continue

        urls = [item["url"] for item in json_data.get("lives", []) if "url" in item]
        if not urls:
            print("No URLs found in the JSON data.")
            continue
        print(f"Extracted URLs from JSON data: {urls}")

        total_urls = len(urls)
        current_url_count = 0
        for url in urls:
            current_url_count += 1

            try:
                print(f"Processing URL {current_url_count}/{total_urls}: {url}")
                sys.stdout.flush()

                response = requests.get(url, stream=True)
                with tqdm.wrapattr(open(os.path.basename(urlparse(url).path), "wb"), "write", miniters=1,
                                   total=int(response.headers.get('content-length', 0)),
                                   desc=f"Processing URL {current_url_count}/{total_urls}",
                                   unit="B", unit_scale=True, unit_divisor=1024) as f:
                    for chunk in response.iter_content(chunk_size=1024):
                        if chunk:
                            f.write(chunk)
                            f.update(len(chunk))
            except Exception as e:
                logging.error(f"Error processing URL {current_url_count}/{total_urls}: {e}")
                continue

    print("All links processed.")

if __name__ == "__main__":
    main()
