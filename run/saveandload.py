import pandas as pd 
'''
@Name saveCSV
@Description saves a dataframe according to the given search term. 
  Will combine dataframes that already exist in the data bucket, and remove duplicates
@params
  df - the dataframe
  name - the search term/label
'''
def saveCSV(df,name):

  oldDf = loadCSV(name)

  # load the old dataframe and save it on top of it 
  if isinstance(oldDf,pd.DataFrame):
    #combine frames
    df = pd.concat([df,oldDf],ignore_index=True)

    #drop duplicates according to title 
    df.drop_duplicates(subset=['Title'])
    print('Data for',name,'already exists in the bucket, we are adding the data accordingly...')

  df.to_csv('/content/drive/My Drive/Workflow/Data Bucket/'+name+'.csv')
  print("Dataframe has been saved in the data bucket")

'''
@name loadCSV
@Description simply loads in a dataframe from the data bucket 
@Params 
  name- the label
'''
def loadCSV(name):
  try:
    return pd.read_csv('/content/drive/My Drive/Workflow/Data Bucket/'+name+'.csv',index_col=0)
  except:
    return None 