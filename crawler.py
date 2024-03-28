#crawler example

from html.parser import HTMLParser
from urllib.parse import urljoin
from urllib.request import urlopen 
from re import findall

class Collector(HTMLParser):
    'a crawler that prints the frequency of words in a webpage and the HTTP links found on the webpage'
    def __init__(self, url):
        'setting the constructors'
        HTMLParser.__init__(self)
        self.url = url
        self.links = []
        self.text = ''

    def handle_starttag(self, tag, attrs):
        'looks for the url start tag'
        if tag == 'a':
            for attr in attrs:
                if attr[0] == 'href':
                    absolute = urljoin(self.url, attr[1])
                    if absolute[:4] == 'http':
                        self.links.append(absolute)
    
    def handle_data(self, data):
        'return the concatenated text in the page'
        self.text += data

    def getLinks(self):
        'returns the links'
        return self.links
    
    def getdata(self):
        'returns the text'
        return self.text
    
# build analyzer

class Crawler(object):      
    'crawl links'
    
    def __init__(self):
        'setting the constructors'
        self.visited = set()
        
    def freq(self, content):
        'count the words in the content'
        #dictionary
        dictionary = {}
        
        #populate it with words
        #increment it everytime we see a new word
        pattern = '[a-zA-Z]+'
        words = findall(pattern, content)
        for w in words:
            if w in dictionary:
                dictionary[w] += 1
            else:
                dictionary[w] = 1 
        
        return dictionary
    
  
    def analyze(self, url):
        'return the list of urls found on the page'
        print('\nVisting ', url)
        content = urlopen(url).read().decode()
        collector = Collector(url)
        collector.feed(content)
        urls = collector.getLinks()
        
        content = collector.getdata()
        frequency = self.freq(content)
        print('\n{:50} {:10} {:5}'.format('URL', 'Word', 'Count'))
        
        for word in frequency:
            print('\n{:50} {:10} {:5}'.format(url, word, frequency[word]))
        for link in urls:
            print('\n{:50} {:10}'.format(url, link))
        
        return urls
    
    
    def crawl2(self, url):
        'a recursive web crawler that calls analyze() on every visited web page'
        self.visited.add(url)
        links = self.analyze(url)
        for link in links:
            if link not in self.visited:
                try:
                    self.crawl2(link)
                except:
                    pass
                
                
# test
c = Crawler()
c.crawl2('https://facweb.cdm.depaul.edu/ahecktma/one.html')


