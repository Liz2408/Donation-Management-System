# -*- coding: utf-8 -*-


from flask import Flask, render_template, request, session, redirect, url_for
from datetime import date,time, datetime
import sqlite3 as sql
import os
# Create Database if it doesnt exist
if not os.path.isfile('database.db'):
  conn = sql.connect('database.db')
  conn.execute('CREATE TABLE IF NOT EXISTS Donors (Name TEXT NOT NULL, Amount INTEGER NOT NULL, Email TEXT NOT NULL, [timestamp] TIMESTAMP)')
  conn.execute('CREATE TABLE IF NOT EXISTS Users (Name TEXT NOT NULL, Email TEXT NOT NULL, Password TEXT NOT NULL, Contact INTEGER NOT NULL)')
  conn.execute('CREATE TABLE IF NOT EXISTS Ngos (Name TEXT NOT NULL, Email TEXT NOT NULL, Password TEXT NOT NULL, Contact INTEGER NOT NULL)')
  conn.execute('CREATE TABLE IF NOT EXISTS Requirements (ReqID	INTEGER NOT NULL UNIQUE,Ngo_Name TEXT NOT NULL,Requirement TEXT NOT NULL,Quantity/Amount	INTEGER NOT NULL,Other_Details	TEXT NOT NULL,PRIMARY KEY("ReqID" AUTOINCREMENT)')

  conn.close()

app = Flask(__name__,static_url_path='/assets',
            static_folder='assets', 
            template_folder='./')

@app.route('/')
def root():
   session['logged_out']= 1
   return render_template('index.html')

@app.route('/index.html')
def index():
   return render_template('index.html')

@app.route('/header_page.html')
def header_page():
   return render_template('header_page.html')

@app.route('/menu-bar-charity.html')
def menu_bar_charity():
   return render_template('menu-bar-charity.html')

@app.route('/footer.html')
def footer():
   return render_template('footer.html')

@app.route('/sidebar.html')
def sidebar():
   return render_template('sidebar.html')   

@app.route('/contact.html')
def contact():
   return render_template('contact.html')

@app.route('/our-causes.html')
def our_causes():
   return render_template('our-causes.html')

@app.route('/about-us.html')
def about_us():
   return render_template('about-us.html')

@app.route('/choose.html')
def choose():
   return render_template('choose.html')


@app.route('/needs.html')
def display_data():
    conn = sql.connect('database.db')  
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Requirements_Updated")  
    data = cursor.fetchall()
    conn.close()

    return render_template('needs.html', data=data)

@app.route('/details/<int:req_id>')
def details(req_id):
    conn = sql.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Requirements_Updated WHERE ReqID = ?", [(req_id)])
    data = cursor.fetchall()
    conn.close()

    if data:
        return render_template('details.html', data=data)


@app.route('/register_donor', methods=['GET', 'POST'])
def register_donor():
  if request.method == 'POST':
    nm = request.form['nm']
    contact = request.form['contact']
    email = request.form['email']
    password = request.form['password']
         
    with sql.connect("database.db") as con:
      cur = con.cursor()
      #check if User already present
      cur.execute("SELECT Email FROM Users WHERE Email=(?)",[(email)])
      data = cur.fetchall()
      if len(data)>0:
        print('User already exists')
        user_exists=1
      else:
        print("User not found, register new user")
        user_exists=0
        cur.execute("INSERT INTO Users (Name,Email,Password,Contact) VALUES (?,?,?,?)",(nm,email,password,contact) )
        
  return render_template('login_donor.html',user_exists=user_exists, invalid = None, logged_out=None)


@app.route('/login_donor.html',  methods=['GET', 'POST'])
def login_donor():
  invalid = None
  if request.method == 'POST':
    email = request.form['email']
    password = request.form['password']     
    with sql.connect("database.db") as con:
      cur = con.cursor()
      #Validate user credentails from database
      cur.execute("SELECT Email FROM Users WHERE Email=(?) AND Password=(?)",[(email),(password)])
      data = cur.fetchall()
      if len(data)>0:
        print('Login Success')
        # Fetch name of user
        cur.execute("SELECT Name FROM Users WHERE Email=(?) AND Password=(?)",[(email),(password)])
        data = cur.fetchall()
        nm=data[0][1]
        # Store User details in Session and log in user
        session['nm'] = nm
        session['email'] = email
        session['user_id'] = data[0][0]
        session['logged_out'] = None
        return redirect(url_for('profile'))
      else:
        print("Invalid Login")
        invalid=1  
  return render_template('login_donor.html',user_exists=None, invalid = invalid, logged_out=None)

@app.route('/register_ngo', methods=['GET', 'POST'])
def register_ngo():
  if request.method == 'POST':
    nm = request.form['nm']
    contact = request.form['contact']
    email = request.form['email']
    password = request.form['password']
         
    with sql.connect("database.db") as con:
      cur = con.cursor()
      #check if User already present
      cur.execute("SELECT Email FROM Ngos WHERE Email=(?)",[(email)])
      data = cur.fetchall()
      if len(data)>0:
        print('NGO already exists')
        ngo_exists=1
      else:
        print("NGO not found, register new NGO")
        ngo_exists=0
        cur.execute("INSERT INTO Ngos (Name,Email,Password,Contact) VALUES (?,?,?,?)",(nm,email,password,contact) )
        
  return render_template('login_ngo.html',ngo_exists=ngo_exists, invalid = None, logged_out=None)


@app.route('/login_ngo.html',  methods=['GET', 'POST'])
def login_ngo():
  invalid = None
  if request.method == 'POST':
    email = request.form['email']
    password = request.form['password']     
    with sql.connect("database.db") as con:
      cur = con.cursor()
      #Validate user credentails from database
      cur.execute("SELECT Email FROM Ngos WHERE Email=(?) AND Password=(?)",[(email),(password)])
      data = cur.fetchall()
      if len(data)>0:
        print('Login Success')
        # Fetch name of NGO
        cur.execute("SELECT Name FROM Ngos WHERE Email=(?) AND Password=(?)",[(email),(password)])
        nm = cur.fetchall()
        nm=nm[0][0]
        # Store User details in Session and log in user
        session['nm'] = nm
        session['email'] = email
        session['logged_out'] = None

        return redirect(url_for('publish'))
      else:
        print("Invalid Login")
        invalid=1  
  return render_template('login_ngo.html',user_exists=None, invalid = invalid, logged_out=None)


@app.route('/logout')
def logout():
  session.clear()
  session['logged_out']=1
  print('Session Cleared and Logged Out')
  return render_template('index.html')  

# @app.route('/donate')
# def donate():
#    # If Logged Out, Redirect to Log In page
#    if session['logged_out']:
#     return render_template('login_donor.html',logged_out=1,user_exists=None, invalid = None)
#    nm = session['nm']
#    email = session['email']
#    return render_template('donate.html',nm=nm,email=email)         

# #insert values into table
# @app.route('/donation',methods = ['POST', 'GET'])
# def donation():
#    # If Logged Out, Redirect to Log In page
#    if session['logged_out']:
#     return render_template('login_donor.html',logged_out=1,user_exists=None, invalid = None)
#    if request.method == 'POST':
#          nm = session['nm']
#          email = session['email']
#          amt = request.form['amt']
#          today = datetime.now()
#          today = today.strftime("%d-%m-%Y"+","+"%H:%M")
         
#          with sql.connect("database.db") as con:
#             cur = con.cursor()
#             #check if already donated. If already donated, add donation. Else create new donation
#             cur.execute("SELECT Email FROM Donors WHERE Email=(?)",[(email)])
#             data = cur.fetchall()
#             if len(data)>0:
#               cur.execute("UPDATE Donors SET Amount=Amount+(?) WHERE Email=(?)",[(amt),(email)])
#             else:
#               cur.execute("INSERT INTO Donors (Name,Amount,Email,timestamp) VALUES (?,?,?,?)",(nm,amt,email,today) )                
#             con.commit()
            
#             # Greeting
#             msg = "Thank You for Donating"
#             for row in cur.execute("SELECT Amount FROM Donors WHERE Email=(?)",[(email)]):
#                 Amount=row
#             con.close()
#          return render_template("greeting.html",msg = msg,nm=nm,Amount=Amount,today=today, email=email)
#          #con.close()

    
@app.route('/view_needs')
def view_needs():
    if session['logged_out']:
      return render_template('login_donor.html',logged_out=1,user_exists=None, invalid = None)
    conn = sql.connect('database.db')  
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Requirements_Updated where Status='Pending' COLLATE BINARY")  
    data = cursor.fetchall()
    conn.close()

    return render_template('needs.html', data=data)

@app.route('/make_donation/<int:req_id>', methods=['GET', 'POST'])
def make_donation(req_id):
   # If Logged Out, Redirect to Log In page
   if session.get('logged_out'):
      return render_template('login_donor.html', logged_out=1, user_exists=None, invalid=None)

   conn = sql.connect('database.db')
   cursor = conn.cursor()
   cursor.execute("SELECT * FROM Requirements_Updated WHERE ReqID = (?)", [req_id])
   req_record = cursor.fetchone()
   
   ngo_name=req_record[1]
   cursor.execute("SELECT * FROM Ngos WHERE Name = (?)", [ngo_name])
   reqq_record = cursor.fetchone()
   ngo_id=reqq_record[0]

   #conn.close()

   if request.method == 'POST':
      nm = req_record[1]
      donor_id = session['user_id']
      #ngo_id = session['ngo_id']
      item = req_record[3]
      amt = request.form['amt']
      today = datetime.now().strftime("%d-%m-%Y, %H:%M")

      with sql.connect("database.db") as con:
         cur = con.cursor()

         #cursor.execute("SELECT * FROM Requirements_Updated where ReqID=(?) COLLATE BINARY",[(req_id)])  
         
         print("Donor ID:", donor_id)
         cur.execute("INSERT INTO Donations (Donor_ID, Ngo_ID, Req_ID, Item, \"Quantity/Amount\", Timestamp) VALUES (?, ?, ?, ?, ?, ?)",
                     (donor_id, ngo_id, req_id, item, amt, today))
         

         cur.execute("INSERT INTO Donors (Donor_ID, Timestamp) VALUES (?, ?)", (donor_id, today))

         
         cur.execute("UPDATE Requirements_Updated SET \"Quantity/Amount\" = \"Quantity/Amount\" - ? WHERE ReqID = ?", (amt, req_id))

         con.commit()
         msg = "Thank You for Donating"

         con.close()

      return render_template("greeting.html", msg=msg, nm=nm, amt=amt, today=today)

   return render_template("donate.html", req_record=req_record,req_id=req_id)



    # conn = sql.connect('database.db')
    # cursor = conn.cursor()
    # cursor.execute("SELECT * FROM Requirements_Updated WHERE ReqID = ?", [(req_id)])
    # data = cursor.fetchall()
    # conn.close()

    # if data:
    #     return render_template('details.html', data=data)


@app.route('/publish')
def publish():
   # If Logged Out, Redirect to Log In page
   if session['logged_out']:
    return render_template('login_ngo.html',logged_out=1,ngo_exists=None, invalid = None)
   nm = session['nm']
   email = session['email']
   return render_template('publish_need.html',nm=nm,email=email)         

#insert values into table
@app.route('/publishing',methods = ['POST', 'GET'])
def publishing():
   # If Logged Out, Redirect to Log In page
   if session['logged_out']:
    return render_template('login_ngo.html',logged_out=1,ngo_exists=None, invalid = None)
   if request.method == 'POST':
         nm = session['nm']
         email = session['email']
         req=request.form['req']
         amt = request.form['amt']
         other = request.form['other']
         today = datetime.now()
         today = today.strftime("%d-%m-%Y"+","+"%H:%M")
         
         with sql.connect("database.db") as con:
            cur = con.cursor()
            #check if already donated. If already donated, add donation. Else create new donation
            cur.execute("INSERT INTO Requirements_History (Ngo_Name,Email,Requirement,\"Quantity/Amount\",Other_Details,Timestamp) VALUES (?,?,?,?,?,?)",(nm,email,req,amt,other,today) )                
            cur.execute("INSERT INTO Requirements_Updated (Ngo_Name,Email,Requirement,\"Quantity/Amount\",Other_Details,Timestamp) VALUES (?,?,?,?,?,?)",(nm,email,req,amt,other,today) )                
            con.commit()
            
            # Greeting
            msg = "Thank You for Partnering with Us"
            # for row in cur.execute("SELECT Amount FROM Donors WHERE Email=(?)",[(email)]):
            #     Amount=row
            # con.close()
         #return render_template("profile.html",msg = msg,nm=nm,email=email)
         return render_template("profile.html")
         #con.close()

#Display List of Donations
@app.route('/list1')
def list1():
   # If Logged Out, Redirect to Log In page
   if session['logged_out']:
    return render_template('login_donor.html',logged_out=1,user_exists=None, invalid = None)
   con = sql.connect("database.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("SELECT * FROM Donors")
   
   rows = cur.fetchall();
   return render_template("list1.html",rows = rows)

#Display Profile
@app.route('/profile')
def profile():
   # If Logged Out, Redirect to Log In page
   if session['logged_out']:
    return render_template('login_donor.html',logged_out=1,user_exists=None, invalid = None)
   nm = session['nm']
   email = session['email']
   with sql.connect("database.db") as con:
    cur = con.cursor()
    # Fetch details of user
    cur.execute("SELECT Contact FROM Users WHERE Email=(?)",[(email)])
    contact = cur.fetchall()
    contact=contact[0][0]

    cur.execute("SELECT Password FROM Users WHERE Email=(?)",[(email)])
    password = cur.fetchall()
    password=password[0][0]
   return render_template("profile.html",nm=nm,email=email,contact=contact,password=password)

if __name__ == '__main__':
   app.secret_key = ".."
   app.run()