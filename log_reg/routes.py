from flask import Blueprint,render_template,request
#import lin_reg_model
import pickle
from pickle import load
import sklearn
import psycopg2
LGRB = Blueprint('LGRB', __name__,template_folder='templates')

# LGRF,LGRH, LGRP, LGRD, LGRB
# Form, History, Predictions, Delete, Blueprint

@LGRB.route('/LGRF')
def index():
    print(__name__)
    return render_template('LGRF.html')

@LGRB.route('/LGRH',methods=['GET','POST'])
def history():
    conn = psycopg2.connect(host="localhost",dbname = 'mlmodels', port = 5432,  user="postgres", password=1234)
    cur = conn.cursor()
    cur.execute('select * from logistic_regression where delete_status = False;')
    rows = cur.fetchall()
    print(rows)
    return render_template('LGRH.html', rows = rows)

@LGRB.route("/lgr_ajax_delete",methods=["POST","GET"])
def lgr_ajax_delete():
    conn = psycopg2.connect(host="localhost",dbname = 'mlmodels', port = 5432,  user="postgres", password=1234)
    cur = conn.cursor()
    if request.method == 'POST':
        getid = request.form['string']
        print(getid)
        cur.execute('UPDATE logistic_regression SET delete_status = True WHERE id = {0};'.format(getid))
        conn.commit()       
        cur.close()
        msg = 'Record deleted successfully'   
    return msg

@LGRB.route("/lr_ajax_update",methods=["POST","GET"])
def lr_ajax_update():
    conn = psycopg2.connect(host="localhost",dbname = 'mlmodels', port = 5432,  user="postgres", password=1234)
    cur = conn.cursor()
    if request.method == 'POST':
        print('*'*30)
        string = request.form['string']
        yoe = request.form['yoe_ajax']
        txtphone = request.form['salary_ajax']
        #print(string,txtname,txtdepartment,txtphone)
        print(string)
        cur.execute("UPDATE linear_regression SET yoe = %s, salary = %s WHERE id = %s ", [yoe, txtphone, string])
        conn.commit()       
        cur.close()
        msg = 'Record successfully Updated'   
    return msg

@LGRB.route('/LGRP',methods=['GET','POST'])
def predictions():
    if request.method == 'POST':
        d = dict(request.form)
        model = load(open('log_reg/model.pkl', 'rb'))
        scaler = load(open('log_reg/scaler.pkl', 'rb'))
        age  = float(d['age'])
        salary = float(d['salary'])
        gender = 1 if d['gender']=='male' else 0
        pred = model.predict(scaler.transform([[age,salary,gender]]))[0]
        #buy_status = 'will buy' if pred==[1] else 'will not buy'
        print('*'*20)
        print(pred)
        print('*'*20)
        conn = psycopg2.connect(host="localhost",dbname = 'mlmodels', port = 5432,  user="postgres", password=1234)
        cur = conn.cursor()
        cur.execute(f'''INSERT INTO logistic_regression (age, salary, gender,buy_status)
                    VALUES ({age},{salary},'{d['gender']}',{pred}); ''')
        conn.commit()
        print('Recorded!')
    return render_template('LGRF.html',pred = pred)
