from Utils import n_hashes

class MinHash:
    def __init__(self,doc_shs,signatures=None):
        self.doc_shs=doc_shs
        self.signatures=[]
        hashes=n_hashes(100)
        for doc in doc_shs:
            doc_sign=[]
            for i in range(100):
                h=hashes[i]
                minhash=int('0xFFFFFFFFFFFFFFFFFFFF',16)
                for sh in doc:
                    hashed_val=h(str(sh))
                    if(hashed_val<minhash):
                        minhash=hashed_val
                doc_sign.append(minhash)
            self.signatures.append(doc_sign)
    
    def getSignatures(self):
        return self.signatures
                    






