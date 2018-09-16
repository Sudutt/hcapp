from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from send_email import send_email
from sqlalchemy.sql import func

app=Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.config['SQLALCHEMY_DATABASE_URI']="postgresql://postgres:postgres123@localhost:5432/height_collector"
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://rxcnolbihnslfk:9279249dbcc919c357b7ecb0e12145b962d0972c159234facba2285af7e31be3@ec2-23-23-110-26.compute-1.amazonaws.com:5432/df4vcj92crgjp0?sslmode=require"
db=SQLAlchemy(app)

class Data(db.Model):
    __tablename__="data"
    id=db.Column(db.Integer, primary_key=True)
    email_=db.Column(db.String(120), unique=True)
    height_=db.Column(db.Float)

    def __init__(self, email_, height_):
        self.email_=email_
        self.height_=height_

@app.route('/')
def index():
    return render_template("index.html")

@app.route("/success",methods=["POST"])
def success():
    if request.method=="POST":
        email=request.form["email-name"]
        height=request.form["height-name"]
        #print(email,height)
        if(db.session.query(Data).filter(Data.email_==email).count()==0):
            data=Data(email,height)
            db.session.add(data)
            db.session.commit()

            average_height=db.session.query(func.avg(Data.height_)).scalar()
            average_height=round(average_height,1)
            #print(average_height)
            count=db.session.query(Data.height_).count()
            send_email(email,height,average_height,count)
            return render_template("success.html")
        else:
            return render_template("index.html",
            text="Seems like we've got something from that email address already!")

if __name__=="__main__":
    app.run(debug=True)