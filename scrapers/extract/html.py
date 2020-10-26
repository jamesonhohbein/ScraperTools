from bs4 import BeautifulSoup
import re
import pandas as pd

def k_largest_bodies(soup, t=0, k=None):
  '''
  Name: k_largest_bodies
  Description: Gets largest bodies of text within a BeautifulSoup object 
  Input:
  @soup: BeautifulSoup object
  @t: minimum number of words in body of text
  @k: number of largest bodies of text to return
  Output: A list of the top k longest bodies of text. 
    List may have fewer than k bodies if fewer than k bodies are at least t words.
  '''

  # extracts p tags of paragraphs from soup
  texts = soup.find_all('p')
  
  # check at least 1 paragraph was found
  if texts:

    # if no limit specified
    if k is None:

      # use all paragraphs
      k = len(texts)

    # split each body into a list of words
    texts = [body.text.split(' ') for body in texts]

    # remove whitespace at start and end of each word and any words that are all whitespace
    texts = [[word.strip() for word in body if word.strip() != ''] for body in texts]

    # sorts texts by number of words
    sorted_texts = sorted(texts, key=len, reverse=True)

    # takes the k longest texts from the sorted list or all texts if fewer than k
    k_longest = sorted_texts[:min(k, len(sorted_texts))]

    # returns each of the k longest texts in sentence form with lowercase characters if each is at least t words long
    return [' '.join(body).lower() for body in k_longest if len(body) >= t]

def extract_html(soup):
  '''
  Name: extract_html
  Description: Takes user input of url/link of academic paper 
  where text is on page and extracts relevant information. 
  Input: 
    @soup: bs4 BeautifulSoup object
  Output: abstract, conclusion, references, text
  '''

  # get all strings in soup
  strings = [string for string in soup.stripped_strings]

  abstract = conclusion = text = 'NA'

  references = []
  
  # check strings exists
  if strings:

    for i, string in enumerate(strings[:-1]):

      if re.match(r'(?i)Abstract.*', string.strip()):

        # get next line for abstract
        abstract = strings[i+1]

      elif re.match(r'(?i)(Conclusion(s)|Summary|Discussion).*', string.strip()):

        # get next line for conclusion
        conclusion = strings[i+1]

      # elif re.match(references_pattern, string):
      #   pass# references.append([])

    # combine all paragraphs of at least 100 words for text
    text = ' '.join(k_largest_bodies(soup, t=100))

    # check text exists
    if not text:
      text = 'NA'

  else:
    references = text = 'NA'

  if not references:
    references = 'NA'

  return pd.Series(data=[abstract, conclusion, references, text], index=['Abstract', 'Conclusion', 'References', 'Text'])