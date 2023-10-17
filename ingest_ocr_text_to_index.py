from pathlib import Path
from langchain.text_splitter import CharacterTextSplitter
import faiss
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
import pickle


# load data from paths
paths = list(Path("./data").glob("**/*.txt"))
data = []
sources = []
for path in paths:
    sources.append(path)
    with open(path) as file:
        data.append(file.read())

# split text using CharacterTextSplitter
text_splitter = CharacterTextSplitter(chunk_size=1500, separator="\n")
docs = []
metadatas = []
for index, d in enumerate(data):
    splits = text_splitter.split_text(d)
    docs.extend(splits)
    metadatas.extend([{"source": sources[index]}] * len(splits))

# create and store a vector store using FAISS
store = FAISS.from_texts(docs, OpenAIEmbeddings(), metadatas=metadatas)
faiss.write_index(store.index, "./data/docs.index")
store.index = None
with open("./data/faiss_index.pkl", "wb") as file:
    pickle.dump(store, file)
