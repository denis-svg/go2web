from HTTPRequest import make_https_request
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

class HttpCommand:
    def __init__(self, option) -> None:
        self.option = option
        self.url = None
        self.cache = {}

    def check(self, command):
        command = command.split()
        if len(command) != 2:
            return False
        
        if command[0] != self.option:
            return False
        
        self.url = command[1]
        return True
    
    def response(self):
        if self.url in self.cache:
            cached_entry, cached_time = self.cache[self.url]
            if datetime.now() - cached_time < timedelta(seconds=60 * 60):
                return cached_entry
        try:
            html_page = make_https_request(self.url)
            soup = BeautifulSoup(html_page, 'html.parser')
            title = soup.title.string
            self.cache[self.url] = (title.strip(), datetime.now())
            return title.strip()
        except Exception as e:
            return str(e)
