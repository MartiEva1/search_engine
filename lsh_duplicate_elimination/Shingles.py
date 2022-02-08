from Utils import hashFamily

class Shingles:
    def __init__(self,k,doc,hashes=None):
        self.k=k
        self.doc=doc
        shingles=set()
        for i in range(len(self.doc)-k+1):
            shingles.add(self.doc[i:i+k])
        hashes=set()
        hash_funct=hashFamily(1234)
        for s in shingles:
            hashes.add(hash_funct(s))
        self.hashes=hashes
    
    def getK(self):
        return self.k
    
    def getShingles(self):
        return self.hashes
    
    def __str__(self):
        tostring=""
        for s in self.hashes:
            tostring=tostring+"; "+str(s)
        return tostring

