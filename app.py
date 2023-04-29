from flask import Flask,render_template,request
import imaplib
import email
import os
import pandas as pd
import numpy as np
from datetime import datetime

app=Flask(__name__)
app.secret_key = "ABAA"

@app.route("/",methods=['GET','POST'])
def upload():
    if request.method == 'POST':
        # Connect to mail account using SSL and select inbox folder
        mail = imaplib.IMAP4_SSL("imap.gmail.com", 993)
        Email=request.form['Emails']
        password=request.form['Pass']
        mail.login(Email, password)
        mail.select("Inbox")

        # Filter emails by start date and end date
        sdate = request.form['stdate']
        edate = request.form['endate']
        var= datetime.strptime(sdate, "%Y-%m-%d")
        var1= datetime.strptime(edate, "%Y-%m-%d")
        start = var.strftime("%d-%b-%Y")
        end = var1.strftime("%d-%b-%Y")
        start_date = start
        end_date = end
        # subject filter
        subjects = request.form['Subjectss']
        sub =subjects
        criteria = f"(SUBJECT {sub}) (SENTSINCE {start_date}) (SENTBEFORE {end_date})"
        type, data = mail.search(None, criteria)
        # Retrieve email content and attachments
        for num in data[0].split():
            typ, data = mail.fetch(num, "(RFC822)")
            raw_email = data[0][1]
            email_message = email.message_from_string(raw_email.decode("utf-8"))
            # Iterate over attachments and save them to local directory
            for part in email_message.walk():
                if part.get_content_maintype() == 'multipart':
                    continue
                if part.get('Content-Disposition') is None:
                    continue
                file_name = part.get_filename()
                print(file_name)
                try:
                    if file_name.endswith(".xlsx"):
                        if file_name.endswith(".xlsx"):
                # Save csv files to local directory
                            file_path = os.path.join(r"static\excel", file_name)
                            with open(file_path, "wb") as fp:
                                fp.write(part.get_payload(decode=True))
                                fp.close()
                except:
                    continue
    # dir_list = os.listdir(r"C:\Users\Hostbooks\Desktop\EmailAutoFlask\static\excel")
    # path = r"C:\Users\Hostbooks\Desktop\EmailAutoFlask\static\excel/"
    entries = os.listdir(r"static\excel")
    return render_template("Excel.html",entries=entries)

@app.route('/view/<path>')
def view(path):
   
    filepath="static/excel/"+path
    print("path is ",filepath)
    # file=request.url(filepath)
    # file=""
    # Parse the data as a Pandas DataFrame type
    data = pd.read_excel(filepath)
    # data = pd.read_excel(dfs)
    df = data.replace(np.NaN, '')
    # Return HTML snippet that will render the table
    return df.to_html()
@app.route("/delete/")
def deleteAll():
    dir = 'static\excel'
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))
    return render_template("Excel.html")
@app.route("/remove/<path>")
def remove(path):
    file="static/excel/"+path
    os.remove("static/excel/"+path)
    entries = os.listdir(r"static\excel")
    return render_template("Excel.html",entries=entries) 

if __name__=='__main__':
    app.run('0.0.0.0',debug=True)