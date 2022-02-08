import requests
from urllib.parse import quote, urlparse
from bs4 import BeautifulSoup
from pathlib import Path
from hashlib import sha512
import httplib2

def meta_redirect(url, content):
    soup  = BeautifulSoup(content)

    result=soup.find("meta",attrs={"http-equiv":"Refresh"})
    if result:
        wait,text=result["content"].split(";")
        if text.strip().lower().startswith("url="):
            re_url=text.split('=', maxsplit=1)[-1]
            print(f'root url {url} re url {re_url}, net loc {urlparse(url).netloc}')
            new_url = urllib.parse.urljoin('{uri.scheme}://{uri.netloc}/'.format(uri = urlparse(url)), re_url)
            print(f'new url {new_url}')
            return new_url
    return None

def get_content(url):
    h=httplib2.Http(".cache")

    resp, content = h.request(url,"GET")

    # follow the chain of redirects
    new_url = meta_redirect(url, content)
    while new_url:
        resp, content = h.request(new_url,"GET") 
    return content

class Document:
    
    def __init__(self, url):
        self.url = url
        parsed = urlparse(url)
        ext = ''.join(Path(parsed.path).suffixes)
        Path('./Storage').mkdir(exist_ok=True)
        self.file_name = f"Storage/{sha512(url.encode('utf-8')).hexdigest()}{ext}"

    def get(self):
        if not self.load():
            if not self.download():
                raise FileNotFoundError(self.url)
            else:
                self.persist()
    
    def download(self):
        if not bool(urlparse(self.url).netloc):
            return False #check if absolute path or not
        try:
            self.content = get_content(self.url)
        except Exception as e:
            print(e, "on", self.url)
            return False
        return True
    
    def persist(self):
        #TODO write document content to hard drive

        try:
            with open(self.file_name, 'wb') as f:
                f.write(self.content.encode())
        except Exception as e:
            print(e)
            return False
        return True
            
    def load(self):
        #TODO load content from hard drive, store it in self.content and return True in case of success
        try:
            with open(self.file_name, 'rb') as f:
                self.content = f.read().decode()    
        except:
            return False
        return True