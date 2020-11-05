from .. import logger
from scrapers.extract.text import extract_text
from scrapers.scrape.arxiv import scrape_arxiv
from scrapers.scrape.core import scrape_core
from scrapers.scrape.scholar import scrape_scholar
from scrapers.scrape.springer import scrape_springer
from scrapers.scrape.ieee import scrape_ieee
import pandas as pd

db_fctns = {
    'core': scrape_core,
            # 'elsevier': scrape_elsevier,
            'arxiv': scrape_arxiv,
            # 'dpla': scrape_dpla,
            # 'ncbi': scrape_ncbi
            'ieee': scrape_ieee,
            'springer': scrape_springer,
            # 'wiley': scrape_wiley,
            # 'plos': scrape_plos,
            # 'crossref': scrape_crossref,
#             'google': scrape_google,
            'scholar': scrape_scholar
            # 'wikipedia': scrape_wikipedia
            }



def master_search(query, pages=0, year=None, databases=None):
  '''
  Input:
    query: search term
    pages: how many pages to get from each database
    year: start year
    databases: list of databases
  Output:
    pandas DataFrame
  '''

  dfs = []

  # if no database specified
  if databases is None:

    # use all databases 
    databases = db_fctns.keys()

  for database in databases:

    # check database exists
    if database.lower() in db_fctns.keys():

      # get corresponding scraper function
      scraper_fctn = db_fctns[database]

      try:

        # scrape specified database with parameters
        rows = scraper_fctn(query, pages, year)

      except Exception as e:
        print(e, database)
        continue
        # logging.error(f'{e}')

      if len(rows) > 0:
        dfs.append(rows)
        
        #logger.debug(f'Scraped {len(dfs[-1])} articles from {database} for "{query}"')

      #else:
        #logger.warning(f'Could not scrape articles from {database} for "{query}"')

  updated_dfs = []

  for df in dfs:
    
    try:
    
      # update Abstract, Conclusion, References, and Text columns by extracting
      updated_dfs.append(extract_text(df))
      
      logger.debug(f'Extracted text from {len(updated_dfs[-1])} articles from {database} for "{query}"')
    
    except:
      logger.warning(f'Could not extract text from {database} for "{query}"')

  # combine DataFrames
  if len(updated_dfs) > 0:
    
    return pd.concat(updated_dfs)
