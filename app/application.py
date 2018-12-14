from flask import Flask, render_template, request, url_for, redirect
from flask_mysqldb import MySQL


app = Flask(__name__)

#configuring database
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123456789'
app.config['MYSQL_DB'] = 'train'

mysql=MySQL(app)
@app.route("/")
def home():
    title = "Welcome To My Train Website"
    return render_template("home.html", title=title)

@app.route("/station", methods=['GET','POST'])
def find():
    if request.method == 'POST':
        od=request.form
        origin=od['origin']
        destination=od['destination']
        cur = mysql.connection.cursor()
        value = cur.execute("SELECT * FROM station WHERE origin=%s AND destination=%s ",(origin, destination))
        if value>0:
            trains = cur.fetchall()
            return render_template("user.html", trains=trains, origin=origin, destination=destination)
        else :
            um='Could Not Find Any Train'
            dm='Please Try Again !!!!!!'
            return render_template("error.html", um=um, dm=dm)
        cur.close()
    return render_template("find.html")



@app.route("/book", methods=['GET','POST'])
def book():
    if request.method =='POST':
        detail=request.form
        name=detail['name']
        gender_choise=detail['gender_choise']
        email=detail['email']
        mobile=detail['mobile']
        age=detail['age']
        train_id=detail['train_id']
        cur = mysql.connection.cursor()
        cur1 = mysql.connection.cursor()
        cur1.execute("INSERT INTO passenger (name, sex, email, mobile, age) VALUES (%s, %s, %s, %s, %s)",(name,gender_choise,email,mobile,age))
        mysql.connection.commit()
        value = cur.execute("SELECT * FROM station WHERE id= {}".format(train_id))
        value1 = cur1.execute("SELECT * FROM passenger WHERE mobile={}".format(mobile))
        if value > 0:
            train_detail=cur.fetchall()
            p_id = cur1.fetchone()
            return render_template("payment.html", train_detail=train_detail, detail=detail, p_id=p_id)
        else :
            um='Could Not Find Any Train'
            dm='Please Try Again !!!!!!'
            return render_template("error.html", um=um, dm=dm)
        cur.close()
        cur1.close()
    return render_template("book.html")



@app.route('/payment/<train_id>/<id>')
def payment(train_id,id):
    cur = mysql.connection.cursor()
    cur.execute('''UPDATE passenger SET train_id=%s WHERE id=%s''',(train_id,id))
    mysql.connection.commit()
    cur.close()
    um="Your Ticket is Successfully Booked , You can see your Ticket Status in the 'Ticket Status' on Home page. You can navigate to home page by clicking on Home button in navigatio bar"
    dm='Happy Journy !!! visit Again !!!'
    return render_template("success.html", um=um, dm=dm)




@app.route("/status",methods=['GET','POST'])
def status():
    if request.method=='POST':
        detail=request.form
        id=detail['pid']
        cur = mysql.connection.cursor()
        value=cur.execute('''SELECT * FROM passenger WHERE id={}'''.format(id))
        if value>0:
            p_detail = cur.fetchone()
            if p_detail[6]!=0 :
                value=cur.execute("SELECT * FROM station WHERE id={}".format(p_detail[6]))
                t_detail = cur.fetchone()
                return render_template("detail.html", p_detail=p_detail, t_detail=t_detail)
            else:
                um='Ticket Not Booked !!! Try Again'
                dm='To book ticket again go to home tab and book there'
                return render_template("error.html", um=um, dm=dm)
        else :
            um='You did not book Any Ticket !!!! To book ticket again go to home tab and book there'
            dm='Please Book Ticket First'
            return render_template("error.html", um=um, dm=dm)
        cur.close()
    message='Check Status'
    return render_template("status.html", message=message)


@app.route("/delete",methods=['GET','POST'])
def delete():
    if request.method == 'POST':
        detail=request.form
        id=detail['pid']
        cur = mysql.connection.cursor()
        value=cur.execute('''DELETE FROM passenger WHERE id={}'''.format(id))
        mysql.connection.commit()
        if value>0 :
            um='Your Ticket is Successfully Cancled '
            dm='Thank You Visit Again !!!'
            return render_template("success.html", um=um, dm=dm)
        else :
            um='You did not book Any Ticket !!!! To book ticket again go to home tab and book there'
            dm='Visit Again !!!'
            return render_template("error.html", um=um, dm=dm)
        cur.close()
    message='Cancel Ticket'
    return render_template("status.html", message=message)

@app.route("/list")
def list():
    cur=mysql.connection.cursor()
    cur.execute('''DELETE FROM passenger WHERE train_id = 0''')
    cur.connection.commit()
    value = cur.execute('''SELECT * FROM passenger''')
    p_detail = cur.fetchall()
    if value > 0 :
        value = cur.execute('''SELECT * FROM STATION''')
        t_detail = cur.fetchall()
        return render_template("final.html", p_detail=p_detail, t_detail=t_detail)

@app.route("/whole")
def whole():
    cur=mysql.connection.cursor()
    value = cur.execute('''SELECT * FROM STATION''')
    t_detail = cur.fetchall()
    return render_template("user.html", trains=t_detail)


if __name__ =='__main__':
    app.run(debug=True)
