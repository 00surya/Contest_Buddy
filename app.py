from flask import Flask,request
import requests
app = Flask(__name__)

@app.route('/')
def ok():
    return "ok"    


        
if __name__ == "__main__":

    app.run(debug=True)













