from Utils import hashFamily
from Utils import preprocessing
from Shingles import Shingles
from MinHash import MinHash
from Lsh import Lsh
from Near_duplicates import Near_duplicates
from linecache import getline
import time

start = time.time()
doc_shingles=[]

with open("jobs.tsv", "r") as jobs:
    for line in jobs:
        preprocessed=preprocessing(line)
        s=Shingles(10,preprocessed).getShingles()
        doc_shingles.append(s)
end = time.time()
shingles_time= end - start
print("\n----------- Near duplicates search -----------\n")
print("time to create the shingles: "+str(shingles_time)+" seconds")


print("*--------- Near duplicates with LSH ---------*")
start = time.time()
signatures=MinHash(doc_shingles).getSignatures()
print("[+] MinHashing Done")
end=time.time()
print("time to perfom minhashing: "+str(end-start)+" seconds")

start = time.time()
candidate_pairs=Lsh(signatures,20,5).getCandidates()
print("[+] LSH Done")
end = time.time()
lsh_time= end - start

print("time with LSH: "+str(lsh_time)+" seconds")
print("number of candidate pairs with LSH: "+str(len(candidate_pairs)))


print("*------- Near duplicates with Jaccard on shingle set -------*")
start = time.time()
near_duplicates=Near_duplicates(doc_shingles).getDuplicate()
end = time.time()
jac_time= end - start
print("time without LSH: "+str(jac_time)+" seconds")

print("number of candidate pairs without LSH: "+str(len(near_duplicates)))
intersection=near_duplicates.intersection(candidate_pairs)
print("number of pairs in the intersection between the results: "+str(len(intersection)))








