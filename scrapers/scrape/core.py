import pandas as pd
import numpy as np
import requests
import json
# import time

# api key registered at https://core.ac.uk/api-keys/register/
api_key = 'oud4CkzvaGT8fXRnPF5cBQjM3iYObwWZ'

# json.loads(requests.get(f'https://core.ac.uk:443/api-v2/articles/search/blockchain?apiKey={api_key}&doi=true&citations=true&language=en&pageSize=1').content)

def scrape_core(query, pages=0, start_year=0):
    '''
    Name: scrape_core
    Description: Uses CORE API to get papers related to query term
    Input:
    @query: search term
    @pages: number of pages (10 articles per page) to request
    @start_year: minimum number of words in body of text
    @log_path: file path for where to create log file
    Output: A pandas DataFrame with one paper per row
    '''
    # log_path = 'log.txt'
    page_size = 10

    # create log file to write errors to
    # log = open(log_path, 'w+')

    # initialize list which will contain all article data and be used for DataFrame
    rows = []

    if pages == 0:
        page_size = 100

        # sets pages to maximum of 100 which aims to get all results
        pages = 100

    # maximum search results is 100 per request, so if less than 10 pages are requested, we can request them all in one query
    elif pages <= 10:
        pages = 1
        page_size = 10 * pages

    # prevents program from crashes if errors
    try:

        # loops through all page numbers for pages we want to scrape
        for page_number in range(1, pages + 1):

            # pauses 10 seconds between iterations since API only allows 1 batch request every 10 seconds
            # time.sleep(2)

            # add base url to search query
            core_url = 'https://core.ac.uk:443/api-v2/articles/search/' + query

            # structure parameters for requesting
            query_data = {
                'apiKey': api_key,
                'similar': 'true',
                'citations': 'true',
                'language': 'english',  # does not work, but most articles are in english
                'page': page_number,
                'pageSize': page_size,
                'urls': 'true',
            }

            # adds starting year restriction to url if user designated a start year
            if start_year:
                query_data['year'] = f'>{start_year}'

            # makes api request to the url with the parameters
            with requests.get(core_url, params=query_data) as response:

                # if a status not equal to 200 means an error occured or there are no more results to show
                if response.status_code != 200:
                    # log repsonse code
                    # log.write(f'Could not get {core_url}.\nStatus Code: {response.status_code}')
                    # log.write('\n')

                    break

                # turns response into a json dictionary-like object for parsing
                results = json.loads(response.text)

            # print(results['data'][0].keys())

            # loops through each paper in the data returns
            for i, paper in enumerate(results['data']):
                # creates empty container to input data
                row = dict()

                # link to download paper if available
                row['Link'] = paper['downloadUrl'] if paper[
                                                          'downloadUrl'] != '' else 'NA'  # else row['fulltextUrls'] if row['fulltextUrls'] != [] else np.nan

                # title of paper, removes quotes at the start and end if there
                row['Title'] = paper['title'].strip()

                # True if pdf is available, False otherwise
                if bool(paper['repositoryDocument']['pdfStatus']):
                    row['Link Type'] = 'Direct'
                else:
                    row['Link Type'] = "NA"

                # page number paper would be on on the website assuming 10 papers per page
                row['Page'] = (i // 10) + 1

                # list of [last-name, first-name]
                row['Authors'] = paper['authors']

                # checks published year after start_year and not a future year
                row['Date'] = (str(paper['year'])[:4] + "-00-00") if len(str(paper[
                                                                                 'year'])) == 6 else 'NA' # if paper['year'] >= start_year and paper['year'] <= today.year else np.nan

                # number of citations
                # row['Citations'] = len(paper['citations'])

                # links to related articles
                row['Related articles'] = [similarity['url'] for similarity in paper['similarities']]

                # checks if publisher is available
                row['Publisher'] = paper['publisher'] if 'publisher' in paper.keys() != '' else 'NA'
                row['Database'] = "CORE"
                row['University'] = "NA"
                row['Department'] = "NA"
                row['Citations'] = "NA"
                row['Abstract'] = "NA"
                row['Conclusion'] = "NA"
                row['Text'] = "NA"
                row['References'] = "NA"
                row['Meta'] = "NA"


                # adds paper data to our dataset
                rows.append(row)

    # write any errors to log file
    except Exception as e:
        pass

    # returns pandas DataFrame where each row is 1 paper
    return pd.DataFrame(rows)

