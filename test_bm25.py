from rank_bm25 import BM25Okapi

print("BM25 imported successfully!")

corpus = [
    "this is a test".split(),
    "hello world".split()
]

bm25 = BM25Okapi(corpus)

print("BM25 object created successfully!")