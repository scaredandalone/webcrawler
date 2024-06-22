import requests
from bs4 import BeautifulSoup
import time
import argparse
from urllib.parse import urljoin

def fetch_page(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return None

def extract_links(base_url, html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    links = []
    for link in soup.find_all('a', href=True):
        href = link['href']
        full_url = urljoin(base_url, href)  # Convert relative URLs to absolute
        if full_url.startswith('http'):
            links.append(full_url)
    return links

def crawl(start_url, max_depth):
    visited = set()
    to_visit = [(start_url, 0)]  # (URL, depth)

    while to_visit:
        current_url, current_depth = to_visit.pop(0)
        if current_depth > max_depth or current_url in visited:
            continue

        print(f"Fetching: {current_url} at depth {current_depth}")
        html_content = fetch_page(current_url)
        if html_content:
            links = extract_links(current_url, html_content)
            to_visit.extend((link, current_depth + 1) for link in links)

        visited.add(current_url)
        time.sleep(0.5) # To avoid hitting the server too frequently, change if you want it to go faster

    return visited

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simple web crawler")
    parser.add_argument('start_url', type=str, help='The starting URL for the web crawler')
    parser.add_argument('max_depth', type=int, help='The maximum depth for the crawler')

    args = parser.parse_args()

    visited_urls = crawl(args.start_url, args.max_depth)
    print("\nVisited URLs:")
    for url in visited_urls:
        print(url)
