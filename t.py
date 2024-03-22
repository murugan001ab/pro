from flask import Flask, Response, render_template,Blueprint
import cv2
from pyzbar.pyzbar import decode
import sqlite3

face = Blueprint('face',__name__)

# Connect to SQLite database
conn = sqlite3.connect('attendance.db')
c = conn.cursor()

# Create table if not exists
c.execute('''CREATE TABLE IF NOT EXISTS attendance (
             id INTEGER PRIMARY KEY,
             barcode TEXT,
             name TEXT,
             timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')

# Commit the transaction
conn.commit()

# Close the connection
conn.close()

# Function to decode barcode and register attendance
def decode_and_register(image):
    # Decode barcodes
    barcodes = decode(image)
    # Connect to SQLite database
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    # Loop over detected barcodes
    for barcode in barcodes:
        # Extract barcode data
        barcode_data = barcode.data.decode("utf-8")
        # Fetch student or staff member details based on barcode data from the database
        c.execute("SELECT name FROM attendance WHERE barcode=?", (barcode_data,))
        row = c.fetchone()
        if row is None:
            # Insert attendance record into the database
            c.execute("INSERT INTO attendance (barcode) VALUES (?)", (barcode_data,))
            print(f"Attendance registered for: {barcode_data}")
        else:
            print('alredy registerd')
    # Commit the transaction and close the connection
    conn.commit()
    conn.close()

# Function to generate frames with barcode detection
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

# Route to display video stream with barcode detection
@face.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Route to render the HTML page with a close button
@face.route('/bar')
def bar():
    return render_template('i.html')



