import pandas as pd
import requests
import json


# WILEY API KEY/ CREDENTIALS
api_key = 'cf5bf9ec-764452a0-66c1ac65-ef5e9789'
email = 'sabelyan@uci.edu'

def wiley(query, year=0, pages=0):

    # initialize list which will contain all article data and be used for DataFrame
    rows = []

    # Wiley uses CrossRef REST API link
    wiley_url = ''
    base = 'https://api.crossref.org/works?query=' + query.replace(' ', '+')
    filter = '&select=DOI,title,URL,issued,author,publisher,is-referenced-by-count,link,abstract'

    # adds starting year restriction to url if user designated a start year
    if year != 0:
        wiley_url = base + '&filter=from-pub-date:' + str(year) + filter
    else:
        wiley_url = base + filter

    # adds number of pages restriction to url if user designated a max page return request
    if ((pages != 0) and (pages < 100)):
        pages = str(pages * 10)  # Each page has 10 results
        wiley_url = wiley_url + '&rows=' + pages
    else:
        wiley_url = wiley_url + '&rows=1000'  # max search results lengh is 1000 hits

    # makes api request to the url with the parameters
    response = requests.get(wiley_url)

    # turns response into a json dictionary-like object for parsing
    results = json.loads(response.text)
    results = results['message']['items']  # extract scrapeable data

    # loops through each result in the data returns to scrape
    for i in range(0, len(results)):

        # creates empty container to input data
        row = dict()

        # URL/DOI of result
        try:
            link = requests.get(results[i]['URL'])
            url = link.url
            del link
            if (url.find('wiley') != -1):  # need final link for wiley links
                url = 'https://api.wiley.com/onlinelibrary/tdm/v1/articles/' + url[url.index('pii/'):len(url)]
            row['Link'] = url
        except:
            try:
                url = results[i]['URL']
                row['Link'] = url
            except:
                url = 'NA'
                row['Link'] = url

        # Link Type 
        if (url.find('.pdf') != -1):
            row['Link Type'] = 'Direct'
        elif ((url.find('publons') != -1) or (url.find('liebertpub') != -1)):
            row['Link Type'] = 'Text'
        else:
            row['Link Type'] = 'Sci-hub'

        # Database
        row['Database'] = 'Wiley/Crossref'

        # Title of result
        try:
            row['Title'] = results[i]['title'][0]
        except:
            row['Title'] = 'NA'

        # Returns page number this result was on (Each page has 10 results)
        row['Page'] = int(i / 10) + 1  # Page 1 is result items 1-9 so offset works

        # Authors 
        author_names = []
        try:
            author = results[i]['author']
            for j in range(0, len(author)):
                name = author[j]
                fullname = name['given'] + ' ' + name['family']
                author_names.append(fullname)
        except:
            author_names = 'NA'
        row['Authors'] = author_names

        # Date
        date = results[i]['issued']['date-parts'][0]
        if (len(date) == 3):
            if (date[1] < 10):
                date[1] = '0' + str(date[1])

            if (date[2] < 10):
                date[2] = '0' + str(date[1])

            row['Date'] = str(date[0]) + '-' + str(date[1]) + '-' + str(date[2])

        elif (len(date) == 2):
            if (date[1] < 10):
                date[1] = '0' + str(date[1])
            row['Date'] = str(date[0]) + '-' + str(date[1]) + '-00'

        elif (len(date) == 1):
            row['Date'] = str(date[0]) + '-00-00'

        else:
            row['Date'] = 'NA'

        # University
        try:
            university = results[i]['author'][0]['affiliation']

            if not university:
                row['University'] = 'NA'

            else:
                university = university[0]['name']
                row['University'] = university

        except:
            row['University'] = 'NA'

        # Department 
        row['Department'] = 'NA'

        # Citations Number 
        try:
            row['Citations'] = results[i]['is-referenced-by-count']
        except:
            row['Publisher'] = 'NA'

        # Related articles 
        row['Related articles'] = 'NA'

        # Publisher
        try:
            row['Publisher'] = results[i]['publisher']
        except:
            row['Publisher'] = 'NA'

        # Abstract
        try:
            row['Abstract'] = results[i]['abstract']
        except:
            row['Abstract'] = 'NA'


        # Conclusion 
        row['Conclusion'] = 'NA'

        # Text 
        row['Text'] = 'NA'

        # References 
        row['References'] = 'NA'

        # appends data to our dataset
        rows.append(row)

    # returns pandas DataFrame where each row is 1 search result
    return pd.DataFrame(rows)
