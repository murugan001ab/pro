from flask import Flask, Response, render_template, Blueprint, session
import cv2
from pyzbar.pyzbar import decode
import sqlite3
from datetime import datetime
from playsound import playsound

face = Blueprint('face', __name__)



# Route to render the HTML page with a close button
@face.route('/bar')
# Function to decode barcode and register attendance

def bar():
    # Assuming 'db' is set in the session somewhere before accessing it
    
    # Function to generate frames with barcode detection
    # Route to display video stream with barcode detection
    
    # Render the template
    return render_template('i.html')
@face.route('/video_feed')
def video_feed():
    db = session.get('db')
    print(db)
    def gen_frames():
        cap = cv2.VideoCapture(0)
        while True:
            success, frame = cap.read()
            if not success:
                break
            # Convert frame to grayscale for better detection
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # Perform barcode decoding and attendance registration
            decode_and_register(gray)
            # Encode frame to JPEG
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    def decode_and_register(image):
        # Decode barcodes
        barcodes = decode(image)
        # Connect to SQLite database
        try:
            conn = sqlite3.connect(db)
            c = conn.cursor()
        except:
            print('connection error')
        d=datetime.now()
        date=d.strftime("%d/%m/%Y")
        time=d.strftime("%H:%M:%S")
        # Loop over detected barcodes
        for barcode in barcodes:
            # Extract barcode data
            barcode_data = barcode.data.decode("utf-8")
            # Fetch student or staff member details based on barcode data from the database
            c.execute("SELECT bar,date FROM attendance WHERE bar=?", (barcode_data,))
            row = c.fetchone()



            try:
                c.execute("SELECT sid,sname,sbar,role FROM staff WHERE sbar=?", (barcode_data,))
                sid = c.fetchone()
                print(sid)
            except:
                print('it is not staff')
            
            try:
                c.execute("SELECT suid,suname,subar,role FROM student WHERE subar=?", (barcode_data,))
                suid = c.fetchone()
                print(suid)
            except:
                print('it is not student')
            

            if row[0] is None and row[1]!=date:
                
                
                if sid: 
                    id=sid[0]
                    username=sid[1]
                    status="present"
                    role=sid[3]
                    bar=sid[2]            # Insert attendance record into the database        
                    c.execute("INSERT INTO attendance (id,username,date,stime_in,status,role,bar) VALUES (?,?,?,?,?,?,?)", (id,username,date,time,status,role,bar,))
                    print(f"Attendance registered for: {barcode_data}")
                    playsound('/home/hacker/Desktop/pro/static/sound/beep.mp3')

                elif suid: 
                    id=suid[0]
                    username=suid[1]
                    status="present"
                    role=suid[3]
                    bar=suid[2]            # Insert attendance record into the database        
                    c.execute("INSERT INTO attendance (id,username,date,stime_in,status,role,bar) VALUES (?,?,?,?,?,?,?)", (id,username,date,time,status,role,bar,))
                    print(f"Attendance registered for: {barcode_data}")
                    playsound('/home/hacker/Desktop/pro/static/sound/beep.mp3')

                else:
                    print("invalid id card")
                

            else:
                print('already registered')
        # Commit the transaction and close the connection
        conn.commit()
        conn.close()


    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
