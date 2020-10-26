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
  bases = ['scihubtw.tw', 'sci-hub.st', 'sci-hub.scihubtw.tw', 'Sci-Hub.tw', 'Sci-hub.se', 'Sci-hub.do', 'sci-hub.ee']
  
  #create sci-hub url base for requested paper
  for base in bases:
    try:
      if not url.startswith('http'):
        url = 'https://doi.org/' + url
      url = 'https://' + base + '/' + url
      response = requests.get(url)

      ### try putting doi.org/ before doi number
      break

    except:
      pass

  # Get response of sci-hub user requested url page,
  # Then create create soup object of Sci-Hub page.
  # response = requests.get(url)
  soup = BeautifulSoup(response.content, "lxml")

  # Extract PDF link using BeutifulSoup 
  try:
      #Scrape sci-hub page for pdf element and address
      link = soup.find("iframe", attrs={"id": "pdf"})['src'].split("#")[0]
      if link.startswith('//'): #scraping path for pdf link in sci-hub html frame
          link = link[2:]
          link = 'https://' + link
  except Exception:
      return
  
  # return link to pdf
  return link