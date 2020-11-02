import pandas as pd
import numpy as np
from scholarly import scholarly, ProxyGenerator

def scrape_scholar(query, pages=0, start_year=0):
  '''  
  Name: scrape_scholar
  Description: Searches Google Scholar using query and returns data for results.
  Input:
  @query: search term
  @pages: number of pages (10 articles per page) to request
  @start_year: minimum number of words in body of text
  @log_path: file path for where to create log file
  Output: A pandas DataFrame with one paper per row
  '''

  pg = ProxyGenerator()
  pg.FreeProxies()
  scholarly.use_proxy(None)

  # initialize list which will contain all article data and be used for DataFrame
  rows = []
  page_size = 10
  maxhits=100 #10 pages

  # the number of the current result being pulled from google scholar
  index = 0

  results = scholarly.search_pubs(query)

  while ((index<maxhits) or (index<page_size*pages)):

      # creates a generator object for results for the query
      result = next(results)

      # retrieves current results object
      curr_result_bib = result.bib

      #instantiates current row container
      row = dict()

      # passes link to article
      if 'eprint' in curr_result_bib:
          URL = curr_result_bib['eprint'] 
          row['Link'] = URL
      elif 'url' in curr_result_bib:
          URL = curr_result_bib['url'] 
          row['Link'] = URL
      else:
          URL = 'NA'
          row['Link'] = 'NA'


      #Link Type - Type: String -The type of link associated with it. 3 types and this will be related to how the specific database delivers its content.
      #Direct - the link is a direct link to the PDF
      #Sci-hub - the link of the paywall that will be inputted into sci-hub.
      #Text - The link is to a webpage that contains the text. Not a pdf, just an html page.
      if (URL.find('.pdf') != -1):
          row['Link Type'] = 'Direct'
      else:
        row['Link Type'] = 'Sci-hub'


      # Database - Type: String - the name of the database this link was retrieved. Google scholar? Arxiv? etc.
      row['Database'] = 'Google Scholar'

      # title of paper, removes quotes at the start and end if there
      row['Title'] = curr_result_bib['title'] if 'title' in curr_result_bib else np.nan

      # page number paper would be on on the website assuming 10 papers per page
      row['Page'] = index//page_size + 1

      # list of [initials last-name]
      row['Authors'] = curr_result_bib['author'] if 'author' in curr_result_bib else np.nan

      # checks published year
      row['Date'] = curr_result_bib['year'] + '-00-00' if 'year' in curr_result_bib else np.nan

      #University - affiliated univeristy/orgmization/company/group,etc. of result
      row['University'] = 'NA'

      #Department - Type: String - The university department this article is associated with. Only include if readily available in the API or website being scraped otherwise "NA" if missing data.
      row['Department'] = 'NA'

      # number of citations
      row['Citations'] = curr_result_bib['cites'] if 'cites' in curr_result_bib else np.nan

      #Related articles - Type: List - The link attatched to the hyperlink "similar articles" on this search result. Only include if readily available in the API or website being scraped otherwise "NA" if missing data.
      row['Related articles'] = 'NA'

      # checks if publisher is available
      row['Publisher'] = curr_result_bib['venue'] if 'venue' in curr_result_bib else np.nan

      #Abstract - Type: String - The string of the abstract attatched of the article. ONLY include this if it is readily available in the API, otherwise leave as "NA"
      row['Abstract'] =  curr_result_bib['abstract'] if 'abstract' in curr_result_bib else np.nan

      #Conclusion - Type: String - The string of the conclusion of the artcile. ONLY include this if it is readily available in the API, otherwise leave as "NA"
      row['Conclusion'] = 'NA'

      #Text - Type: String - The string of the text of the artcile. ONLY include this if it is readily available in the API, otherwise leave as "NA". Most likely, this will be "NA"
      row['Text'] = 'NA'

      #References - Type:List - The list of references this article makes to other literature. ONLY include this if it is readily available in the API, otherwise leave as "NA". If it is available, the list should contain a series of dictonaries with the key title and the key author which should be a string of all authors seperated by a comma. Note the following example.
      row['References'] = 'NA'
      row['Meta'] = 'NA'

      # adds paper data to our dataset
      rows.append(row)
      index += 1


  # replaces all NaN values with "NA"
  df = pd.DataFrame(rows)
  df = df.replace(np.nan, 'NA', regex=True)

  if (start_year!=0):
      size = len(df)
      remove = [0]*size
      for i in range(0,size):
          year = int(df.Date[i][0:4])
          if year<start_year:
              remove[i] = True
          else: 
              remove[i] = False
      df['remove'] = remove
      df  = df[df.remove == False]
      df = df.drop(columns=['remove']).reset_index(drop=True)

  # returns pandas DataFrame where each row is 1 paper
  return df