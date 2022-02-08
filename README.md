# Search_engine and nearest neighbours

## Search_engine
The code is divided into 3 parts:
- web crawler: file simple crawler.py announcement saved in jobs.tsv
-  index construction: file ’index constructor.py’ that pre-processes the documents and builds the inverted index and writes it in the file ’in- dex file.tsv’
-   query processing part: file ’query processing.py’that uses the index in the file to answer the queries

To test the code you first have to launch python3 index constructor.py and then python3 query processing.py.

## Nearest Neighbours with LSH
The implementation of nearest neighbor search is split into different files:
-     ’Utils.py’ contains util functions
-     ’Shingles.py’ the class that given a documents creates the set of hash of the shingles
-     ’MinHash.py’ the class that from the hash of the shingles creates the minhash signatures
-     ’Lsh.py’ the class that implements LSH finding the candidate pairs
-     ’Near duplicates.py’ finds the nearest neighbours computing the Jac-card similarity of the shingle sets.
-      ’p2.py’ the ’main’ program that finds the duplicates with LSH, without LSH and shows the number of duplicate pairs 
        found in both cases, the intersection of the candidate pairs and the time required.

To test the code you have to launch python3 p2.py.

## Nearest Neighbours in Apache Spark
The implementation of nearest neighbor search in Apache spark is in the notebook ’nearest neighbours.ipynb’.
