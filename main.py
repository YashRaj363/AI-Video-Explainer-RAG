from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings,ChatOllama
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser


loader=TextLoader("transcript.txt",encoding='utf-8')

docs=loader.load()

splitter=RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

chunks=splitter.split_documents(docs)


#print(chunks[0].page_content)

llm_embedding= OllamaEmbeddings(
    model="embeddinggemma:latest"
)

vector_store=FAISS.from_documents(
    embedding=llm_embedding,
    documents=chunks
)


retriever=vector_store.as_retriever(search_kwargs={"k":4})

llm=ChatOllama(
    model="qwen2.5:3b",
    temperature=0.7
)

template1=PromptTemplate(
    template="""
        You are a helpful assistant.
      Answer ONLY from the provided transcript context.
      If the context is insufficient, just say you don't know.

      {context}
      Question: {question}
    """,
    input_varibles=['context','question']
)


def format_docs(retriever_docs):
    context_text="\n\n".join(doc.page_content for doc in retriever_docs)

    return context_text

parallel_chain = RunnableParallel({
    'context': retriever | RunnableLambda(format_docs),
    'question': RunnablePassthrough()
})

parser=StrOutputParser()

main_chain=parallel_chain | template1 | llm | parser

result=main_chain.invoke("Can you summerize this video ?")

print(result)


