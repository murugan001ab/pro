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
        d=datetime.now()
        date=d.strftime("%d/%m/%Y")
        print(date)

        db=session['db']
        print(db)
        con=sql.connect(db)
        cur=con.cursor()
        cur.execute('select count(sno) from staff')
        data=cur.fetchall()
        totalstaff=data[0][0]
        cur.execute('select count(sno) from student')
        data=cur.fetchall()
        totalstudent=data[0][0]
        cur.execute('select count(*) from attendance where role="student" and date=?',(date,))
        data=cur.fetchall()
        print(data)
        studentcome=data[0][0]
        if totalstudent==0:
            studentcomep=0
        else:    
            studentcomep=(studentcome/totalstudent)*100
        print(studentcomep)
        studentleave=totalstudent-studentcome
        cur.execute('select count(*) from attendance where role="staff" and date=?',(date,))
        data=cur.fetchall()
        staffcome=data[0][0]
        if totalstaff==0:
            staffcomep=0
        else:
            staffcomep=(staffcome/totalstaff)*100
        staffleave=totalstaff-staffcome
    



        return render_template('dashboad.html',student=totalstudent,studentcome=studentcome,studentcomep=studentcomep,studentleave=studentleave,staff=totalstaff,staffcome=staffcome,staffcomep=staffcomep,staffleave=staffleave)
    else:
        return redirect(url_for('auth.userlogin'))

@main.route('/udash')
def udash():
    if 'logged_in' in session and session['logged_in']:
        return render_template('udash.html')
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
        
        role=request.form.get('role')
        dept=request.form.get('dept')
        email=request.form.get('email')
        mobile=request.form.get('mobile')
        file=request.files['file']
        filename=mobile+'.png'
        if file:
            filepath="pro/static/css/images/"+filename
            file.save(filepath)
        try:
            path=session['db']
            con=sql.connect(path)
            cor=con.cursor()
            cname=str(path).split("/")[2]
            cname=cname.split('.')[0]
            
            date=datetime.now()
            date=date.strftime("%Y")[2::]

            cor.execute("select sno from staff")
            data=cor.fetchall()
            
            
            if not data:
                sid=cname[0]+date+dept+role[0]+'1'

                cor.execute("insert into staff(sid,sname,sdept,semail,smobile,cname,sphoto,sbar,spass,role) values(?,?,?,?,?,?,?,?,?,?)",(sid,name,dept,email,mobile,cname,filename,mobile,name,role))
            else:
                data=int(data[-1][0])+1
                sid=cname[0]+date+dept+role[0]+str(data)
                cor.execute("insert into staff(sid,sname,sdept,semail,smobile,cname,sphoto,sbar,spass,role) values(?,?,?,?,?,?,?,?,?,?)",(sid,name,dept,email,mobile,cname,filename,mobile,name,role))

            con.commit()
            con.close()
            return redirect(url_for('main.profiles'))
        except Exception as e:
            print("insert erorr",e)

        
    return redirect(url_for('main.profiles'))    

    

@main.route('/sasheet')
def sasheet():
    if 'logged_in_admin' in session and session['logged_in_admin']:
        
        path=session['db']
        con=sql.connect(path)
        cur=con.cursor()
        cur.execute("select sid,sname from staff")
        data=cur.fetchall()

        return render_template('attendacesheet.html',data=data)
    else:
        return redirect(url_for('auth.login'))
    
@main.route('/sasheet',methods=['POST'])
def asheetd():
    if request.method=="POST":
        d=datetime.now()
        date=d.strftime("%d/%m/%Y")
        time=d.strftime("%H:%M:%S")
        path=session['db']
        con=sql.connect(path)
        cur=con.cursor()

        student_selected=[]
        student_selected=request.form.getlist('list')
        role="staff"
        print(student_selected)
        for i in student_selected:
            status='present'
            i,j=i.split(",")[0],i.split(",")[1]
            print(i,j)
            try:
                cur.execute("select id,date from attendance where username=? and date=?",(str(i),date))
                data=cur.fetchall()
                if len(data)==0:

                    cur.execute("insert into attendance(id,username,date,stime_in,status,role) values(?,?,?,?,?,?)",(str(i),str(j),date,time,status,role))
                    con.commit()
                    
                else:
                    print(data)
            except Exception as e:
                print("insert error",e)

    return redirect(url_for("main.attendance"))

@main.route('/suasheet')
def suasheet():
    if 'logged_in_admin' in session and session['logged_in_admin']:
        
        path=session['db']
        con=sql.connect(path)
        cur=con.cursor()
        if request.method=="GET":
            sudept=request.args.get('dept')
            print(sudept)
        cur.execute("select suid,suname from student where sudept=?",(sudept,))
        data=cur.fetchall()

        return render_template('suas.html',data=data)
    else:
        return redirect(url_for('auth.login'))

@main.route('/ssuasheet')
def ssuasheet():
    if 'logged_in_admin' in session and session['logged_in_admin']:
        
        path=session['udb']
        sname=session['sname']
        con=sql.connect(path)
        cur=con.cursor()
        cur.execute("select sdept from staff where sname=?",(sname,))
        sdept=cur.fetchone()    
        print(sdept)
        cur.execute("select suid,suname from student where sudept=?",(sdept[0],))
        data=cur.fetchall()

        return render_template('ssua.html',data=data)
    else:
        return redirect(url_for('auth.login'))
@main.route('/ssuasheet',methods=['POST'])
def ssuasheetd():
    if request.method=="POST":
        d=datetime.now()
        date=d.strftime("%d/%m/%Y")
        time=d.strftime("%H:%M:%S")
        path=session['db']
        con=sql.connect(path)
        cur=con.cursor()

        student_selected=[]
        student_selected=request.form.getlist('list')
        role="student"
        print(student_selected)
        for i in student_selected:
            status='present'
            i,j=i.split(",")[0],i.split(",")[1]
            print(i,j)
            try:
                cur.execute("select id,date from attendance where username=? and date=?",(str(i),date))
                data=cur.fetchall()
                if len(data)==0:

                    cur.execute("insert into attendance(id,username,date,stime_in,status,role) values(?,?,?,?,?,?)",(str(i),str(j),date,time,status,role))
                    con.commit()
                    
                else:
                    print(data)
            except Exception as e:
                print("insert error",e)

    return redirect(url_for("main.ua"))
    


@main.route('/suasheet',methods=['POST'])
def suasheetd():
    if request.method=="POST":
        d=datetime.now()
        date=d.strftime("%d/%m/%Y")
        time=d.strftime("%H:%M:%S")
        path=session['db']
        con=sql.connect(path)
        cur=con.cursor()

        student_selected=[]
        student_selected=request.form.getlist('list')
        role="student"
        print(student_selected)
        for i in student_selected:
            status='present'
            i,j=i.split(",")[0],i.split(",")[1]
            print(i,j)
            try:
                cur.execute("select id,date from attendance where username=? and date=?",(str(i),date))
                data=cur.fetchall()
                if len(data)==0:

                    cur.execute("insert into attendance(id,username,date,stime_in,status,role) values(?,?,?,?,?,?)",(str(i),str(j),date,time,status,role))
                    con.commit()
                    
                else:
                    print(data)
            except Exception as e:
                print("insert error",e)

    return redirect(url_for("main.attendance"))
    


@main.route('/attendance')
def attendance():
    if 'logged_in_admin' in session and session['logged_in_admin']:
        date=datetime.today().strftime("%d/%m/%Y")
        role=request.args.get('role')
        con=sql.connect(session['db'])
        cur=con.cursor()
        cur.execute("select * from attendance where date=? and role=?",(date,role))
        data=cur.fetchall()
        return render_template('attendance.html',data=data)
    else:
        return redirect(url_for('auth.login'))
@main.route('/ua')
def ua():
    if 'logged_in_admin' in session and session['logged_in_admin']:
        date=datetime.today().strftime("%d/%m/%Y")
        role="student"
        con=sql.connect(session['db'])
        sname=session['sname']
        cur=con.cursor()
        cur.execute("select sdept from staff where sname=?",(sname,))
        sdept=cur.fetchone()    
        print(sdept)
        cur.execute("select * from attendance where date=? and role=? and id LIKE ?",(date,role,'%'+sdept[0]+'%'))
        data=cur.fetchall()
        return render_template('ua.html',data=data)
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
            cor.execute("select * from staff")
            data=cor.fetchall()
            return render_template('staff.html',datas=data)
        except:
            print("insert erorr")
        
    else:
        return redirect(url_for('auth.login'))

@main.route('/suprofiles')
def suprofiles():
    if 'logged_in_admin' in session and session['logged_in_admin']:
        path=session['db']
        con=sql.connect(path)
        cur=con.cursor()
        if request.method=="GET":
            sudept=request.args.get('dept')
            print(sudept)
        cur.execute("select * from student where sudept=?",(sudept,))
        data=cur.fetchall()
        return render_template('student.html',datas=data)
    else:
        return redirect(url_for('auth.login'))

@main.route('/suadds')
def suadds():
    if 'logged_in_admin' in session and session['logged_in_admin']:

        return render_template('suadds.html')
    else:
        return redirect(url_for('auth.login'))
    
@main.route('/addsu',methods=['POST','GET'])
def addsu():
    if request.method =="POST":
        date=datetime.now()
        date=date.strftime("%Y")[2::]
        name=request.form.get('name')
        sudept=request.form.get('dept')
        sec=request.form.get('sec')
        email=request.form.get('email')
        mobile=request.form.get('mobile')
        file=request.files['file']
        filename=mobile+'.png'
        if file:
            filepath="pro/static/css/images/"+filename
            file.save(filepath)
        try:
            path=session['db']
            cname=str(path).split("/")[2]
            cname=cname.split('.')[0]
            subar=mobile
            con=sql.connect(path)
            cor=con.cursor()
            cor.execute("select sno from student")
            data=cor.fetchall()
            print(data)
            role="student"
            if not data:   
                suid=cname[0]+date+sudept+sec+"1"
                cor.execute("insert into student(suid,suname,sudept,suemail,sumobile,cname,suphoto,supass,suclass,subar,role) values(?,?,?,?,?,?,?,?,?,?,?)",(suid,name,sudept,email,mobile,cname,filename,name,sec,subar,role))
            else:
                data=int(data[-1][0])+1
                suid=cname[0]+date+sudept+sec+str(data)
                cor.execute("insert into student(suid,suname,sudept,suemail,sumobile,cname,suphoto,supass,suclass,subar,role) values(?,?,?,?,?,?,?,?,?,?,?)",(suid,name,sudept,email,mobile,cname,filename,name,sec,subar,role))

            con.commit()
            con.close()
            return redirect(url_for('main.suprofiles'))
        except Exception as e:
            print("insert erorr",e)

        
    return redirect(url_for('main.suprofiles'))    


@main.route('/about')
def about():
    if 'logged_in_admin' in session and session['logged_in_admin']:
        
       

        return render_template('about.html')
    else:
        return redirect(url_for('auth.login'))     