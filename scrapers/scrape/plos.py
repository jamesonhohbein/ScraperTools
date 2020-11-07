import time
import pandas as pd
import numpy as np
import requests
import json
import re

def scrape_plos(query, pages=0, start_year=1):
    '''  
    Name: scrape_plos
    Description: Uses PLOS API to get papers related to query term from PLOS publisher
    Input:
    @query: search term
    @pages: number of pages (10 articles per page) to request
    @start_year: minimum number of words in body of text
    @log_path: file path for where to create log file
    Output: A pandas DataFrame with one paper per row
    '''

    # api key for accessing the PLOS search API
    api_key = 'dQtKMd9guvwTvzrnG5Pk'

    # prevents program from crashes if errors
    try:
        max_index = pages*10

        # initialize list which will contain all article data and be used for DataFrame
        rows = []

        # initializes counter for keeping track of which row element the search is currently on
        index = 0

        # add base url to search query
        plos_url = 'http://api.plos.org/search'

        # loops through all page numbers for pages we want to scrape
        while (index<max_index or not max_index):

            # pauses 12 seconds between iterations since API only allows 5 batch requests per minute
            time.sleep(12)

            # decrements the start year if a year was provided, and formating to a 4-digit year
            if start_year and isinstance(start_year, int):
                start_year -= 1
                start_year = f'{start_year:04}'


            # structure parameters for requesting
            query_data = {
                'api_key': api_key,
                'q': f'everything:{query} and publication_date:[{start_year}-12-31T23:59:59Z TO *]',
                'fl': 'abstract,conclusions,body,reference,id,title_display,author_display,publication_date,journal,alm_scopusCiteCount,affiliate',
                'rows': f'{min(max_index-index, 1000) or 10}',
                'start': index
            }

            # makes api request to the url with the parameters
            with requests.get(plos_url, params=query_data) as response:

                # if a status not equal to 200 means an error occured or there are no more results to show
                if response.status_code != 200:
                    # log repsonse code
                    log.write(f'Could not get {query}.\nStatus Code: {response.status_code}')
                    log.write('\n')
                    print(f'Could not get {query}.\nStatus Code: {response.status_code}')
                    break

                # turns response into a json dictionary-like object for parsing  
                results = json.loads(response.text)['response']
                
                # if fewer results can be retrived by the search function that were requested, the program will now stop instead at the available number of results
                max_index = min(max_index, results['numFound'])

                # if there was no page limit specified initially, the function will set it to the number of results accessible
                if not max_index:
                    max_index = results['numFound']

                # loops through each paper in the data returns
                for i, paper in enumerate(results['docs']):

                    if 'publication_date' in paper and int(paper['publication_date'][:4]) > int(start_year):

                        # creates empty container to input data
                        row = dict()

                        # link to download paper if available
                        row['Link'] = ('https://journals.plos.org/plosntds/article?id=' + paper['id']) if 'id' in paper else 'NA'
                        row['Link Type'] = 'Text' if 'id' in paper else 'NA'

                        # database this article was retrieved from
                        row['Database'] = 'Plos'

                        # title of paper, removes quotes at the start and end if there
                        row['Title'] = cleanhtml(paper['title_display']) if 'title_display' in paper else 'NA'

                        # page number paper would be on on the website assuming 10 papers per page
                        row['Page'] = (index // 10) + 1

                        # list of full names
                        row['Authors'] = [element for element in paper['author_display']] if 'author_display' in paper else 'NA'

                        # checks published year
                        row['Date'] = paper['publication_date'][:10] if 'publication_date' in paper else 'NA'

                        # checks for university in the affiliations
                        row['University'] = list({next(filter(lambda f: 'University' in f or 'College' in f, element.split(',')[::-1]), 'NA') for element in paper['affiliate']})[0] if 'affiliate' in paper else 'NA'

                        # retrieves list of affiliations for each author
                        row['Department'] = 'NA'

                        # number of citations
                        row['Citations'] = paper['alm_scopusCiteCount'] if 'alm_scopusCiteCount' in paper else 'NA'

                        # links to related articles
                        row['Related articles'] = 'NA'

                        # checks if publisher is available
                        row['Publisher'] = paper['journal'] if 'journal' in paper else 'NA'

                        # returns abstract
                        row['Abstract'] = paper['abstract'][0] if 'abstract' in paper else 'NA'

                        # returns conclusion
                        row['Conclusion'] = paper['conclusions'][0] if 'conclusions' in paper else 'NA'

                        # returns body of paper
                        row['Text'] = paper['body'] if 'body' in paper else 'NA'

                        # list of references
                        row['References'] = [{'Title':element.split(' | ')[2], 'Author':element.split(' | ')[0].replace('\n        ','')} for element in paper['reference']] if 'reference' in paper else 'NA'

                        # adds paper data to our dataset
                        rows.append(row)
                    
                        # increments the index to keep track of where in the search the function is
                        index += 1
    
    # write any errors to log file
    except Exception as e:
        # log = open(log_path + f'{query}.txt', 'w+')
        # log.write(str(e))
        # log.write('\n')
        pass

    # returns pandas DataFrame where each row is 1 paper, and duplicates have been removed
    return pd.DataFrame(rows).drop_duplicates(subset=['Link'])

# function to remove html tags from titles
def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext