import requests
from requests_html import HTMLSession
import wget
import pathlib

def get_absolute_links(url):
    try:
        session = HTMLSession()
        links = session.get(url).html.absolute_links
        return links
    except Exception as e:
        print(e)
    else:
        links = []

def download(url, filename):
    print(f"Downloading {filename}")
    try:
        wget.download(url, out=filename)
    except Exception as e:
        print(e)

def file_size_in_mb(url):
    response = requests.head(url)
    content_length = response.headers['content-length'].strip()
    size = round(int(content_length) / (1024*1024)) # bytes -> Mb 
    return size

def get_file_name(url):
    filename = wget.detect_filename(url=url).replace(" ", "_").lower() # file name
    return filename


if __name__ == "__main__": 
    FILE_DOWNLOAD_SIZE = 30 # Mb
    path = pathlib.Path.cwd()
    links = get_absolute_links('http://www.msbve.gov.in/msbve/html/samplepaper.htm')
    zip_urls = [link for link in links if link.endswith('.zip')]
    
    for url in zip_urls:
        filename = get_file_name(url)
        size = file_size_in_mb(url)
        file = path / filename
        
        if file.exists():
            print(f"file already exists {filename}")
        else:
            if size > FILE_DOWNLOAD_SIZE: # are you interested in downloading large files ?
                ask = input(f"Do you wish to download {size}mb file? (y/n): ")
                if ask == "y":
                    download(url, filename=filename)
                else:
                    continue
            else:
                    download(url, filename=filename)

    print() # \r + \n
    
