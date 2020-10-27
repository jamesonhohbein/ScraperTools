from scrapers.scrape.master import master_search

x=master_search('vegetables', 1, 2010, ['arxiv'])

if x:
    x.to_csv('vegetables_arxiv_2010.csv')

else:
    print('could not get x')