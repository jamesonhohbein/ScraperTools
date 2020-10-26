from pdf import extract_pdf
from scihub import extract_scihub
from html import extract_html
import pandas as pd
import requests
from bs4 import BeautifulSoup
from .. import logger

def extract_text(df):
  '''
  Name: extract_text
  Description: For each paper, get scihub link if not open access and then extract info from pdf
  Input: 
    @df: pandas DataFrame 
  Output: 
    pandas DataFrame with Abstract, Conclusion, Text, Referenes columns filled or 'NA'
  '''

  # create copy of DataFrame
  rows = []

  # set default extractor as pdf
  extractor_fctn = extract_pdf

  # loops through each row in DataFrame
  for row_index, row in df.iterrows():

    fields = ['Abstract', 'Conclusion', 'References', 'Text']

    # checks for fields already filled
    for field in fields:

      if row[field].lower() not in ['na', 'nan']:

        # keeps field the same
        fields.remove(field)

    # set default input as given link
    input = row['Link']

    # if pdf is not available but link exists
    if row['Link Type'].lower() in ['scihub', 'sci-hub', 'doi']:

      try:
        # get scihub link
        input = extract_scihub(row['Link'])

      except:
        logger.debug(f"Could not get sci-hub link for {row['Link']}")

    elif row['Link Type'].lower() == 'text':
      
      try:
        # get webpage HTML
        input = BeautifulSoup(requests.get(row['Link']).content)

      except:
        logger.debug(f"Could not get HTML for {row['Link']}")

      # change extractor to html
      extractor_fctn = extract_html

    # elif row['Link Type'].lower != 'direct':
    #   row[fields] = ['NA'] * len(fields)
    #   rows.append(row)
    #   ## debug
    #   print('LINK MISSING')
    #   continue

    try:
      # extract fields
      row[fields] = extractor_fctn(input)[fields]
      
      logger.debug(f"Extracted fields from {row['Link']}")
      
    except:
      logger.warning(f"Could not extract fields from {row['Link']}")

    # add to rows
    rows.append(row)

  # return rows
  return pd.DataFrame(rows)