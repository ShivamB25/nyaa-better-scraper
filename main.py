#!/usr/bin/python
import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import argparse
import time
from flask import Flask, request, jsonify
import logging
import os

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_base_url(url):
    parsed_url = urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    return base_url

def get_rows_from_soup(soup):
    success_rows = soup.find_all('tr', class_='success')
    danger_rows = soup.find_all('tr', class_='danger')
    default_rows = soup.find_all('tr', class_='default')
    rows = success_rows + danger_rows + default_rows
    logging.info(f"Found {len(success_rows)} success rows, {len(danger_rows)} danger rows, and {len(default_rows)} default rows.")
    return rows

def extract_download_links(url, base_url, retries=3):
    headers = {'User-Agent': 'Mozilla/5.0'}
    for attempt in range(retries):
        try:
            logging.info(f"Fetching URL: {url} (Attempt {attempt + 1})")
            response = requests.get(url, headers=headers)
            logging.info(f"HTTP Status Code: {response.status_code}")
            if response.status_code == 200:
                break
        except requests.RequestException as e:
            logging.error(f"Request failed: {e}")
            if attempt < retries - 1:
                logging.info("Retrying...")
                time.sleep(2)
            else:
                logging.error("Max retries reached. Failed to fetch the page.")
                return []
    else:
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    rows = get_rows_from_soup(soup)
    logging.info(f"Total rows found: {len(rows)}")

    download_links = []
    for row in rows:
        try:
            links = row.find_all('td', class_='text-center')[0].find_all('a')
            torrent_link = urljoin(base_url, links[0]['href'])
            download_links.append(torrent_link)
        except IndexError as e:
            logging.error(f"Error processing row: {row}")
            logging.error(f"IndexError: {e}")
        except Exception as e:
            logging.error(f"Unexpected error: {e}")

    return download_links

@app.route('/scrape', methods=['GET'])
def scrape():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "URL parameter is required"}), 400

    base_url = get_base_url(url)
    download_links = extract_download_links(url, base_url)

    if not download_links:
        return jsonify({"error": "No download links found"}), 404

    return jsonify(download_links)

def save_links_to_file(links, file_path):
    with open(file_path, 'w') as file:
        for link in links:
            file.write(link + '\n')
    logging.info(f"Links saved to {file_path}")

def main(url, output_file=None):
    base_url = get_base_url(url)
    logging.info(f"Base URL: {base_url}")
    download_links = extract_download_links(url, base_url)

    if not download_links:
        logging.info("No download links found.")
    else:
        for link in download_links:
            print(link)
        if output_file:
            save_links_to_file(download_links, output_file)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Nyaa Scraper Script')
    parser.add_argument('url', nargs='?', help='URL to scrape')
    parser.add_argument('-o', '--output-file', help='Save links to a file')
    parser.add_argument('--port', type=int, default=int(os.getenv('PORT', 5000)), help='Port to run the Flask app on')
    args = parser.parse_args()

    if args.url:
        main(args.url, args.output_file)
    else:
        app.run(host='0.0.0.0', port=args.port)