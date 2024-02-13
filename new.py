from PIL import Image, ImageDraw, ImageFont
import barcode
from barcode.writer import ImageWriter
import os

class idcard():
    def barcodeu(id):
        code128=barcode.get_barcode_class('code128')
        idcardn=11111111111+id
        bar=code128(str(idcardn),writer=ImageWriter())
        path=os.path.join("static/id/userbar/",str(id))
        bar.save(path)
    def idcard(cname,cadd,cnum,clogo,uphoto,uname,urole,unum,ubar):
        font1=ImageFont.truetype("static/font/Barlow-Black.ttf",size=18)
        font3=ImageFont.truetype("static/font/Roboto-Light.ttf",size=12)
        font2=ImageFont.truetype("static/font/Barlow-Black.ttf",size=13)

        #open background image
        width=300
        hight=500
        id=Image.open('static/id/bc.jpeg')
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
        position= ((image_width - text_width) // 2)-v+20,40
        draw.text(position, cadd, fill="black", font=font3)
        #draw the compay number
        cnum=cnum
        text_width=draw.textlength(cnum)
        image_width, image_height = id.size
        position= ((image_width - text_width) // 2)-v,60
        draw.text(position, cnum, fill="black", font=font3)
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
        position= ((image_width - text_width) // 2)-20,290
        draw.text(position, uname, fill="black", font=font1)
        #user role draw
        urole=urole
        draw.text((125,310), urole, fill="black", font=font2)
        #draw a user phone num
        unum=unum
        draw.text((80,330), unum, fill="black", font=font2)
        #draw user barcode
        ubar=Image.open(ubar)
        ubar=ubar.resize((200,70),resample=Image.BICUBIC).crop((0,0,190,50))
        id.paste(ubar,(50,360))

        id.show()
    
    cname="ST.jospesh "
    cadd="70,south street,irulankuppa,607106"
    cnum="Phone no:1234567890"
    clogo='static/id/clogo/log.png'
    uphoto='static/id/userphoto/pavi.jpg'
    uname="M.MURUGAN"
    uid=1
    urole="(Student)"
    unum="Phone no:12345678990"
    ubar='static/id/userbar/1.png'

    barcodeu(uid)
    idcard(cname,cadd,cnum,clogo,uphoto,uname,urole,unum,ubar)

