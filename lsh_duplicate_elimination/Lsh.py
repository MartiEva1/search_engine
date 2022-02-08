from Utils import n_hashes
from collections import defaultdict

class Lsh:
    def __init__(self,signatures,bands,rows,candidate_pairs=None):
        self.signatures=signatures
        #signatures = [[signaturesDoc0],[signaturesDoc1],...]
        self.bands=bands
        self.rows=rows

        hashes=n_hashes(bands)
        all_bands=defaultdict(dict)     #dictionary containing the buckets for each band
        #all_bands={}        
        n=len(signatures)
        for d in range(n):
            doc_sig = signatures[d]
            for i in range(bands):
                h=hashes[i]
                band=""
                for j in range(rows):
                    band=band+str(doc_sig[(i*rows)+j])
                hashed_band=h(band)
                if(all_bands[i].get(hashed_band,0)==0):
                    all_bands[i][hashed_band]=[d+1]       #dict{ 'dictband1': { 'hashvalue1' : [docIDs]}}
                else:
                    all_bands[i][hashed_band].append(d+1) 
        
        candidate_pairs=set()
        for band in all_bands.keys():
            for hashval in all_bands[band].keys():
                near_docs=all_bands[band][hashval]
                for doc1 in near_docs:
                    for doc2 in near_docs:
                        if(doc1<doc2):
                            candidate_pairs.add((doc1,doc2))  #docIDs (docdID1,docID2)
        
        self.candidate_pairs=candidate_pairs
    
    def getCandidates(self):
        return self.candidate_pairs
            

                
