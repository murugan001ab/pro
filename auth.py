from flask import Flask,Blueprint,render_template,request,Response,url_for,redirect,flash,session
import sqlite3 as sql
import os
import smtplib
import random
import time


auth=Blueprint('auth',__name__)
@auth.route('/register')
def newuser():  
    return render_template('register.html')

@auth.route('/register',methods=['POST'])
def register():
    if request.method=='POST':
        name=request.form.get('name')
        email=request.form.get('email')
        mobile=request.form.get('mobile')
        password=request.form.get('password') 
        floar=request.form.get('floar')
        street=request.form.get('street')
        city=request.form.get('city')
        pin=request.form.get('pin')
        clogo=request.files['clogo']
        clogon=name+'.png'
        path='pro/static/id/clogo/'+clogon
        clogo.save(path)
        add=floar+','+street+','+city+','+pin
        print(name,email,mobile,password,add,clogon)
        try:
            con=sql.connect('pro/db/org.db')
            cur=con.cursor()
            cur.execute("insert into admins(name,email,mobile,password,cadd,clogo) values(?,?,?,?,?,?)",(name,email,mobile,password,add,clogon))
            con.commit()
            try:
                dbname=name+'.db'
                path=os.path.join('pro/db/',dbname)
                con=sql.connect(path)
                cor=con.cursor()
                cor.execute('''CREATE TABLE if not exists student (sno INTEGER not null,suid	TEXT NOT NULL,suname TEXT NOT NULL,suclass	TEXT,sudept	TEXT,sumobile	INTEGER,suemail	TEXT,suphoto	TEXT,subar	INTEGER,supass	TEXT,cname	TEXT ,role text,PRIMARY KEY(sno AUTOINCREMENT))''')
                cor.execute('''CREATE TABLE if not exists staff (sno INTEGER  not null,sid TEXT NOT NULL,sname	TEXT NOT NULL,smobile	INTEGER,semail	TEXT,sdept	TEXT,cname	INTEGER,sphoto	TEXT,sbar	TEXT,spass	TEXT,role text,PRIMARY KEY(sno AUTOINCREMENT));''')
                cor.execute('''CREATE TABLE IF NOT EXISTS attendance (id text,username TEXT,date text,stime_in text,status TEXT,role text,bar text)''')
                con.commit()
                con.close()
            except Exception as e:
                print('data base create error',e)
        except Exception as e:
            print('connection error',e)
    return redirect(url_for('auth.login'))


@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login',methods=['POST','GET'])
def logina():
    if request.method=='POST':
        username=request.form.get('username')
        password=request.form.get('password')
        con=sql.connect('pro/db/org.db')
        cur=con.cursor()
        try:
            cur.execute("select aid,name,email,password from admins")
            data=cur.fetchall()
            for i in data:
              if (i[1] or i[2])==username:
                  if (i[3])==password:
                
                      email=i[2]
                      dbname=i[1]+'.db'
                      session['logged_in_admin']=True

                      try:
                        path=os.path.join('pro/db/',dbname)
                        session['db']=path
                        con=sql.connect(path)
                        cur=con.cursor()
                        cur.execute("select *from newuser")
                        data=cur.fetchall()
                        con.commit()
                        print(data)
                      except:
                          print("connect error")
                  
                      return redirect(url_for("main.dash"))
                  else:
                      return render_template('login.html')
              else:
              
                  flash("incorrect username",'red')
            
            con.commit()
        except:
            print('user login')

    return render_template("dashboad.html")



@auth.route('/userlogin')
def userlogin():
    return render_template('userlogin.html')

@auth.route('/userlogin',methods=['POST','GET'])
def loginu():
    if request.method=='POST':
        cname=request.form.get('cname')
        username=request.form.get('username')
        password=request.form.get('password')
        dbname=cname+".db"
        path=os.path.join('pro/db/',dbname)
        con=sql.connect(path)
        cur=con.cursor()
        cur.execute("select sname,spass,sdept from staff")
        data=cur.fetchall()
        for i in data:
          if (i[0])==username:
              if (i[1])==password:
                  session['logged_in']=True
                  path=os.path.join('pro/db/',dbname)
                  session['udb']=path
                  session['sname']=username
                  
                  return redirect(url_for('main.udash'))
             
    return redirect(url_for('auth.userlogin'))



@auth.route('/base')
def base():
    if 'logged_in' in session and session['logged_in']:
        return render_template('.html')
    else:
        return redirect(url_for('auth.userlogin'))

@auth.route('/signout')
def signout():
    session['logged_in_admin']=False
    session['logged_in']=False
    return render_template('index.html')
    

@auth.route('/forget')
def forget():
    return render_template('forget.html')

@auth.route('/forget',methods=['POST','GET'])
def user_forget():
    if request.method == 'POST':
        action = request.form['action']
        if action=='sent':
            username=request.form.get('username')
            print(username)
            try:
                def generate_otp():
                    otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])
                    return otp
                def send_otp_email(email, otp):
                    smtp_server = 'smtp.gmail.com'  # Update with your SMTP server
                    smtp_port = 587  # Update with your SMTP port
                    sender_email ='attendanceregistersjc@gmail.com'
                    sender_password ='heds vojn vjks ugkz '
                    subject = 'Your One Time Password (OTP)'
                    body = f'Your OTP is: {otp}'
                    message = f'Subject: {subject}\n\n{body}'
                    try:
                        # Connect to the SMTP server
                        server = smtplib.SMTP(smtp_server, smtp_port)
                        server.starttls()
                        # Login to your email account
                        server.login(sender_email, sender_password)
                        # Send email
                        server.sendmail(sender_email, email, message)
                        print("OTP sent successfully!")
                        session['otptime'] = time.time() 
                        print(session['otptime'])
                    except Exception as e:
                        print(f"Failed to send OTP: {e}")
                    finally:
                        server.quit()
                # Example usage
                email = username
                otp = generate_otp()
                session['otp']=otp
                send_otp_email(email, otp)
                flash('opt sent success','green')
            except:
                print('otp error')

            return render_template('forget.html',username=username)
        elif action=='change':
            otpr=request.form.get('otp') 
            username=request.form.get('username')
            con=sql.connect('pro/db/org.db')
            cur=con.cursor()
            cur.execute("select * from admins")
            data=cur.fetchall()
            otp=session['otp']

            curt=time.time()
            valit=session['otptime']
            print(curt-valit)
            for i in data:
                if i[2]==username: 
                    if curt-valit<300:
                        if otp==otpr:
                            password=request.form.get('pword')
                            cpassword=request.form.get('cpword')
                            if password==cpassword:
                                cur.execute("update admins set password=? where email=?",(cpassword,username))
                                con.commit()
                                return redirect(url_for('auth.login'))
                        else:
                            print('otp not match')
                    else:
                        print("otp invalid")
            return render_template('forget.html')
    
    