class Near_duplicates:
    def __init__(self,docs,duplicate_pairs=None):
        self.docs=docs
        n=len(docs)
        duplicate_pairs=set()
        for i in range(n):
            for j in range (n):
                if (i>=j):
                    continue
                else:
                    shingles1=docs[i]
                    shingles2=docs[j]
                    jaccard=len(shingles1.intersection(shingles2))/ len(shingles1.union(shingles2))
                    if(jaccard>=0.8):
                        duplicate_pairs.add((i+1,j+1))
        self.duplicate_pairs=duplicate_pairs
    
    def getDuplicate(self):
        return self.duplicate_pairs
