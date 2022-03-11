from flask import Blueprint,render_template,request
#import lin_reg_model
import pickle
import sklearn
import psycopg2
LRB = Blueprint('LRB', __name__,template_folder='templates')

# LRF,LRH, LRP, LRD, LRB
# Form, History, Predictions, Delete, Blueprint

@LRB.route('/LRF')
def index():
    print(__name__)
    return render_template('LRF.html')

@LRB.route('/LRH',methods=['GET','POST'])
def history():
    conn = psycopg2.connect(host="localhost",dbname = 'mlmodels', port = 5432,  user="postgres", password=1234)
    cur = conn.cursor()
    cur.execute('select * from linear_regression where delete_status = False;')
    rows = cur.fetchall()
    print(rows)
    return render_template('LRH.html', rows = rows)


@LRB.route("/lr_ajax_delete",methods=["POST","GET"])
def lr_ajax_delete():
    conn = psycopg2.connect(host="localhost",dbname = 'mlmodels', port = 5432,  user="postgres", password=1234)
    cur = conn.cursor()
    if request.method == 'POST':
        getid = request.form['string']
        print(getid)
        cur.execute('UPDATE linear_regression SET delete_status = True WHERE id = {0};'.format(getid))
        conn.commit()       
        cur.close()
        msg = 'Record deleted successfully'   
    return msg

@LRB.route("/lr_ajax_update",methods=["POST","GET"])
def lr_ajax_update():
    conn = psycopg2.connect(host="localhost",dbname = 'mlmodels', port = 5432,  user="postgres", password=1234)
    cur = conn.cursor()
    if request.method == 'POST':
        print('*'*30)
        string = request.form['string']
        
        yoe = request.form['yoe_ajax']
        
        #print(string,txtname,txtdepartment,txtphone)
        print(string)
        cur.execute("UPDATE linear_regression SET yoe = %s, salary = %s WHERE id = %s ", [yoe, yoe, string])
        conn.commit()       
        cur.close()
        msg = 'Record successfully Updated'   
    return msg

@LRB.route('/LRP',methods=['GET','POST'])
def predictions():
    if request.method == 'POST':
        print(request.form['yoe'])
        dbfile = open('lin_reg/lin_reg_model', 'rb')     
        db = pickle.load(dbfile)
        try:
            x = db.predict([[float(request.form['yoe'])]])
        except:
            return 'enter valid values.'
        x = round(x[0][0])
        conn = psycopg2.connect(host="localhost",dbname = 'mlmodels', port = 5432,  user="postgres", password=1234)
        cur = conn.cursor()
        cur.execute(f'''INSERT INTO linear_regression (yoe, salary)
                    VALUES ({request.form['yoe']},{x}); ''')
        conn.commit()
    return render_template('LRF.html',prediction = x,yoe=request.form['yoe'])
