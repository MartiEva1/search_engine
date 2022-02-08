#needed for CERTIFICATE_VERIFY_FAILED in downloading nltk
import ssl
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context
#####

from math import log10, sqrt
from linecache import getline
import nltk
import heapq

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer

##---------------- UTILS: functions ----------------##

#merge between 2 posting lists
def intersect2lists(p1,p2):
    answer=[]
    i1=0
    i2=0
    while(i1 < len(p1) and i2<len(p2)):
        if(p1[i1][0]==p2[i2][0]):   #doc_ID1==doc_ID2
            answer.append([p1[i1][0]])    #doc_id
            i1=i1+1
            i2=i2+1
        elif(p1[i1][0]<p2[i2][0]):
            i1=i1+1
        else:
            i2=i2+1
    return answer

#merge between ALL postings
def boolean_search(query_terms,index):
    j=0
    n_query=len(query_terms)
    exception=True
    answer=[]
    while(exception):
        try: 
            answer=index[query_terms[j]][1:]
            exception=False
        except:
            j=j+1
            if(j>n_query):
                answer=[]
                return answer
    for i in range(j+1,len(query_terms)):
        try:
            index[query_terms[i]]
            answer=intersect2lists(answer,index[query_terms[i]][1:])
        except:
            continue
    docs=[]
    for val in answer:
        docs.append(val[0])
    return docs

#union between 2 postings
def union2lists(p1,p2):
    answer=[]
    i1=0
    i2=0
    while(i1 < len(p1) and i2<len(p2)):
        if(p1[i1][0]==p2[i2][0]):   #doc_ID1==doc_ID2
            answer.append([p1[i1][0]])    #doc_id
            i1=i1+1
            i2=i2+1
        elif(p1[i1][0]<p2[i2][0]):
            answer.append([p1[i1][0]])
            i1=i1+1
        else:
            answer.append([p2[i2][0]])
            i2=i2+1
    
    #if one list terminated and the other not
    while(i1 < len(p1)):
        answer.append([p1[i1][0]])
        i1=i1+1
    while(i2 < len(p2)):
        answer.append([p2[i2][0]])
        i2=i2+1 
    return answer

#return all docs with AT LEAST one query term
def union_search(query_terms,index):
    j=0
    n_query=len(query_terms)
    exception=True
    answer=[]
    while(exception):
        try: 
            answer=index[query_terms[j]][1:]
            exception=False
        except:
            j=j+1
            if(j>n_query):
                answer=[]
                return answer
    for i in range(j+1,len(query_terms)):
        try:
            index[query_terms[i]]
            answer=union2lists(answer,index[query_terms[i]][1:])
        except:
            continue
    docs=[]
    for val in answer:
        docs.append(val[0])
    return docs


def search(query_terms, index, bool):
    if(bool):
        #AND of docIDs (docs containing all terms)
        return boolean_search(query_terms,index)
    else:
        #OR of docIDs (docs containing at least one term)
        return union_search(query_terms,index)

#computes query length
def query_len(query_terms,index,docs):
    score=0
    for term, occ in query_terms.items():
        try:
            tf_idf=log10(occ + 1)*log10(docs/index[term][0][0])
            score=score + tf_idf*tf_idf
        except:
            #term not in the index
            continue
    return sqrt(score)

        
#cosine similarity scores computation
def cos_sim(query_terms,index,n_docs,docs,query_len):
    scores={}
    for term, occ in query_terms.items():
        w_tq=log10(1+int(occ))
        df=0
        try:
            df=int(index[term][0][0])
        except:
            continue

        for posting in index[term][1:]:
            doc_id=posting[0]
            tf=posting[1]
            if doc_id not in docs:
                continue
            w_td=log10(1+int(tf))
            idf=log10(n_docs/df)
            scores[doc_id]=scores.get(doc_id,0) + float(w_td * idf * w_tq * idf)   
    
    for doc in scores.keys():
        scores[doc]=scores[doc] /(float(lengths[doc-1])*query_len)     

    return scores

def top_k(scores,k):
    l=0
    heap=[]
    for docID,score in scores.items():
        if(l<k):
            heapq.heappush(heap,(score,docID))
            l=l+1
        elif(score>=heap[0][0]):
            heapq.heappushpop(heap,(score,docID))

    sorted_docs=heapq.nlargest(k,heap)
    return sorted_docs


#loading the index from the file
def load_index():
    index= {}     #dictionary: (term,[postings list]), posting list=[docID,tf], posting list[0]=[df,0]
    with open("index_file.tsv", "r") as index_file:
        n_docs=0
        lengths=[]
        l=0
        for line in index_file:
            if(l==0):
                n_docs=int(line) #total number of documents
                l=l+1
                continue
            if(l==1):
                lengths=line.split("\t")[1:]
                l=l+1
                continue

            fields=line.split("\t")
            term=fields[0]
            df=int(fields[1])
            index[term]=[[df,0]]
            for i in range(2,2+df):
                posting=fields[i].split(",")
                doc_ID=int(posting[0])
                tf=int(posting[1])
                index[term].append([doc_ID,tf])    
    return index, lengths, n_docs

##---------------- MAIN ----------------##        

index, lengths, n_docs = load_index()  

#query processing
stop_words = set(stopwords.words('italian')) 
stemmer = SnowballStemmer(language='italian')
tokenizer = RegexpTokenizer(r"[a-zA-Z]+")

print(" ____________________________")
print("|                            |")
print("| Eva's simple search engine |")
print("|____________________________|")
print("This is a simple search engine for kijiji jobs announcements, \n feel free to insert queries or type 'q' if you want to quit \n Enjoy! =) \n")
while(1):
    query=input("What are you looking for? ")
    if(query=='q'):
        print("Bye, have a nice day!")
        break

    tokens = tokenizer.tokenize(query)
    query_terms={}
    for w in tokens: 
        if w not in stop_words and len(w)>1: 
            w=w.lower()
            term=stemmer.stem(w)
            if term not in query_terms:
                query_terms[term]=1
            else:
                occ=query_terms[term]
                query_terms[term]=occ+1
    

    keys=list(query_terms.keys())
    query_length=query_len(query_terms,index,n_docs)
    
    #docs=search(keys,index, True)      #if you want to test the search engine in boolean search (true)
    docs=search(keys,index, False)

    scored_docs=cos_sim(query_terms,index,n_docs,docs,query_length) 
    top_10=top_k(scored_docs,10)

    #results
    results=len(top_10)
    if(results==0):
        print("Sorry, there is NO Document matching your query, try with another formulation!")
    else:
        print(str(len(docs))+" results found, showing the TOP-10:")
    
    for i in range(results):
        doc=top_10[i][1]
        score=top_10[i][0]
        print("------------------------------------")
        print(str(i+1)+". doc_ID: "+str(doc)+" score:"+"{0:.3f}".format(score))
        print(getline("jobs.tsv",doc))
        print("------------------------------------")





    

    
    
