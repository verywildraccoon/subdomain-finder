import requests
from bs4 import BeautifulSoup
import sys
from urllib.parse import urlparse

not_checked_urls = set()
checked_not_visited_urls = set()
visited_checked_urls = set()
unique_domains = set()

def check_url():
    print(not_checked_urls)
    if len(not_checked_urls) == 0:
        sys.exit("No URLs to check. The set is empty.")
    else:
        for url in not_checked_urls:
            try:
                r = requests.get(url)
                r.raise_for_status()
                print(f"Checking URL... {url} is OK.")
                checked_not_visited_urls.add(url)
            except requests.exceptions.RequestException:
                print("URL is bad.")
    print(f'The following URLs are queued for scraping: {checked_not_visited_urls}')


def extract_matching_domains(domain_keyword):
    for website in checked_not_visited_urls.copy():
        print(f'Scraping the following website: {website}')
        checked_not_visited_urls.remove(website)
        not_checked_urls.remove(website)
        visited_checked_urls.add(website)
        print(f'Added {website} to visited and checked websites.')
        print(f'The following websites are in the list of both visited and checked websites: {visited_checked_urls}')
        print(f'The following websites are in the list of checked but not visited websites: {checked_not_visited_urls}')
        r = requests.get(website)
        soup = BeautifulSoup(r.content, 'html.parser')
        anchor_tags = soup.find_all("a")
        for tag in anchor_tags:
            href = tag.get('href')
            if href and "https://" in href and domain_keyword in urlparse(href).netloc and href not in visited_checked_urls:
                not_checked_urls.add(href)
            if href and href.startswith("/") and href != '/':
                href = website + href
                not_checked_urls.add(href)

def domain_extractor():
    for website in visited_checked_urls:
        domain = urlparse(website).netloc
        cleaned_domain = domain.replace('https://', '').replace('www.', '').replace('http://', '')
        if keyword in cleaned_domain:
            unique_domains.add(cleaned_domain)
    print(f'The scraper identified the following unique domains: {unique_domains}')

url = input("Enter the url you want to scrap: ")
keyword = input("Enter the domain name in a URL to extract: ")
max_depth = int(input("Enter depth search level number: "))

if "https://" not in url:
    url = "https://" + url

not_checked_urls.add(url)
for i in range(max_depth):
    check_url()
    extract_matching_domains(keyword)
domain_extractor()
