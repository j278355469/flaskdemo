from flask import Flask,render_template, request
from datetime import datetime 
import pandas as pd
import json



app = Flask(__name__)
today = datetime.now()

books={1:"Python book",2:"Java book",3:"Flask book"}
#首頁
@app.route("/index")
@app.route("/")
def index():
    today = datetime.now()
    print(today)

    return render_template("index.html",today=today)


@app.route("/books")
def all_books():
    books={
1:{
"name":"Python book",
"price":299,
"image_url":"https://im2.book.com.tw/image/getImage?i=https://www.books.com.tw/img/CN1/136/11/CN11361197.jpg&v=58096f9ck&w=348&h=348"
},

2:{

"name":"Java book",
"price":399,
"image_url":"https://im1.book.com.tw/image/getImage?i=https://www.books.com.tw/img/001/087/31/0010873110.jpg&v=5f7c475bk&w=348&h=348"
},

3:{
"name":"C# book",
"price":499,
"image_url":"https://im1.book.com.tw/image/getImage?i=https://www.books.com.tw/img/001/036/04/0010360466.jpg&v=62d695bak&w=348&h=348"
},
} 
    for id in books:
            print(id , books[id]["name"],books[id]["price"],books[id]["image_url"]) 
    return render_template("books.html",**locals())

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

@app.route("/pm25-chart")
def get_pm25_chart():
    return render_template("pm25-chart.html")



@app.route("/pm25-json")
def get_pm25_josn():
    url='https://data.moenv.gov.tw/api/v2/aqx_p_02?api_key=e8dd42e6-9b8b-43f8-991e-b3dee723a52d&limit=1000&sort=datacreationdate%20desc&format=CSV'
    df=pd.read_csv(url).dropna()
    six_county=['新北市','臺北市','桃園市','臺中市','臺南市','高雄市']

    six_data={}
    for county in six_county:
        #print(county)
        #print(df.groupby('county').get_group(county)['pm25'].mean())
        six_data[county]=round(df.groupby('county').get_group(county)['pm25'].mean(),2)


    json_data={
        "title": "PM2.5數據",
        "xData": df['site'].tolist(),
        "yData": df["pm25"].tolist(),
        "sixData":six_data,
    }
    

    return json.dumps(json_data,ensure_ascii=False)





@app.route("/pm25",methods=['GET',"POST"])
def get_pm25():
    global ascending
    url='https://data.moenv.gov.tw/api/v2/aqx_p_02?api_key=e8dd42e6-9b8b-43f8-991e-b3dee723a52d&limit=1000&sort=datacreationdate%20desc&format=CSV'
    
    now=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sort = False
    ascending = True
    if request.method =="POST":
        if request.form.get('sort'):
            sort = True


    try:
        df=pd.read_csv(url).dropna()
        if sort:
            df = df.sort_values("pm25", ascending=ascending)
            ascending=not ascending
        else:
            ascending = True
        columns=df.columns.tolist()
        values=df.values.tolist()
        lowest=df.sort_values('pm25').iloc[0][['site','pm25']].values
        highes=df.sort_values('pm25').iloc[-1][['site','pm25']].values
        
        message="取得資料成功!"
        
    except Exception as e:
        print(e)
        message="取得資料失敗..."


    return render_template("pm25.html",**locals())

if __name__=='__main__':
    

    app.run(debug=True)




# https://github.com/17app001/flask-demo1/tree/master/templates