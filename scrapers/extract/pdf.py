import pandas as pd
import re
from tika import parser
from cleantext import clean
import nltk
nltk.download('stopwords')

def extract_pdf(url):
  '''
  Name: extract_pdf
  Description: Takes user input of pdf url/link of academic paper and 
  extracts relevant information. 
  Input: 
  @url: the string of link to pdf of requested academic paper
  Output: abstract, conclusion, references, text
  '''

  # Parse PDF from url
  pdfFile = parser.from_file(url)
  text = pdfFile["content"].strip()

  # do minmal cleaning on text 
  text = clean(text)#,no_line_breaks=True) caused an error
  # print(text)
  abstract = conclusion = references = 'NA'

#   title_author = text.split(re.search('(?i)Abstract', text)[0],1)[0].strip().replace('\n\n', '\n')

  #Get ABSTRACT
  try:
    # Find keyword in text and split to remove leading whitespace after Keyword.
    search = '(?i)Abstract'
    keyword = re.search(search, text)[0]
    post_abstract = text.split(keyword,1)[1].strip()

    # Extract subtring (Abstract) until two newlines detected
    abstract = post_abstract[:post_abstract.index('\n\n')].strip()

  except:
    pass

  #Get CONCLUSION
  try:
    #search parameters for conclusion
    search = '(?i)(Conclusion(s)|Summary|Discussion)'

    keyword = re.search(search,text)[0]

    #split text to after keyword found
    post_conclusion = text.split(keyword,1)[1].strip()

    #index keyword 'refrences in split text containing conclusion(s)
    end = re.search('(?i)(References|Bibliiography|Works Cited|Sources|Citations)',post_conclusion).start()

    #Extract text from 'conclusion' keyword to 'references' keyword.
    conclusion = post_conclusion[:end-1].strip()
    #conclusion = post_conclusion[:post_conclusion.index('\n\n')].strip()
  
  except:
    conclusion = text[-2000:-500]

  #Get CITATIONS and FULL BODY TEXT WITHOUT CITATIONS
  try:
    # list of indicators/key words for the "citations" category 
    search = '(?i)(References|Bibliiography|Works Cited|Sources|Citations)'

    #Find keyword used from list
    keyword = re.search(search,text)[0]

    #Split on keyword and extract everything after match
    citations = text.split(keyword,1)[1].strip()

    #return the full body text of the article without the citations.
    fulltext = text.split(keyword,1)[0].strip() 



    #Create Exception to remove Appendix or Acknowledgemnt section
    if (re.search('(?i)(Appendix|Acknowledgement)',citations)):

      keyword2 = re.search('(?i)(Appendix|Acknowledgement)',citations)[0]

      #citations is between 'citations' keyword and 'appendix; keyword.
      references = references.split(keyword2,1)[0].strip()
  
  except:
    fulltext = text
    references = text[-500:]


  for data in [abstract, conclusion, references, fulltext]:
    if type(data) == str:
      data = data.replace('\n', '')


  references = [references] if references else 'NA'

  return pd.Series(data=[abstract, conclusion, references, text], index=['Abstract', 'Conclusion', 'References', 'Text'])