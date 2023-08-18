from langchain.document_loaders import CSVLoader, UnstructuredPDFLoader,UnstructuredExcelLoader, Docx2txtLoader

from langchain.document_loaders.merge import MergedDataLoader
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from io import StringIO
import os 
from pdfminer.pdfpage import PDFPage
from langchain.indexes import VectorstoreIndexCreator

os.environ["OPENAI_API_KEY"] ="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"


def extract_text_from_pdf(pdf_path):
    resource_manager = PDFResourceManager()
    fake_file_handle = StringIO()
    converter = TextConverter(resource_manager, fake_file_handle, laparams=LAParams())
    page_interpreter = PDFPageInterpreter(resource_manager, converter)

    with open(pdf_path, 'rb') as file:
        for page in PDFPage.get_pages(file, check_extractable=True):
            page_interpreter.process_page(page)

    text = fake_file_handle.getvalue()
    converter.close()
    fake_file_handle.close()
    return text

def load_files_from_directory(directory_path):
    loaders = []
    i=0
    for dirpath, dirnames, filenames in os.walk(directory_path):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            # 根据文件扩展名选择合适的加载器
            if os.path.isfile(file_path) and filename.endswith('.pdf'):
                #text = extract_text_from_pdf(file_path)
                loader = UnstructuredPDFLoader(file_path, mode="single", strategy="fast", check_extractable=False)
            elif filename.endswith('.csv'):
                loader = CSVLoader(file_path)
            elif filename.endswith('.xlsx'):
                loader = UnstructuredExcelLoader(file_path, mode="elements")
            elif filename.endswith('.docx'):
                loader = Docx2txtLoader(file_path)
            else:
                # we aren't surpport the file now,continue
                #print("we aren't surpport the file format {} ".format(filename))
                continue
            if not "mergered_loader" in vars():
                mergered_loader = loader
            else:
                mergered_loader=MergedDataLoader(loaders=[mergered_loader, loader])

        i+=1
        if i>4:
            break 
    #使用MergeLoader合并所有加载器
    #documents=mergered_loader.load()
    return mergered_loader.load()  

if __name__=="__main__":
    dir_path  = "./data"
    documents = load_files_from_directory(dir_path)
    print(documents[0])
    index = VectorstoreIndexCreator().from_documents(documents)



