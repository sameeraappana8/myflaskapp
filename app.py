# -*- coding: utf-8 -*-
"""
Created on Sat Sep 14 00:34:03 2019

@author: Sameera
"""

from flask import Flask, g,render_template,request
import sqlite3
app = Flask(__name__)
    
@app.route("/")
def main():
    return render_template('signup.html')

@app.before_request
def before_request():
    g.db = sqlite3.connect("formdata.db")
    
@app.route("/enterDetails", methods=["post"])
def enterDetails():
    c=g.db.cursor()
    username=request.form['inputName']
    password=request.form['inputPassword']
    c.execute("select username from tbl_user where username=(?)",[username])
    if c.fetchone() is not None :
       print("in if")
       r_data=g.db.execute("select firstname,lastname,email from tbl_user where username=(?)",[username])
       return render_template('display.html',data=r_data)
    else:
          print("in else")
          g.db.execute("INSERT INTO tbl_user(username,password) VALUES (?,?)", [username,password])
          g.db.commit()
          return render_template('details.html')
    
@app.route("/giveData", methods=["post"])
def giveData():
   c=g.db.cursor()
   username= request.form['inputName']
   firstname= request.form['inputFName']
   lastname= request.form['inputLName']
   email= request.form['inputEmail']
   c.execute("update tbl_user set firstname=(?) where username=(?)", [firstname,username])
   c.execute("update tbl_user set lastname=(?) where username=(?)", [lastname,username])
   c.execute("update tbl_user set email=(?) where username=(?)", [email,username])
   g.db.commit()
   mydata=c.execute("SELECT firstname,lastname,email from tbl_user where username=(?)",[username])
   return render_template('display.html',data=mydata)
         
         
if __name__=="__main__":
    app.run()
