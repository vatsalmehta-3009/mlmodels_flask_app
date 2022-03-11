from flask import Blueprint,render_template,request
#import lin_reg_model
import pickle
from pickle import load
import sklearn
import psycopg2
KMB = Blueprint('KMB', __name__,template_folder='templates')

# KMF,KMH, KMP, KMD, KMB
# Form, History, Predictions, Delete, Blueprint

@KMB.route('/KMF')
def index():
    print(__name__)
    return render_template('KMF.html')

@KMB.route('/KMH',methods=['GET','POST'])
def history():
    conn = psycopg2.connect(host="localhost",dbname = 'mlmodels', port = 5432,  user="postgres", password=1234)
    cur = conn.cursor()
    cur.execute('select * from kmeans where delete_status = False;')
    rows = cur.fetchall()
    print(rows)
    return render_template('KMH.html', rows = rows)


@KMB.route("/km_ajax_delete",methods=["POST","GET"])
def km_ajax_delete():
    conn = psycopg2.connect(host="localhost",dbname = 'mlmodels', port = 5432,  user="postgres", password=1234)
    cur = conn.cursor()
    if request.method == 'POST':
        getid = request.form['string']
        print(getid)
        cur.execute('UPDATE kmeans SET delete_status = True WHERE id = {0};'.format(getid))
        conn.commit()       
        cur.close()
        msg = 'Record deleted successfully'   
    return msg

@KMB.route("/lr_ajax_update",methods=["POST","GET"])
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

@KMB.route('/KMP',methods=['GET','POST'])
def predictions():
    if request.method == 'POST':
        d = dict(request.form)
        model = load(open('kmeans/kmeansmodel.pkl', 'rb'))
        #scaler = load(open('log_reg/scaler.pkl', 'rb'))
        spending_score  = float(d['spending_score'])
        annual_inc = float(d['annual_inc'])
        pred = model.predict([[annual_inc,spending_score]])[0]
        print('*'*20)
        print(pred)
        print('*'*20)
        conn = psycopg2.connect(host="localhost",dbname = 'mlmodels', port = 5432,  user="postgres", password=1234)
        cur = conn.cursor()
        cur.execute(f'''INSERT INTO kmeans (annual_inc, spending_score, pred)
                    VALUES ({annual_inc},{spending_score},{pred}); ''')
        conn.commit()
        print('Recorded!')
    return render_template('KMF.html',pred =pred)
