from flask import Flask, render_template,url_for, request
import Data

app= Flask(__name__)


@app.route("/",methods=["GET","POST"])
def main():
    if request.method == 'GET':
        print(request.method)
        return render_template("index.html")
        
    if request.method =="POST":

        data= request.form
        stockname = data['stock']

        stock = Data.get_stock(stockname)

        a,b =Data.get_data(stock)

        predictions= Data.predict(a,b)

        days=range(1, len(predictions)+1)

        return render_template("index.html", results=predictions , day=days, len= len(predictions))


if __name__ =='__main__':
    app.run(debug=True)