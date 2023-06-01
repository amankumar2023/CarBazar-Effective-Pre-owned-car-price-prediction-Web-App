from flask import Flask , render_template, request
import pickle
import numpy as np
# from flask import Flask, render_template, request, redirect, url_for, flash
from flaskext.mysql import MySQL
import pymysql

import warnings 
import sys
if not sys.warnoptions:
    warnings.simplefilter("ignore")
warnings.filterwarnings("ignore",category=DeprecationWarning)

app = Flask(__name__,template_folder='template')
app.secret_key = "CAR_BAZZAR"

mysql = MySQL()
   
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'car_bazzar'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


model=pickle.load(open('model_train.pkl','rb'))

def helper(loc,fuel,tran,own):
    loc1 = 0
    loc2 = 0
    loc3 = 0
    loc4 = 0
    loc5 = 0
    loc6 = 0
    loc7 = 0
    loc8 = 0
    loc9 = 0
    loc10 = 0
    if(loc == "Bangalore"):
        loc1 = 1
    elif loc== "Chennai":
        loc2 = 1
    elif loc== "Coimbatore":
        loc3 = 1
    elif loc== "Delhi":
        loc4 = 1
    elif loc== "Hyderabad":
        loc5 = 1
    elif loc== "Jaipur":
        loc6 = 1
    elif loc== "Kochi":
        loc7 = 1
    elif loc== "Kolkata":
        loc8 = 1
    elif loc== "Mumbai":
        loc9 = 1
    else:
        loc10=1
    f1=0
    f2=0
    f3=0
    if(fuel == "Diesel"):
        f1 = 1
    elif fuel=="LPG":
        f2 = 1
    else:
        f3=1
    auto=0
    man=0
    if(tran=="Auto"):
        auto=1
    else:
        manual=1
    first=0
    second=0
    third=0
    four=0
    if(own == 'First'):
        first=1
    elif own == 'Second':
        second=1
    elif own == 'Third':
        third=1
    else:
        four
    return loc1,loc2,loc3,loc4,loc5,loc6,loc7,loc8,loc9,loc10,f1,f2,f3,auto,man,first,second,third,four


@app.route('/')
def Index():
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
 
    cur.execute('SELECT * FROM cars')
    data = cur.fetchall()
  
    cur.close()
    return render_template('index.html', cars = data)

@app.route('/index')
def carform():
    return render_template('wel.html')


@app.route('/predict',methods=['POST'])
def fun():
    name = request.form["Name"]
    mb = request.form["Mob"]
    cr = request.form["car_mod"]
    yr = request.form["yr"]
    km = request.form["km"]
    mil = request.form["mil"]
    en_cc = request.form["en_cc"]
    pwr = request.form["pwr"]
    seat = request.form["seat"]
    loc = request.form["loc"]
    fuel = request.form["fuel"]
    tran = request.form["tran"]
    own = request.form["own"]
    yr = int(yr)
    km = int(km)
    mil= float(mil)
    en_cc = float(en_cc)
    pwr = float(pwr)
    seat = float(seat) 

    loc1,loc2,loc3,loc4,loc5,loc6,loc7,loc8,loc9,loc10,f1,f2,f3,auto,man,first,second,third,four = helper(loc,fuel,tran,own)
    arr = np.array([yr,km,mil,en_cc,pwr,seat,loc1,loc2,loc3,loc4,loc5,loc6,loc7,loc8,loc9,loc10,f1,f2,f3,auto,man,first,second,third,four])
    # pred=model.predict([[2013,10670,15.20,1968.0,140.80,5.0,0,0,1,0,0,0,0,0,0,0,1,0,0,1,0,0,0,1,0]])
    pred = model.predict(arr.reshape(1,-1))                        #predicting our result 
    # return render_template('res.html', data=pred)
    x=float(pred)
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    # email = request.form['email']
    cur.execute("INSERT INTO cars (name,phone_number,car_name,year,kilometer_driven,fuel_type,transmission,owner_type,mileage_kmpl,engine_cc,power_bhp,seats,location,price) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (name,mb,cr,yr,km,fuel,tran,own,mil,en_cc,pwr,seat,loc,x))
    conn.commit()

    return render_template('wel.html',prediction_text="You Can Sell the Car at {} lakhs ".format(pred))
   
    # arr=np.array([3366	,2200.0	,135.0	,360.0	,1.0	,1	,1	,1	,0	,0	,0	,1	,0	,1	,0	,0])
    # arr=np.array([app_income,coapp_income	,loan_amount	,la_term	,cr_history	,gender	,married	,dependents_0	,dependents_1	,dependents_2	,dependents_3	,education	,self_emp	,p_rural	,p_semi_urban	,p_urban])
    # pred= model.predict(arr.reshape(1,-1))
    # return render_template('prediction_page.html', data=pred)
    


if __name__ == "__main__":
    app.run(port=3000,debug=True)