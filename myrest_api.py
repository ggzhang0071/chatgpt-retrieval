from flask import Flask, request, jsonify
from chatgpt import greet
import argparse
app = Flask(__name__)



# REST API接口路由
@app.route(DETECTION_URL, methods=['POST'])
def chatbot():
    if request.method != 'POST':
        return
    input_text= request.form['text']
    response= greet(input_text)
    with app.app_context():
        return jsonify({"response":response})
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Flask API exposing chatbot')
    parser.add_argument('--port', default=5000, type=int, help='port number')
    opt = parser.parse_args()

    #app.run(host='10.176.5.199', port=8080)
    app.run(host='0.0.0.0', port=5000)
    #print(chatbot_tmp("你是谁"))