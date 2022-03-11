import psycopg2
from flask import Flask,render_template
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from kmeans.routes import KMB

from lin_reg.routes import LRB
from log_reg.routes import LGRB

app = Flask(__name__)
app.register_blueprint(LRB)
app.register_blueprint(LGRB)
app.register_blueprint(KMB) 
@app.route('/')
def hello_world():
	return render_template('index.html')

if __name__ == '__main__':
	app.run(debug=True)

