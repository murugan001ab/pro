from flask import Flask,Blueprint,render_template,session,redirect,url_for,request
import sqlite3 as sql
import os 
from datetime import datetime
main=Blueprint('main',__name__)

@main.route('/')
def home():
    
    return render_template('index.html')

@main.route('/dash')
def dash():
    if 'logged_in_admin' in session and session['logged_in_admin']:
        return render_template('dashboad.html')
    else:
        return redirect(url_for('auth.userlogin'))
    

@main.route('/adds')
def adds():
    if 'logged_in_admin' in session and session['logged_in_admin']:


        return render_template('adds.html')
    else:
        return redirect(url_for('auth.login'))
    
@main.route('/adds',methods=['POST','GET'])
def addst():
    if request.method =="POST":
        name=request.form.get('name')
        age=request.form.get('age')
        role=request.form.get('role')
        clas=request.form.get('class')
        email=request.form.get('email')
        mobile=request.form.get('mobile')
        file=request.files['file']
        filename=name+'.png'
        if file:
            filepath="pro/static/css/images/"+filename
            file.save(filepath)
        try:
            path=session['db']
            con=sql.connect(path)
            cor=con.cursor()
            cor.execute("insert into profiles(name,class,email,mobile,role,age,file) values(?,?,?,?,?,?,?)",(name,clas,email,mobile,role,age,filename))
            cor.execute("insert into newuser(username,email,mobile,password) values(?,?,?,?)",(name,email,mobile,name))

            con.commit()
            con.close()
            return redirect(url_for('main.profiles'))
        except:
            print("insert erorr")

        
    return redirect(url_for('main.profiles'))    

    

@main.route('/asheet')
def asheet():
    if 'logged_in_admin' in session and session['logged_in_admin']:
        
        path=session['db']
        con=sql.connect(path)
        cur=con.cursor()
        cur.execute("select uid,username from newuser")
        data=cur.fetchall()

        return render_template('attendacesheet.html',data=data)
    else:
        return redirect(url_for('auth.login'))
    
@main.route('/asheet',methods=['POST','GET'])
def asheetd():
    if request.method=="POST":
        d=datetime.now()
        date=d.strftime("%d/%m/%Y")
        time=d.strftime("%H:%M:%S")
        path=session['db']
        con=sql.connect(path)
        cur=con.cursor()
        student_selected=[]
        student_selected.append(request.form.getlist('uid'))
        cur.execute("select id,date from attendance")
        data=cur.fetchall()
        if data:
            print(data)
        else:
            data=('0','0','0'),('0','0','0')

        
        for i,y in zip(data,student_selected):
            print(i)
            print(y)

        
            # if (i[0]!=int(y[0]) and i[1]!=y[1]):
            #     print(i)
            #     status='present'
          
            #     try:
            #         cur.execute("insert into attendance values(?,?,?,?,?)",(int(y[0]),y[1::],date,time,status))
            #         con.commit()
            #     except:
            #         print("insert error")

            # else:

            #     print("condition not stat")
                
        
           
    return redirect(url_for("main.attendance"))


@main.route('/attendance')
def attendance():
    if 'logged_in_admin' in session and session['logged_in_admin']:
        date=datetime.today().strftime("%d/%m/%Y")
        print(date)
        con=sql.connect(session['db'])
        cur=con.cursor()
        cur.execute("select * from attendance where date=?",(date,))
        data=cur.fetchall()
        return render_template('attendance.html',data=data)
    else:
        return redirect(url_for('auth.login'))


@main.route('/profiles')
def profiles():
    if 'logged_in_admin' in session and session['logged_in_admin']:
        try:
            path=session['db']
            con=sql.connect(path)
            cor=con.cursor()
            con.row_factory=sql.Row
            cor.execute("select * from profiles")
            data=cor.fetchall()
            return render_template('profiles.html',datas=data)
        except:
            print("insert erorr")
        
    else:
        return redirect(url_for('auth.login'))






        