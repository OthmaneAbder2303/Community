from flask import Flask      # type: ignore

app = Flask(__name__)   # Flask constructor 
  
# A decorator used to tell the application 
# which URL is associated function 
@app.route('/')
def index():
    return 'Index Page'

@app.route('/hello')
def hello():
    return 'Hello, World'

#app.add_url_rule('/', 'hello', hello)

@app.route('/hello/<name>') 
def hello_name(name): 
    return 'Hello %s!' % name 

if __name__=='__main__': 
   app.run(debug = True) 
