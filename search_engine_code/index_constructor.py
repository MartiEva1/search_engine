#needed for CERTIFICATE_VERIFY_FAILED in downloading nltk
import ssl
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context
#####

import nltk
from math import log, log10, sqrt
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from bs4 import BeautifulSoup as bs

def removeHTML(text):
    soup=bs(text,"html.parser")
    return soup.get_text(separator=" ")

#computes and stores into an array the length of each doc
def doc_length(doc_terms,index,n_docs):
    lengths=[]
    for i in range(n_docs):
        docID=i+1
        term_list=doc_terms[docID]
        score=0
        for t in term_list:
            tf=t[1]
            term=t[0]
            df=len(index[term])
            tf_idf=log10(1+tf)*log10(n_docs/df)
            score=score + tf_idf*tf_idf
        length=sqrt(score)
        lengths.append(length)
    return lengths
    

index_file = open("index_file.tsv", 'w')

with open("jobs.tsv", "r") as jobs:
    stop_words = set(stopwords.words('italian')) 
    tokenizer = RegexpTokenizer(r"[a-zA-Z]+")
    stemmer = SnowballStemmer(language='italian')

    index= {}       #dictionary: (term,[postings list]), posting list=[docID,tf],...
    doc_terms={}    #dictionary: (docID, [term,tf])

    doc_ID=0
    for line in jobs:
        doc_ID=doc_ID+1

        #preprocessing
        fields=line.split("\t")

        title=fields[0]
        description=fields[1]
        cleaned_text=removeHTML(description)
        location=fields[2]
        doc_text=title+" "+cleaned_text+" "+location

        tokens = tokenizer.tokenize(doc_text) 
        terms=set()
  
        for w in tokens: 
            if w not in stop_words and len(w)>1: 
                w=w.lower()
                term=stemmer.stem(w)
                
                if (term not in index):
                    index[term]=[[doc_ID,1]]
                else:
                    if (index[term][-1][0]!= doc_ID):
                        index[term].append([doc_ID,1])
                    else:
                        tf=index[term][-1][1]
                        index[term][-1]=[doc_ID,tf+1]
                if (term not in terms):
                    terms.add(term)
        
        doc_terms[doc_ID]=[]
        for t in terms:
            tf=index[t][-1][1]
            doc_terms[doc_ID].append([t,tf])
            
    n_docs=doc_ID
    lengths=doc_length(doc_terms,index,n_docs)     #lengts[doc_ID-1]=length of document doc_ID 

    index_file.write(str(n_docs)+"\n")      #total number of documents 
    len_str="lengths"
    for l in lengths:
        len_str=len_str+"\t"+str(l) 
    index_file.write(len_str+"\n")

    for term, postings_list in sorted(index.items()):
        df = len(postings_list)
        to_write=term+"\t"+str(df)
        for doc_ID in postings_list:
            to_write=to_write+"\t"+str(doc_ID[0])+","+str(doc_ID[1])
        index_file.write(to_write+"\n")

print("Index written on file 'index_file.tsv'")

jobs.close()
index_file.close()