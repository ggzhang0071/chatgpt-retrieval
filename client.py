import gradio as gr 
from chatgpt import greet

guihua_gpt_url="127.0.0.1"
port ="8080"

def launch_demo(guihua_gpt_url,port):
    demo = gr.Interface(fn=greet,
            inputs=gr.Textbox(lines=3, placeholder="Enter your question here"),
            outputs=gr.Textbox(lines=3) )
    demo.launch(server_name=guihua_gpt_url,server_port=port)