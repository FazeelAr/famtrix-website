import os
from dotenv import load_dotenv
load_dotenv()
from flask import Flask, request, jsonify, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import smtplib

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class ContactRequest(db.Model):
    __tablename__ = 'contact_requests'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    phone = db.Column(db.String)
    message = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)



@app.route("/")
def index():
    return render_template('index.html')


@app.route("/about")
def about():
    return render_template('about.html')


@app.route("/contact", methods=['POST', 'GET'])
def contact():
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')
    
        new_contact = ContactRequest(
            full_name=full_name,
            email=email,
            phone=phone,
            message=message
        )

        db.session.add(new_contact)
        db.session.commit()

        ## email functionality ##
        sender = 'webfamtrix@gmail.com'
        reciever = 'famtrixsolutions@gmail.com'
        subject = f'Client email: {full_name}'
        text = f"Subject: {subject}\n\n{message}\n\nemail: {email} \n\nphone: {phone}"

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()

        server.login(sender, os.getenv('APP_PASSWORD'))
        server.sendmail(sender, reciever, text)

        print("email sent to the admin")


        return redirect(url_for('contact'))  # Or show success message
    
    return render_template('contact.html')



@app.route("/services")
def services():
    return render_template('services.html')


if __name__ == "__main__":
    app.run(debug=True, port=5000)
