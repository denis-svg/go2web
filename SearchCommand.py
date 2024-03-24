from HTTPRequest import make_https_request
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
from datetime import datetime, timedelta

class SearchCommand:
    def __init__(self, option) -> None:
        self.option = option
        self.terms = ""
        self.cache = {}

    def check(self, command):
        command = command.split()
        if len(command) < 2:
            return False
        
        if command[0] != self.option:
            return False
        
        self.terms = ""
        for i in range(1, len(command)):
            self.terms += command[i] + " "
        self.terms.strip()

        return True
    
    def response(self):
        if self.terms in self.cache:
            cached_entry, cached_time = self.cache[self.terms]
            if datetime.now() - cached_time < timedelta(seconds=60 * 60):
                return cached_entry
        try:
            page = 1
            results = 0
            response = ""
            while results < 10:
                search_url = f'https://www.google.com/search?q={quote_plus(self.terms)}&start={(page-1)*10}'
                html_page = make_https_request(search_url)

                search_results = self.extract_google_search_results(html_page)
                for result in search_results:
                    results += 1
                    response += str(results) + "\n" + result['title'] + "\n" + result['link'] + "\n" + result['description'] + "\n" + "----------" + "\n"
                    if results == 10:
                        self.cache[self.terms] = (response, datetime.now())
                        return response
                page += 1
            self.cache[self.terms] = (response, datetime.now())
            return response
        except Exception as e:
            return str(e)
    
    def extract_google_search_results(self, html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        # Find all the search result this div wrapper
        result_divs = soup.find_all('div', class_='Gx5Zad fP1Qef xpd EtOod pkphOe')
        results = []

        for div in result_divs:
            # Only get the organic_results
            if div.find('div', class_='egMi0 kCrYT') is None:
                continue

            # Extracting the title (linked text) from h3
            title = div.find('h3').text
            # Extracting the URL
            link = div.find('a')['href'][7:]
            # Extracting the brief description
            description = div.find('div', class_='BNeawe s3v9rd AP7Wnd').text

            results.append({'title': title, 'link': link, 'description': description})
        
        return results
