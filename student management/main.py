from flask import Flask,render_template,request,session,redirect,url_for,flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user,logout_user,login_manager,LoginManager
from flask_login import login_required,current_user
import json

# MY db connection
local_server= True
app = Flask(__name__)
app.secret_key='kusumachandashwini'


# this is for getting unique user access
login_manager=LoginManager(app)
login_manager.login_view='login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



# app.config['SQLALCHEMY_DATABASE_URL']='mysql://username:password@localhost/databas_table_name'
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:@localhost/accelerometer'
db=SQLAlchemy(app)

class DataSource(db.Model):
    cid=db.Column(db.Integer,primary_key=True)
    source_name=db.Column(db.String(100))

class Attendence(db.Model):
    aid=db.Column(db.Integer,primary_key=True)
    XAxis=db.Column(db.String(100))
    attendance=db.Column(db.Integer())

class Trig(db.Model):
    tid=db.Column(db.Integer,primary_key=True)
    XAxis=db.Column(db.String(100))
    action=db.Column(db.String(100))
    timestamp=db.Column(db.String(100))


class User(UserMixin,db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(50))
    email=db.Column(db.String(50),unique=True)
    password=db.Column(db.String(1000))





class AccelerometerData(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    XAxis=db.Column(db.String(50))
    YAxis=db.Column(db.String(50))
    ZAxis=db.Column(db.String(50))
    latitude=db.Column(db.String(50))
    longitude=db.Column(db.String(50))
    data_source=db.Column(db.String(100))


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/accelerometerdetails')
def accelerometerdetails():
    query=db.engine.execute(f"SELECT * FROM `accelerometerData`")
    return render_template('accelerometerdetails.html',query=query)

@app.route('/triggers')
def triggers():
    query=db.engine.execute(f"SELECT * FROM `trig`")
    return render_template('triggers.html',query=query)

@app.route('/dataSource',methods=['POST','GET'])
def dataSource():
    if request.method=="POST":
        dept=request.form.get('dept')
        query=DataSource.query.filter_by(source_name=dept).first()
        if query:
            flash("DataSource Already Exist","warning")
            return redirect('/dataSource')
        dep=DataSource(source_name=dept)
        db.session.add(dep)
        db.session.commit()
        flash("DataSource Added","success")
    return render_template('datasource.html')

@app.route('/addattendance',methods=['POST','GET'])
def addattendance():
    query=db.engine.execute(f"SELECT * FROM `accelerometerData`")
    if request.method=="POST":
        XAxis=request.form.get('XAxis')
        attend=request.form.get('attend')
        print(attend,XAxis)
        atte=Attendence(XAxis=XAxis,attendance=attend)
        db.session.add(atte)
        db.session.commit()
        flash("Attendance added","warning")


    return render_template('attendance.html',query=query)

@app.route('/search',methods=['POST','GET'])
def search():
    if request.method=="POST":
        XAxis=request.form.get('x')
        bio=AccelerometerData.query.filter_by(XAxis=XAxis).first()
        attend=Attendence.query.filter_by(XAxis=XAxis).first()
        return render_template('search.html',bio=bio,attend=attend)

    return render_template('search.html')

@app.route("/delete/<string:id>",methods=['POST','GET'])
@login_required
def delete(id):
    db.engine.execute(f"DELETE FROM `accelerometerdata` WHERE `id`={id}")
    flash("Slot Deleted Successful","danger")
    return redirect('/accelerometerdetails')


@app.route("/edit/<string:id>",methods=['POST','GET'])
@login_required
def edit(id):
    dept=db.engine.execute("SELECT * FROM `data_source`")
    posts=AccelerometerData.query.filter_by(id=id).first()
    if request.method=="POST":
        XAxis=request.form.get('XAxis')
        YAxis=request.form.get('YAxis')
        ZAxis=request.form.get('ZAxis')
        latitude=request.form.get('latitude')
        longitude=request.form.get('longitude')
        query=db.engine.execute(f"UPDATE `accelerometerdata` SET `XAxis`='{XAxis}',`YAxis`='{YAxis}',`ZAxis`='{ZAxis}',`latitude`='{latitude}',`longitude`='{longitude}''")
        flash("Slot is Updates","success")
        return redirect('/accelerometerdetails')

    return render_template('edit.html',posts=posts,dept=dept)


@app.route('/signup',methods=['POST','GET'])
def signup():
    if request.method == "POST":
        username=request.form.get('username')
        email=request.form.get('email')
        password=request.form.get('password')
        user=User.query.filter_by(email=email).first()
        if user:
            flash("Email Already Exist","warning")
            return render_template('/signup.html')
        encpassword=generate_password_hash(password)

        new_user=db.engine.execute(f"INSERT INTO `user` (`username`,`email`,`password`) VALUES ('{username}','{email}','{encpassword}')")

        # this is method 2 to save data in db
        # newuser=User(username=username,email=email,password=encpassword)
        # db.session.add(newuser)
        # db.session.commit()
        flash("Signup Succes Please Login","success")
        return render_template('login.html')



    return render_template('signup.html')

@app.route('/login',methods=['POST','GET'])
def login():
    if request.method == "POST":
        email=request.form.get('email')
        password=request.form.get('password')
        user=User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password,password):
            login_user(user)
            flash("Login Success","primary")
            return redirect(url_for('index'))
        else:
            flash("invalid credentials","danger")
            return render_template('login.html')

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logout SuccessFul","warning")
    return redirect(url_for('login'))



@app.route('/addaccelerometer',methods=['POST','GET'])
@login_required
def addaccelerometer():
    dept=db.engine.execute("SELECT * FROM `data_source`")
    if request.method=="POST":
        XAxis=request.form.get('XAxis')
        YAxis=request.form.get('YAxis')
        ZAxis=request.form.get('ZAxis')
        latitude=request.form.get('latitude')
        longitude=request.form.get('longitude')
        sourceName=request.form.get('dataSource')
        #num=request.form.get('num')
        query=db.engine.execute(f"INSERT INTO `accelerometerdata` (`XAxis`,`YAxis`,`ZAxis`,`latitude`,`longitude`, `source_name`) VALUES ('{XAxis}','{YAxis}','{ZAxis}','{latitude}','{longitude}', '{sourceName}')")


        flash("Acceleration Data Added","info")


    return render_template('accelerometer.html',dept=dept)
@app.route('/test')
def test():
    try:
        Test.query.all()
        return 'My database is Connected'
    except:
        return 'My db is not Connected'


app.run(debug=True)    