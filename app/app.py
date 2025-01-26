from flask import Flask      # type: ignore

app = Flask(__name__)   # Flask constructor 
  
# A decorator used to tell the application 
# which URL is associated function 
@app.route('/')       
def hello(): 
    return 'OTHMANE'

if __name__=='__main__': 
   app.run() 
