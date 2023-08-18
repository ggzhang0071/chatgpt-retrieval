from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.indexes import VectorstoreIndexCreator
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain.llms import OpenAI
from langchain.vectorstores import Chroma
import gradio as  gr
import openai, os, sys
from  langchain_dir_load  import load_files_from_directory


os.environ["OPENAI_API_KEY"] ="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"
#os.environ["OPENAI_API_BASE"] = "https://api.openai.mycompany.com/v1/"



# Enable to save to disk & reuse the model (for repeated queries on the same data)
PERSIST = False

query = None
if len(sys.argv) > 1:
  query = sys.argv[1]

dir_path  = "./data"
documents = load_files_from_directory(dir_path)

if PERSIST:
    index = VectorstoreIndexCreator(vectorstore_kwargs={"persist_directory":"persist"}).from_loaders([loader])
else:
    index = VectorstoreIndexCreator().from_documents(documents)

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
        outputs=gr.Textbox(lines=3))
  demo.launch()


