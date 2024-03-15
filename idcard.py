from PIL import Image, ImageDraw, ImageFont
import barcode
from barcode.writer import ImageWriter
from flask import Flask,Blueprint,render_template,request,Response,url_for,redirect,flash,session
import sqlite3 as sql
import os

idc=Blueprint('idc',__name__)
def barcodeu(id):
    code128=barcode.get_barcode_class('code128')
    idcardn=id
    bar=code128(str(idcardn),writer=ImageWriter())
    path=os.path.join("pro/static/id/userbar/",str(id))
    bar.save(path)
def idcardu(idp,cname,cadd,cnum,clogo,uphoto,uname,urole,unum,ubar):
    font1=ImageFont.truetype("pro/static/font/Barlow-Black.ttf",size=18)
    font3=ImageFont.truetype("pro/static/font/Roboto-Light.ttf",size=12)
    font2=ImageFont.truetype("pro/static/font/Barlow-Black.ttf",size=13)
    #open background image
    width=300
    hight=500
    id=Image.open('pro/static/id/bc.jpeg')
    id=id.resize((width,hight))
    draw=ImageDraw.Draw(id)
    #company name draw
    cname=cname
    text_width=draw.textlength(cname)
    if text_width<220 and text_width>=200:
        v=90
    elif text_width<200 and text_width>=180 :
        v=85
    elif text_width<180 and text_width>=160:
        v=75
    elif text_width<160 and text_width>=140:
        v=70
    elif text_width<140 and text_width>=120:
        v=65
    elif text_width<120 and text_width>=90:
        v=55
    elif text_width<90 and text_width>=60:
        v=35
    else:
        v=30
    image_width, image_height = id.size
    position= ((image_width - text_width) // 2)-v-10,10
    draw.text(position, cname, fill="black", font=font1)
    #green line draw
    draw.line((10,37,200,37),fill="green")
    #company Adress draw
    cadd=cadd
    text_width=draw.textlength(cadd)
    image_width, image_height = id.size
    position= ((image_width - text_width) // 2)-v+10,40
    draw.text(position, cadd, fill="black", font=font3)
    #draw the compay number
    num='Cantact:'+str(cnum)
    text_width=draw.textlength(num)
    image_width, image_height = id.size
    position= ((image_width - text_width) // 2)-v,60
    draw.text(position, num, fill="black", font=font3)
    #compay logo paste
    clogo=clogo
    logo=Image.open(clogo)
    logo=logo.resize((67,65),resample=Image.LANCZOS)
    id.paste(logo,(220,20))
    #user photo paste 
    uphoto=uphoto
    photo=Image.open(uphoto)
    photo=photo.resize((160,170),resample=Image.BICUBIC)
    id.paste(photo,(70,120))
    #draw user name
    uname=uname
    text_width=draw.textlength(uname)
    image_width, image_height = id.size
    position= ((image_width - text_width) // 2)-10,290
    draw.text(position, uname, fill="black", font=font1)
    #user role draw
    urole=urole
    draw.text((135,310), urole, fill="black", font=font2)
    #draw a user phone num
    num="Phone no:"+str(unum)
    draw.text((80,330), num, fill="black", font=font2)
    #draw user barcode
    ubar=Image.open(ubar)
    ubar=ubar.resize((200,70),resample=Image.BICUBIC).crop((0,0,190,50))
    id.paste(ubar,(50,360))
    path='pro/static/id/'+idp+'.png'
    id.save(path)


@idc.route('/idcard')
def idcard():
    if 'logged_in_admin' in session and session["logged_in_admin"]:
       
        db=session['db']
        cname=str(db).split("/")[2]
        cname=cname[:-3]
        print(cname)
        try:
            con=sql.connect("org.db")
            cur=con.cursor()
            cur.execute('select name,mobile,cadd,clogo from admins where name=?',(cname,))
            cdata=cur.fetchall()
            for i in cdata:
                cname=i[0]
                cnum=i[1]
                cadd=i[2]
                clogo='pro/static/id/clogo/'+str(i[3])
            
            con.close()
        except Exception as e:
            print(e)
        selected=request.args.get('list')
        if selected=="staff":
            con=sql.connect(session['db'])
            cur=con.cursor()
            cur.execute('select sid,sname,smobile,sbar,role from staff')
            data=cur.fetchall()
            print(data)
            for j in data:
                id=j[0]
                uname=j[1]
                unum=j[2]
                sbar=j[3]
                urole=j[4]
                uphoto= "pro/static/css/images/"+str(unum)+'.png'

                ubar="pro/static/id/userbar/"+str(sbar)+'.png'
                print(cname,cadd,cnum,clogo,uphoto,uname,urole,unum,ubar)
                barcodeu(sbar)
                idcardu(id,cname,cadd,cnum,clogo,uphoto,uname,urole,unum,ubar)
            return render_template('idcard.html',data=data)
        else:
            con=sql.connect(session['db'])
            cur=con.cursor()
            cur.execute('select suid,suname,sumobile,subar,role from student')
            data=cur.fetchall()
            print(data)
            for j in data:
                idp=j[0]
                uname=j[1]
                unum=j[2]
                sbar=j[3]
                urole=j[4]
                uphoto= "pro/static/css/images/"+str(unum)+'.png'

                ubar="pro/static/id/userbar/"+str(sbar)+'.png'
                print(cname,cadd,cnum,clogo,uphoto,uname,urole,unum,ubar)
                barcodeu(sbar)
                idcardu(idp,cname,cadd,cnum,clogo,uphoto,uname,urole,unum,ubar)
            return render_template('idcard.html',data=data)            
    return render_template('auth.login')
    

