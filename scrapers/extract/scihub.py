import requests
from bs4 import BeautifulSoup

def extract_scihub(url):
  '''
  Name: extract_scihub
  Description: Takes user url of requested academic paper and find a direct access 
  pdf link from a resource called sci-hub to bypass this. Sci-hub is essentially 
  a pirate website specifically for academic papers, books, etc. 
  Input: 
    @url: url of requested academic paper as string
  Output: string consisting of link/url to direct access pdf of 
  requested academic paper
  '''

  # different scihub domains since some are not always working
  bases = ['sci-hub.tf', 'scihubtw.tw', 'sci-hub.st', 'sci-hub.scihubtw.tw', 'Sci-Hub.tw', 'Sci-hub.se', 'Sci-hub.do', 'sci-hub.ee']
  
  user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
  headers = {'user-agent': user_agent}
  
  #create sci-hub url base for requested paper
  for base in bases:
    try:
      if not url.startswith('http'):
        url = 'https://doi.org/' + url
      else:
        url = 'https://' + base + '/' + url
      
      response = requests.get(url, headers=headers)

      

#     except:
#       pass

  # Get response of sci-hub user requested url page,
  # Then create create soup object of Sci-Hub page.
  # response = requests.get(url)
      soup = BeautifulSoup(response.content, "lxml")

    # Extract PDF link using BeutifulSoup 
  #   try:
        #Scrape sci-hub page for pdf element and address
      link = soup.find("iframe", attrs={"id": "pdf"})['src'].split("#")[0]
      if link.startswith('//'): #scraping path for pdf link in sci-hub html frame
          link = link[2:]
          link = 'https://' + link
      return link
    
    except Exception:
      conitinue
  
  # return link to pdf
#   return link
