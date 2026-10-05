from langchain_chroma import Chroma
from ..config import (collection_name, persist_directory, chunk_size, 
                      chunk_overlap, separators, max_spliter_char_number, 
                      md5_path, session_config)
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from .splitter import split_by_heading, format_heading_path
from datetime import datetime
import os
import hashlib

def check_md5(md5_str:str):
    """Check whether the given MD5 string has already been processed
            return False if not processed, True if processed
    """
    if not os.path.exists(md5_path):
        # the file does not exist, so this MD5 has never been processed
        open(md5_path,'w',encoding='utf-8').close()
        return False
    else:
        for line in open(md5_path,'r',encoding='utf-8').readlines():
            line=line.strip()   # strip surrounding spaces and line breaks
            if line == md5_str:
                return True     # already processed
        return False

def save_md5(md5_str:str):
    """Append the given md5 string to the record file"""
    with open(md5_path,'a',encoding="utf-8")as f:
        f.write(md5_str + '\n')

def get_string_md5(input_str:str ,encoding='utf-8'):
    """Convert the given string to its md5 string"""

    # encode the string to bytes
    str_bytes = input_str.encode(encoding=encoding)

    # create the md5 object
    md5_obj =hashlib.md5()      # get the md5 object
    md5_obj.update(str_bytes)   # feed in the bytes to be hashed
    md5_hex=md5_obj.hexdigest() # get the md5 hex string

    return md5_hex


class KnowledgeBaseService(object):
    def __init__(self):
        # create the folder if it does not exist, skip otherwise
        os.makedirs(persist_directory,exist_ok=True)

        self.chroma=Chroma(          # vector store instance, the Chroma vector store object
            collection_name=collection_name,      # collection (table) name
            embedding_function=DashScopeEmbeddings(model="text-embedding-v4"),
            persist_directory=persist_directory,   # local storage folder of the database
        )      # vector store instance, the Chroma vector store object
        self.spliter=RecursiveCharacterTextSplitter(  # text splitter object
            chunk_size=chunk_size,             # max length of a chunk after splitting
            chunk_overlap=chunk_overlap,       # number of overlapping characters between consecutive chunks
            separators=separators,             # symbols that mark natural paragraph boundaries
            length_function=len,                      # use python's built-in len to measure length
        )      # text splitter object

    def split_coarse(self,data:str)->list[tuple[str,dict]]:
        """Coarse-grained split: split by length, return [(chunk, chunk metadata), ...]"""
        if len(data) > max_spliter_char_number:
            knowledge_chunks:list[str]=self.spliter.split_text(data) # keep one type: always a list of strings
        else:
            knowledge_chunks=[data]
        return [(chunk,{"granularity":"coarse"}) for chunk in knowledge_chunks]

    def split_fine(self,data:str)->list[tuple[str,dict]]:
        """Fine-grained split: split by heading, one chunk per section; returns an empty list if the document has no heading structure"""
        chunks=[]
        for titles,body in split_by_heading(data):
            if not titles:
                continue      # body text under no heading is already covered by the coarse pass
            title=format_heading_path(titles)
            chunk_metadata={"granularity":"fine","title":title}
            # prefix every chunk with its heading path so it keeps its context when retrieved alone
            prefix=title + "\n"
            if len(prefix + body) > chunk_size:
                # the section is too long, keep splitting inside it
                chunks.extend((prefix + piece,chunk_metadata) for piece in self.spliter.split_text(body))
            else:
                chunks.append((prefix + body,chunk_metadata))
        return chunks

    def upload_by_str(self,data:str,filename):
        """Embed the given string and store it in the vector database"""
        # first get the md5 of the given string
        md5_hex=get_string_md5(data)
        if check_md5(md5_hex):
            return "[Repeat] 内容已存在知识库"
        # dual pass: coarse chunks keep broad context, fine chunks pinpoint a section by heading
        chunks=self.split_coarse(data) + self.split_fine(data)
        knowledge_chunks:list[str]=[chunk for chunk,_ in chunks] # keep one type: always a list of strings

        metadata={
            "source":filename,
            #2026-3-8 15:43:30
            "create_time":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "operator":"客户",
        }

        self.chroma.add_texts(        # load the content into the vector store
            # iterable-> list \tuple
            knowledge_chunks,
            metadatas=[{**metadata,**chunk_metadata} for _,chunk_metadata in chunks],

        )
        save_md5(md5_hex)
        return "[Success]内容已经成功载入向量库"

if __name__ =='__main__':
    service= KnowledgeBaseService()
    r=service.upload_by_str("流星","testfile")
    print(r)
