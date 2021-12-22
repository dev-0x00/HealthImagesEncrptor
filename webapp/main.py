from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
from bcrypt import *

import MySQLdb.cursors
import re, os

from mainscript import mainClass
import decryptor, encryptor, keyGen

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'memcached'
app.secret_key = '1l0v3sh3an0r3'
#sess = session(    )

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'faceAuthentication'

mysql = MySQL(app)

@app.route('/')
def logger():
    return redirect(url_for('login'))

@ app.route('/Home')
def home():
    if 'loggedin' in session:
        Directory = mainClass()
        rootName = os.getcwd().split("/")[-1]
        return render_template('index.html', Directories=Directory.DirectoryListing("/home/dev/personalProjects/inovators/johnBCSF/ImageEncryptor/archive"), username=session['username'])

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
    path = "/home/dev/personalProjects/inovators/johnBCSF/ImageEncryptor/archive"
    os.chdir(path)
    if request.method == "POST":
        fileOrDir = request.form["fileordir"]
    if os.path.isfile(fileOrDir):
        if os.path.join(path, fileOrDir).endswith(".enc"):
            keyDir = "/home/dev/personalProjects/inovators/johnBCSF/ImageEncryptor/webapp/keys"
            keyList = os.listdir(keyDir)
            thisFile = fileOrDir.split(".")[0] + ".key"
            if thisFile in keyList:
                os.chdir(keyDir)
                with open(thisFile, 'rb') as secreteKey:
                    content = secreteKey.read()
                    cipherText = fileOrDir
                    plainText = fileOrDir.split(".")[0] + "." + fileOrDir.split(".")[1]
                    path = ("/home/dev/personalProjects/inovators/johnBCSF/ImageEncryptor/archive")
                    os.chdir(path)
                    decryptor.decryptCipher(content, cipherText, plainText)
                    os.system("rm {}".format(fileOrDir))
                       

            '''
            print(fileOrDir)
            a = mainClass()
            a.Decryptor(os.path.join(path, fileOrDir))
            '''

        extensions = ["jpg", "jpeg", "png", "gif"]
        for extension in extensions:
            if os.path.join(path, fileOrDir).endswith("{}".format(extension)):
                key = keyGen.generateKey()
                plainFile = fileOrDir
                cipherFile = fileOrDir + ".enc"
                encryptor.encryptFile(key, plainFile, cipherFile)
                os.system("rm {}".format( fileOrDir))
                keyFile = plainFile.split(".")[0] + ".key"
                os.chdir("/home/dev/personalProjects/inovators/johnBCSF/ImageEncryptor/webapp/keys")
                keyGen.saveKey(key, keyFile)
                '''
                a = mainClass()
                a.Encryptor(os.path.join(path, fileOrDir))
                '''

    elif os.path.isdir(fileOrDir):
        path = os.getcwd()
        os.chdir(path+'/'+fileOrDir)
        for fileName in os.listdir():
            print(fileName)
            if fileName.endswith("png"):
                key = keyGen.generateKey()
                plainFile = fileName
                cipherFile = fileName + ".enc"
                encryptor.encryptFile(key, plainFile, cipherFile)
                os.system("rm {}".format( fileName))
                keyFile = plainFile.split(".")[0] + ".key"
                os.chdir("/home/dev/personalProjects/inovators/johnBCSF/ImageEncryptor/webapp/keys")
                keyGen.saveKey(key, keyFile)
                Directory = mainClass()
                return render_template('index.html', Directories=Directory.DirectoryListing("/home/dev/personalProjects/inovators/johnBCSF/ImageEncryptor/archive/{}".format(fileOrDir)), username=session['username'])

            if os.path.join(path, fileOrDir).endswith(".enc"):
                keyDir = "/home/dev/personalProjects/inovators/johnBCSF/ImageEncryptor/webapp/keys"
                keyList = os.listdir(keyDir)
                thisFile = fileOrDir.split(".")[0] + ".key"
                if thisFile in keyList:
                    os.chdir(keyDir)
                    with open(thisFile, 'rb') as secreteKey:
                        content = secreteKey.read()
                        cipherText = fileOrDir
                        plainText = fileOrDir.split(".")[0] + "." + fileOrDir.split(".")[1]
                        path = ("/home/dev/personalProjects/inovators/johnBCSF/ImageEncryptor/archive")
                        os.chdir(path)
                        decryptor.decryptCipher(content, cipherText, plainText)
                        os.system("rm {}".format(fileOrDir))

            '''
            a = mainClass()
            (a.Encryptor(fileName))
            '''
    return redirect(url_for("home"))



if __name__ == '__main__':
    app.run(debug=True)
