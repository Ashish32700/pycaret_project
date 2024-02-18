import os
from flask import Flask, request, render_template, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from datetime import datetime
from flask_mail import Mail, Message
from pycaret_code import create_report
import pandas as pd


ALLOWED_EXTENSIONS = set(['csv'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

app = Flask(__name__)
app.config['SECRET_KEY'] = "tsfyguaistyatuis589566875623568956"
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'mlreports32700@gmail.com'
app.config['MAIL_PASSWORD'] = 'repd vkcu tvxc istb'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)

@app.route('/',methods=['GET', 'POST'])

#repd vkcu tvxc istb

 
def upload():
    if request.method == 'POST':
        min_clusters=request.form["min_clusters"]
        max_clusters=request.form["max_clusters"]
        methods_to_use=request.form.getlist('checkbox')
        scores=request.form.getlist('checkbox2')
        client_mail_id=request.form["email"]
        file = request.files['data']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename).replace(".csv","")
            new_filename = (filename+str(str(datetime.now()).replace(" ","").replace(".","").replace("-","").replace(":","")))+".csv"
            save_location = os.path.join(r'c:\Users\ASUS\Desktop\pycaret_assignment\data_bases',new_filename)
            file.save(save_location)
                        
            
            
            data=pd.read_csv('data_bases/'+str(new_filename))
            # methods_to_use=["kmeans","hclust","ap","meanshift","dbscan","sc"]
            verb=False
            for i in methods_to_use:
                create_report(str(i),data,scores,int(min_clusters),int(max_clusters),verb,new_filename)
                        
            
            
            
            
            msg = Message(subject='CLUSTERING REPORTS!', sender='noreply-mlreports32700@gmail.com', recipients=[client_mail_id])
            msg.body = "HERE ARE YOUR REPORTS FOR THE DATA-SET "+(str(filename)).capitalize()+" !!"
            
            
            directory = 'results'

            files_in_directory = os.listdir(directory)
            
            for i in files_in_directory:
                with app.open_resource("results\\"+str(i)) as fp:  
                    msg.attach(str(i), "application/csv", fp.read())
                     
            for i in files_in_directory:
                os.remove("results\\"+str(i))
            
            mail.send(msg)

            return("uploaded! Wait you will recieve your email soon!")
        else:
            return("did not get any file")
    else:
        return render_template('index.html')



if __name__ == '__main__':
    
    app.run(debug=True)
    
