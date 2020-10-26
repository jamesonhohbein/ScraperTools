from saveandload import saveCSV
# import alreadyexist

'''
@name caller function
@description loops through rows, extracting labels and triggering master function to gather data, then saves to data bucket
@ params
  startRow - int the starting row of the loop
  endRow - int the end row of the loop
  df - a list of databases for the master function
'''
def caller(startRow,endRow,db,pages=10): 
  df = pd.read_csv('/content/drive/My Drive/Workflow/Labels/Tal List/TAL_list_csv.csv',header=None)

  while startRow <=endRow:

    # extract search term for that row 
    searchTerm = df.loc[startRow,0]

    print('\n\n\n','Starting to scrape',str(db), 'for search term:',searchTerm,'\n\n\n')

    # get dataframe for specific search term 
    st = master_search(searchTerm, pages=pages, year=2010, databases=db)

    print('\n\n\nData gathered for',searchTerm,'   saving to bucket...')
    # save the csv to the data bucket 
    saveCSV(st,searchTerm)


    startRow+=1