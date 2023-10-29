from flask import Flask
from datetime import datetime 
app = Flask(__name__)


books={1:"Python book",2:"Java book",3:"Flask book"}
#首頁
@app.route("/index")
@app.route("/")

def index():
    today = datetime.now()
    print(today)

    return f'<h1>你看不見我，你看不到我{today}</h1>'


@app.route("/books")

def all_books():  
    return books

@app.route("/books/id=<int:id>",methods=['GET'])
def get_books(id):
    try:

     return f"<h2>{books[id]}</h2>"
    except Exception as e:
        print(e)
    return '<hi>查無此書編號</h1>'

@app.route("/BMI/name=<name>&height=<h>&weight=<w>")

def get_BMI(name, h , w):
    BMI=round(eval(w)/(eval(h)/100)**2 ,2)
    
    return {'name':name,'height':h,'weight':w,'BMI':BMI}



if __name__=='__main__':
    app.run(debug=True)

