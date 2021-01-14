from flask import Flask,request,render_template,redirect,url_for
import pymongo
from pymongo import MongoClient
from datetime import datetime
cluster= MongoClient("mongodb+srv://pardhu:Partha@realmcluster.w2v4d.mongodb.net/<dbname>?retryWrites=true&w=majority")
db=cluster["Liver_disease_prediction"]
collecion= db["Data"]
app = Flask(__name__) 

from joblib import load
model=load('navieliver.save')

@app.route('/')
def home():
	return render_template('index.html')
@app.route('/liverdis',methods=['post'])
def liver():
	xt=[[float(x) for x in request.form.values()]]
	print(xt)
	predic=model.predict(xt)
	now = datetime.now()
	date_time = now.strftime("%d/%m/%Y, %H:%M:%S")
	collecion.insert_one({
		"time": str(date_time),
		"age": str(xt[0][0]),
		"gender": str(xt[0][1]),
		"Total_Bilirubin": str(xt[0][2]),
		"Direct_Bilirubin": str(xt[0][3]),
		"Alkaline_Phosphotase": str(xt[0][4]),
		"Alamine_Aminotransferase": str(xt[0][5]),
		"Aspartate_Aminotransferase": str(xt[0][6]),
		"Total_Protiens": str(xt[0][7]),
		"Albumin": str(xt[0][8]),
		"Albumin_and_Globulin_Ratio": str(xt[0][9]),
		"Resut":str(predic[0]),
		})
	print(predic)
	if(predic[0]):
		return render_template('liverdisease.html')
	else:
		return render_template('nonliverdisease.html')
	

	

	

if __name__ == '__main__': 
	app.run(host='0.0.0.0', port=5000) 
	
