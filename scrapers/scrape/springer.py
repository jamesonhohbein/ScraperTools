import pandas as pd
import requests

def scrape_springer(keyword: str, pages: int, year: int):
    #set up query and send the request
    api_key = 'd5a3884a41c429e61ad829e67ba30568'
    url = 'http://api.springernature.com/meta/v2/json?q=subject:' + keyword + '%20type:Journal%20' + 'onlinedatefrom:' + str(year) + \
          '-01-01%20%20onlinedateto:2030-01-01&p=' + str(pages) + '&api_key=' + api_key
    response = requests.get(url)
    json_data = response.json()
    
    #extract the articles fromt the json response
    articles = json_data["records"]

    title = []
    authors = []
    date = []
    link = []
    abstract = []
    journal = []
    meta = []
    link_type = []
    page = []
    publisher = []

    #iterate through article responses and extract all necessary info
    try:
        page_iterator = 0
        for article in articles:
            #extract article url
            try:
                link.append(article['url'][1]['value'])
                link_type.append('Direct')
            except:
                link.append("NA")
                link.append(article['identifier'])
                link_type.append('DOI')
            #extract title
            try:
                title.append(article['title'])
                #print(article['title'])
            except:
                title.append("NA")

            try:
                author_list = []
                #iterate through list of dictionaries with author names
                for i in article['creators']:
                    author_list.append(i['creator'])
                authors.append(author_list)
            except:
                authors.append("NA")

            try:
                journal.append(article['publicationName'])
            except:
                journal.append("NA")

            try:
                publisher.append(article['publisher'])
            except:
                publisher.append("NA")

            try:
                date.append(article['onlineDate'])
            except:
                date.append("NA")

            try:
                abstract.append(article['abstract'])
            except:
                abstract.append("NA")


            meta_dict={}
            try:
                meta_dict['html_link'] = article['url'][0]['value']
            except:
                meta_dict['html_link'] = "NA"

            try:
                meta_dict['doi'] = article['doi']
            except:
                meta_dict['doi'] = "NA"
            
            meta.append(meta_dict)

            page.append(page_iterator // 10)
            page_iterator = page_iterator + 1

    except:
        print("No articles found")

    #create dataframe with all of the above things
    df = pd.DataFrame()
    df['Link'] = link
    df['Link Type'] = link_type
    df['Database'] = 'Springer'
    df['Page'] = page
    df['Title'] = title
    df['Authors'] = authors
    df['Date'] = date
    df['Abstract'] = abstract
    df['Publisher'] = journal
    df['References'] = 'NA'
    df['University'] = 'NA'
    df['Department'] = 'NA'
    df['Citations'] = 'NA'
    df['Related Articles'] = 'NA'
    df['Conclusion'] = 'NA'
    df['Text'] = 'NA'
    df['Meta'] = meta

    return df
