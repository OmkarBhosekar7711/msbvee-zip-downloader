from requests_html import HTMLSession
import wget
import requests
import pathlib
from urllib.error import ContentTooShortError

session = HTMLSession()


res = session.get('http://www.msbve.gov.in/msbve/html/samplepaper.htm').html.absolute_links # Set of urls
path = pathlib.Path.cwd()
    
def format_file(filename):
    whitespace_to_underscore = filename.replace(" ", "_")
    file_name = whitespace_to_underscore.lower() # lower case 
    return file_name

def does_exists(filename):
    file = path / filename
    if not file.exists():
        return True
    else:
        return False

def get_file_size(url):
    response = requests.head(url)
    size = round(
        int(response.headers['content-length'].strip()) / (1024*1024)
    ) # file size in mb default in bytes
    return size

    
for url in res:
    if url.endswith('.zip'):
        file_name = wget.detect_filename(url)
        file = format_file(file_name)
        exists = does_exists(file)
        size = get_file_size(url)
        if exists:
            ask = input(f"Size of [{file}] is [~={size} mb] do you wish to continue? (y/n) default(y): ") or 'y'
            print(ask)
            if ask == 'y':
                try:
                    print(f"\nDownloading {file}[~= {size} mb]")
                    wget.download(url, out=file)
                except ContentTooShortError as error:
                    print("Content Short Error trying again")
                    wget.download(url, out=file)

        else:
            print(f"File [{file}] already exists")
