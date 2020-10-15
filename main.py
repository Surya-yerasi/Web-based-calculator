from flask import Flask, render_template, request
import mysql.connector
mydb = mysql.connector.connect(
  host="calculator.c1f9mdmc8xrk.us-east-2.rds.amazonaws.com",
  user="calculator",
  password="calculator",
  database = "calculator"
  )
app = Flask(__name__)
@app.route("/",  methods=["GET"])
def Home():
    cursor = mydb.cursor()
    cursor.execute("""select result from calcop order by id DESC limit 10""")
    last = cursor.fetchall()
    mydb.commit()
    cursor.close()
    return render_template("index.html", result = last)
@app.route('/calc', methods=["POST"])
def calculator():
    ip = request.form['calval']
    op = ip +' = ' + str(eval(ip))
    cursor = mydb.cursor()
    insquery = "INSERT INTO calcop(result) VALUES (%s)"
    
    cursor.execute(insquery,(op,))
    cursor.close()
    cursor = mydb.cursor()
    cursor.execute("""select result from calcop order by id DESC limit 10""")
    last = cursor.fetchall()
    mydb.commit()
    cursor.close()
   
    return render_template("index.html", result = last)


if __name__ == "__main__":
    app.run()