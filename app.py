from flask import Flask, render_template, request,send_from_directory, jsonify, url_for
from flask import redirect
from flask_mail import Mail, Message

# from scripts import helper
import requests


import json

import time
import os
import pickle


application = Flask(__name__)

mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": os.environ['EMAIL_USER'],
    "MAIL_PASSWORD": os.environ['EMAIL_PASSWORD']
}

application.config.update(mail_settings)
mail = Mail(application)



# def setup_app(application):
#    # All your initialization code
   
#    helper.setup()


# setup_app(application)



@application.route("/")
def hello():
    return render_template('index.html')




@application.route('/submit_dataset',methods=["POST"])
def submit_dataset():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        file_name=str(int(time.time()))+".csv"
        file.save(file_name)



        name=str(request.form['name'])
        email=str(request.form['email'])
        N=str(request.form['N'])
        k=str(request.form['k'])
        randmx=str(request.form['randmx'])
        d_t=str(request.form['d_t'])
        message=str(request.form['message'])

        string_to_mail=""
        string_to_mail+="name = "+name+", email="+email+"\n"
        string_to_mail+="N= "+N+", k="+k+"\n"
        string_to_mail+="randmx="+randmx+", d_t="+d_t+"\n"
        string_to_mail+="message = "+message        



        with application.app_context():
            msg = Message(subject="Need Augmentation",
                          sender=application.config.get("MAIL_USERNAME"),
                          recipients=["ashhadulislam@gmail.com"], # replace with your email for testing
                          body=string_to_mail)
            print("Opening file",file_name)
            with application.open_resource(file_name) as fp:
                msg.attach(file_name, "text/csv",  fp.read()) #attaches the submitted file to the email
            print('file attached successfully')
            mail.send(msg)




        os.remove(file_name)
        print("removed file")


    
            

    
    
    return render_template('onsubmit.html')


@application.route('/homepage')
def homepage():    
    return render_template('index.html')


    


if __name__ == "__main__":
    
    application.run(debug=True)
