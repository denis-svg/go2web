from HTTPRequest import make_https_request
from bs4 import BeautifulSoup

class HttpCommand:
    def __init__(self, option) -> None:
        self.option = option
        self.url = None

    def check(self, command):
        command = command.split()
        if len(command) != 2:
            return False
        
        if command[0] != self.option:
            return False
        
        self.url = command[1]
        return True
    
    def response(self):
        try:
            html_page = make_https_request(self.url)
            soup = BeautifulSoup(html_page, 'html.parser')
            title = soup.title.string
            return title.strip()
        except Exception as e:
            return str(e)
