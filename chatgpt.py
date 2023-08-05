import os
import sys

import openai
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.indexes import VectorstoreIndexCreator
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain.llms import OpenAI
from langchain.vectorstores import Chroma

import gradio as  gr

# openai api key
os.environ["OPENAI_API_KEY"] ="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"

#VPN to visit openai
os.environ["OPENAI_API_BASE"] = "https://nodomainname.win/v1/"


# Enable to save to disk & reuse the model (for repeated queries on the same data)
PERSIST = False

query = None
if len(sys.argv) > 1:
  query = sys.argv[1]

if PERSIST and os.path.exists("persist"): 
  print("Reusing index...\n")
  vectorstore = Chroma(persist_directory="persist", embedding_function=OpenAIEmbeddings())
  index = VectorStoreIndexWrapper(vectorstore=vectorstore)
else:
  loader = TextLoader("data/data.txt") # Use this line if you only need data.txt
  #loader = DirectoryLoader("data/")
  
  if PERSIST:
    index = VectorstoreIndexCreator(vectorstore_kwargs={"persist_directory":"persist"}).from_loaders([loader])
  else:

    index = VectorstoreIndexCreator().from_loaders([loader])

chain = ConversationalRetrievalChain.from_llm(
  llm=ChatOpenAI(model="gpt-3.5-turbo"),
  retriever=index.vectorstore.as_retriever(search_kwargs={"k": 1}),
)

def  greet(input,request: gr.Request):
  if request:
    print("Request headers dictionary:", request.headers)
    print("IP address:", request.client.host)
  chat_history = []
  while True:
    result = chain({"question": input, "chat_history": chat_history})
    chat_history.append((input, result['answer']))
    input = None
    return result['answer']

if  __name__=="__main__":
  # gradio 用于网页展示
  demo = gr.Interface(fn=greet,
        inputs=gr.Textbox(lines=3, placeholder="Enter your question here"),
        outputs=gr.Textbox(lines=3) )
  demo.launch(share=True,server_name="10.176.5.199",server_port=8080)


