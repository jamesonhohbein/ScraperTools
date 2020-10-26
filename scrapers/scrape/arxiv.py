import urllib.request
import pandas as pd 
from bs4 import BeautifulSoup


from scrapers.run.saveandload import saveCSV
# import alreadyexist




def scrape_arxiv(query,pages=50,year=0):

  # load the old data to check if incoming titles already exist or not 
  # oldDf = loadCSV(query) 
  # oldquery = query

  #no spaces allowed in the api. Uses pluses
  query = query.replace(' ',"+")

  # change to number of results 
  pages = pages*10


  df = pd.DataFrame()

  #initliaze columns
  df['Link'],df['Link Type'],df['Database'],df['Title'],df['Page'],df['Authors'],df['Date'],df['University'],df['Department'],df['Citations'],df['Related articles'],df['Publisher'],df['Abstract'],df['Conclusion'],df['Text'],df['References'],df['Meta'] = 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17

  # call data via arxiv api 
  with urllib.request.urlopen("http://export.arxiv.org/api/query?search_query=all:"+query+"&start=0&max_results="+str(pages)) as url:
    data = url.read()

  # parse data in more readable form 
  text = data.decode('utf-8')
  soup = BeautifulSoup(text,'xml')

  count = 0 

  # split soup amoung ids of results
  for result in str(soup).split('<id>'): 

    # convert back to soup 
    soup = BeautifulSoup(result)

    # pass invalid results
    if len(soup.findAll('author')) == 0:
      continue
    
    try:
      date = soup.published.string.split('T')[0]

      if int(date.split('-')[0]) <year:
        continue
    except:
      date = 'NaN'


    try:
      summary = soup.summary.string.replace('\n',' ')
    except:
      summary = 'NaN'

    authors = []

    for author in soup.findAll('author'):
      try:
        authors.append(author.find('name').string) 
      except:
        authors = 'NaN'

    authors = str(authors)

    try:
      title = soup.title.string.replace('\n',' ')
    except:
      title = 'NaN'

    try:
      link = soup.find(title='pdf')['href']
    except:
      link='NaN'

    try:
      page = int(count/10) +1
    except:
      page = 'NaN'

    try:
      updated = soup.find('updated').string.split("T")[0]
      meta = {
          'updated':updated
      }
      meta = str(meta)
    except:
      meta = 'NaN'

    # defaults 
    linkType = 'Direct'
    Database = 'Arxiv'

    # check to see if the title exists in the old data, if it does, skip to the next 
    # if alreadyExists(title,oldquery,oldDf) == True:
      # continue

    # set to dataframe 
    df.loc[count,'Link'],df.loc[count,'Link Type'],df.loc[count,'Database'],df.loc[count,'Title'],df['Page'],df.loc[count,'Authors'],df.loc[count,'Date'],df.loc[count,'Abstract'],df.loc[count,'Meta'] = link,linkType,Database,title,page,authors,date,summary,meta

    #count rows of dataframe
    count +=1


  return df


