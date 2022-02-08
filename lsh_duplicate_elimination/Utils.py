import hashlib
import nltk

#needed for CERTIFICATE_VERIFY_FAILED in downloading nltk
import ssl
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context
#####

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from bs4 import BeautifulSoup as bs

def removeHTML(text):
    soup=bs(text,"html.parser")
    return soup.get_text(separator=" ")

def hashFamily(i):
  resultSize = 8        
  maxLen = 20           
  salt = str(i).zfill(maxLen)[-maxLen:]
  def hashMember(x):
      hexval="0x"+hashlib.sha1((x + salt).encode()).hexdigest()[-resultSize:]
      return int(hexval,16)
  return hashMember

def n_hashes(n):
    hashes=[]
    for i in range(n):
        hashes.append(hashFamily(i+int(n/99)))
    return hashes



def preprocessing(text):
    stop_words = set(stopwords.words('italian')) 
    tokenizer = RegexpTokenizer(r"[a-zA-Z]+")

    fields=text.split("\t")
    description=fields[1]
    cleaned_text=removeHTML(description)
    doc_text=cleaned_text

    tokens = tokenizer.tokenize(doc_text) 

    processed_text=""
    for w in tokens: 
        if w not in stop_words and len(w)>1: 
            term=w.lower()
            processed_text= processed_text + " " + term
    
    return processed_text
