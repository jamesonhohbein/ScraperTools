import urllib.parse
import requests
import pandas as pd

# IEEE Scrape
ieee_api_key = '8h45hsqv8hkkzzreu9uce5ze'

# IEEE parameters
per_page = 10
max_records = 200


def getAuthors(authors):
    '''
    Name: getAuthors
    Description: parse the authors dictionary, to get the list of authors
    :param authors: the dictionary structure returned by the API
    :return: list of author full names
    '''
    if not authors:
        return "NA"
    
    authorsMap = authors['authors']
    s = []
    for a in authorsMap:
        s.append(a["full_name"])
    return s


def scrape_ieee(search_term, page=0, year=None):
    '''
    Name: scrape_ieee
    Description: Uses IEEE Xplore  API to get papers related to search term
    Input:
    @search_term: keywords to search
    @year: start year only articles published on or after will be returned
    @page: number of articles to request = page * 10
    Output: A pandas DataFrame with one paper per row
    '''

    # initialize list which will contain all article data and be used for DataFrame
    rows = []

    # base URL
    url = 'https://ieeexploreapi.ieee.org/api/v1/search/articles'

    # structure parameters for request
    query_data = {
        'apikey': ieee_api_key,
        'querytext': urllib.parse.quote_plus(search_term),
        'start_record': 1
    }

    # adds starting year restriction to url if user designated a start year
    if year:
        query_data['start_year'] = year

    try:
        # loop for all the pages
        p = 0;
        bFirst = True
        while bFirst or p < page:
            bFirst = False

            # makes api request to the url built above and names it response
            with requests.get(url, params=query_data, verify=False) as response:
                response.raise_for_status()
                response.encoding= "utf-8"

                # convert results to JSON
                results = response.json()

                # get the total number of results and calculate how many pages
                if page == 0 :
                    page = math.ceil(int(results['total_records']) / per_page)

                # loops through all page numbers for pages we want to scrape
                for paper in results['articles']:
                    row = {}
                    row['Link'] = paper.get('pdf_url', 'NA')
                    row['Link Type'] = 'Direct' # changed from original function
                    row['Database'] = 'IEEE'
                    row['Title'] = paper.get('title', 'NA')
                    row['Page number'] = p + 1
                    row['Authors'] = getAuthors(paper.get('authors', None))
                    row['Date'] = str(paper['publication_year'])+'-00-00' if 'publication_year' in paper else 'NA'
                    row['University'] = "NA"
                    row['Department'] = "NA"
                    row['Citations'] = paper.get('citing_paper_count', 'NA')
                    row['Related articles'] = "NA"
                    row['Publisher'] = paper.get('publisher', 'NA')
                    row['Abstract'] = paper.get('abstract', 'NA')
                    row['Conclusion'] = "NA"
                    row['Text'] = "NA"
                    row['References'] = "NA"
                    row['Meta'] = "NA"
                    rows.append(row)

            # get next page of results
            p = p + 1
            query_data['start_record'] = 1 + per_page * p

    except HTTPError as http_err:
        msg = f'HTTP error occurred: {http_err}'
        print(msg)
    except Exception as err:
        msg = f'Other error occurred: {err}'
        print(msg)

    return pd.DataFrame(rows)
