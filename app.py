import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlsplit
import argparse
import csv
import datetime

now = datetime.datetime.now()
formatted_date = now.strftime("%d%m%y%H%S")

def getHTMLDocument(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        return response.text
    except Exception as e:
        print(f"[-] Error fetching page: {e}")
        return ""

parser = argparse.ArgumentParser(description='Python website scraper.')
parser.add_argument(
    'url', help="The target URL to run asset scans on. e.g: www.example.com"
)
parser.add_argument('--export-to-csv',action='store_true', help="Wheter to export the result into a csv file.")
parser.add_argument('--assets', nargs='+', type=str, help="Add additional assets to list of targetted assets.")
args = parser.parse_args()

args.url = args.url
html_document = getHTMLDocument(args.url)
to_check = ['assets', 'uploads', 'js', 'images', 'backup', 's3', 'sitemap', 'zip', 'sql', 'login', 'admin', 'bug', 'temp', 'ftp', 'php']

if args.assets:
    for arg in args.assets:
        if arg in to_check:
            print(f"{arg} already in lists of assets, skipping...")
            print(f"Full list of assets present: {to_check}")
        else:
            to_check.append(arg)

soup = BeautifulSoup(html_document, 'html.parser')

def security_asset_scanner():
    print(f"[*] Scanning {args.url} for interesting assets...\n")
    
    data_to_csv = []
    fields = ['Key', 'Tag', 'URL']
    extract_hostname = urlsplit(args.url)
    filename = f"{extract_hostname.hostname}-{formatted_date}.csv"
    
    for tag in soup.find_all(lambda t: t.has_attr('href') or t.has_attr('src')):
        raw_link = tag.get('href') or tag.get('src')
        if not raw_link:
            continue
        
        absolute_link = urljoin(args.url, raw_link)
        
        for check in to_check:
            if check in absolute_link.lower():
                row = {
                    'Key': check, 
                    'Tag': tag.name, 
                    'URL': absolute_link
                }
                                    
                data_to_csv.append(row)
                print(f"[FOUND] Key: '{check}' | Tag: <{tag.name}> | URL: {absolute_link}")
    if args.export_to_csv and data_to_csv:
        try:
            with open(filename, 'w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fields)
                writer.writeheader()
                writer.writerows(data_to_csv)
            print(f"\n[+] Exported {len(data_to_csv)} itmes to {filename}")
        except Exception as e:
            print(f"[!] Error writing to CSV: {e}")
    elif args.export_to_csv:
        print("\n[!] No assets found to export")
                
if __name__ == "__main__":
    if html_document:
        security_asset_scanner()
