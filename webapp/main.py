from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
from bcrypt import *

import MySQLdb.cursors
import re, os

from mainscript import mainClass
import worker

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'memcached'
app.secret_key = ''
#sess = session(    )

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = ''

mysql = MySQL(app)

@app.route('/')
def logger():
    return redirect(url_for('login'))

@ app.route('/Home')
def home():
    if 'loggedin' in session:
        Directory = mainClass()
        rootName = os.getcwd().split("/")[-1]
        return render_template('index.html', Directories=Directory.DirectoryListing(""), username=session['username'])

    return redirect(url_for('login'))

@app.route('/Login', methods=['GET', 'POST'])
def login():
    msg = ''
    #crete variables if the username, password are in the form and the request is post.
    if request.method == 'POST' and 'Email' in request.form and 'Password' in request.form:
        Email = request.form['Email']
        Password = request.form['Password']
        #check if the username and the password match the details in the msql table
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM Users WHERE Email = %s and Passowrd = %s', (Email, Password))
        #fetch the record and return the results
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['UserName']
            return redirect(url_for('home'))

        else:
            msg = "Incorrect, check your Emain/Password "
            return redirect(url_for('login'))


    return render_template('login.html', msg=msg)

@app.route('/Logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        formDetails = request.form
        Email = formDetails['Email']
        Username = formDetails['Username']
        Password = formDetails['Password']
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO Users(Email, Username, Passowrd) VALUES(%s, %s, %s)", (Email, Username, Password))
        mysql.connection.commit()
        cursor.close()
        while True:
            return redirect(url_for('login'))

    return render_template("signup.html")



@app.route("/Home", methods=["POST"])
def operator():
    path = ("")
    os.chdir(path)
    if request.method == "POST":
        fileOrDir = request.form["fileordir"]
        password = "Even a fool knows the secret is understanding"
        print(fileOrDir)
        work = worker.Encryptor(password)
        if os.path.isfile(fileOrDir):
            if os.path.join(path, fileOrDir).endswith(".enc"): 
                cipherText = fileOrDir
                os.chdir("")
                work.decrypt_file(fileOrDir)
                #call decryption function
             
            extensions = ["jpg", "jpeg", "png", "gif"]
            for extension in extensions:
                if os.path.join(path, fileOrDir).endswith("{}".format(extension)):
                    work.encrypt_file(fileOrDir)

        elif os.path.isdir(fileOrDir):
            path = os.getcwd()
            directory = (path+'/'+fileOrDir)
            if directory.endswith(".enc"):
                work.decrypt_all_files(directory)
                #call directory decryptory
                print(directory)
                Directory = mainClass()
                directory1 = directory.split("/")[-1].split(".")[0]
                directory2 = directory.split("/")
                directory2.pop()
                directory3 = "/".join(directory2) + "/" + directory1
                return render_template('index.html', Directories=Directory.DirectoryListing(directory3), username=session['username'])

            else:
                work.encrypt_all_files(directory)
                #call directory encrypt
                Directory = mainClass()
                directory1 = directory.split("/")[-1]  + ".enc"
                directory2 = directory.split("/")
                directory2.pop()
                directory3 = "/".join(directory2) + "/" + directory1
                return render_template('index.html', Directories=Directory.DirectoryListing(directory3), username=session['username'])

         
        return redirect(url_for("home"))



if __name__ == '__main__':
    app.run(debug=True)
