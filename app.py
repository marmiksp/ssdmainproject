from flask import Flask,render_template,request,session,logging,url_for,redirect,flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session,sessionmaker
import random
import json
from passlib.hash import sha256_crypt
import os
from werkzeug.utils import secure_filename

# engine=create_engine("mysql+pymysql://root:@localhost/ssdproject")
engine=create_engine("mysql+pymysql://root:mast1320@localhost/ssdproject")
db=scoped_session(sessionmaker(bind=engine))
UPLOAD_FOLDER = 'static/uploads/'

app=Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def home():
    return render_template("mainpage.html")

# @app.route("/InstructorLobby")
# def InstructorLobby():

#     return render_template('InstructorLobby.html')

# register here
@app.route("/register",methods=["GET","POST"])
def register():
    if request.method=="POST":
        firstname=request.form.get("firstname")
        lastname=request.form.get("lastname")
        email=request.form.get("email")
        password=request.form.get("password")
        confirm=request.form.get("confirm")
        usertype=request.form.get("usertype")
        # secure_password=sha256_crypt.encrypt(str(password))

        emailData=db.execute("SELECT email from users WHERE email=:email",{"email":email}).fetchone()
        
       
        if emailData!=None:
             flash("This email is already registered,try to login with your passwod","danger")
             return redirect(url_for('login'))


        if password==confirm:
            db.execute("INSERT INTO users(firstname,lastname,email,password,usertype) VALUES(:firstname,:lastname,:email,:password,:usertype)",
            {"firstname":firstname,"lastname":lastname,"email":email,"password":password,"usertype":usertype})
            db.commit()
            userid = db.execute("Select userid from users where email = :email",{"email":email}).fetchone()[0]
            if(usertype == "participant"):
                
                db.execute("INSERT INTO teams(userid,email,teamid) VALUES(:userid,:email,:teamid)",{"userid":userid,"email":email,"teamid":-10})
                db.commit()
            flash("you are registered and can login now","success")
            return redirect(url_for('login'))
        else:
            flash("Password does not match","danger")
            return render_template("register.html")


    return render_template("register.html")

# login here
@app.route("/login",methods=["GET","POST"])
def login():
    # da=db.execute("SELECT * from users").fetchall()
    # print(da[0])
    if request.method=="POST":
        
        email=request.form.get("email")
        password=request.form.get("password")
        print(password)
        print(email)
        
        userid=db.execute("SELECT userid from users WHERE email=:email",{"email":email}).fetchone()[0]
        fname=db.execute("SELECT firstname from users WHERE email=:email",{"email":email}).fetchone()[0]
        emailData=db.execute("SELECT email from users WHERE email=:email",{"email":email}).fetchone()[0]
        passwordData=db.execute("SELECT password from users WHERE email=:email",{"email":email}).fetchone()[0]
        usertype=db.execute("SELECT usertype from users WHERE email=:email",{"email":email}).fetchone()[0]
        print(userid)
        print("email")
        if emailData is None:
            flash("Email is not registered","danger")
            return render_template("login.html")
        else:
            #  if usertype=="instructuor":
            #      return redirect("/InstructorLobby")
           
            #  session['logged_in'] = True
            #  session['email'] = email
            #  session['userid'] = userid
            #  session['fname'] = fname
                print(password +"   "+passwordData)
                if(password == passwordData):
                    if usertype=="instructor":
                        return  redirect("/instructorlobby/"+str(userid))
                    alreadylogin = db.execute("Select * from login where userid = :userid",{"userid":userid}).fetchone()
                    if alreadylogin is None:
                        
                        db.execute("INSERT INTO login(userid,email) VALUES(:userid,:email)",{"userid":userid,"email":email})
                        db.commit()
                   # teamid = db.execute("Select * from teams where email = :email",{"email":email}).fetchone()[2]
                #  print(teamid)
                    
                    # flash("You are now login","success")
                    print("Hello ji")
                    return redirect("/waiting/"+str(userid))
                        # change to main page
                        
                else:
                    flash("Incorrect Password","danger")
                    return render_template("login.html")                
    return render_template("login.html")


@app.route('/checkassign/<int:userid>')
def checkassign(userid):
    print(userid)
    teamid = db.execute("Select teamid from teams where userid = :userid",{"userid":userid}).fetchone()[0]
    if(teamid == -10):
        return redirect("/waiting/"+str(userid))
    else:
        
        return redirect("/sticky1/"+str(teamid))

@app.route('/logout/<int:userid>')
def logout(userid):
    

        # Create cursor
        # uid = session['uid']
        # x = '0'
        # cur.execute("UPDATE users SET online=%s WHERE id=%s", (x, uid))
    loginst = db.execute("Select * from login where userid = :userid",{"userid":int(userid)}).fetchone()
    if loginst is None:
        flash('You are not logged in', 'success')
        return render_template("home.html")
        
    db.execute("Delete from login where userid=:userid",{"userid":userid})
    db.commit()
    # flash('You are logged out', 'success')
    return redirect("/")

 #waiting room
@app.route("/waiting/<int:userid>",methods=["GET","POST"])
def waiting(userid):
     
    data = db.execute("select * from users where userid=:userid",{"userid":int(userid)}).fetchone()
    print(data)
    return render_template("waiting.html", data=data)   
 
# login here
@app.route("/assignteamid/<int:userid>",methods=["GET","POST"])
def assignteamid(userid):
    
    if request.method=="POST":
         
         
        loguserid=db.execute("SELECT userid from teams where teamid=:teamid",{"teamid":-10}).fetchall()
        #  UPDATE table_name SET field1 = new-value1, field2 = new-value2
        #     [WHERE Clause]
        # print()
        teamdet={}
        
        for i in loguserid:
             
            teamid=request.form.get(str(i[0]))
            teamtitle=request.form.get("title"+str(i[0]))
            
            teamdet[teamtitle]=teamid
            print(teamtitle)
            print(teamid)
            
            db.execute("UPDATE teams SET teamid=:teamid where userid=:userid",{"teamid":teamid, "userid":i[0]})
        db.commit()
        for i in teamdet:
            print(type(teamdet[i]))
            db.execute("INSERT INTO teamdetails(teamid, title) VALUES(:teamid,:title)",{"teamid":int(teamdet[i]), "title":i})
        db.commit() 
        
        return redirect("/instructorlobbyafter/"+str(userid))  


@app.route('/instructorlobbyafter/<int:userid>')
def instructorlobbyafter(userid):
    users=db.execute("SELECT u.firstname 'firstname', u.lastname 'lastname',u.userid 'userid', t.teamid 'teamid'  from users u,teams t where u.userid=t.userid").fetchall()
        
                     
        # return redirect("/instructorlobby/"+str(userid))              
    return render_template("InstructorLobbyafter.html", users = users)

@app.route("/chatbox/<int:userid>")
def chatboxtest(userid):
    teamid = db.execute("select * from teams where userid = :userid",{"userid":userid}).fetchone()[2]
    print(type(teamid))
    teammembers = db.execute("select u.userid, u.firstname, u.lastname from users u, teams t where u.userid = t.userid and t.teamid = :teamid",{"teamid":teamid}).fetchall()
    project=db.execute("SELECT title from teamdetails where teamid=:teamid",{"teamid":teamid}).fetchone()[0]
    return render_template("chatbox.html", userid=userid, teamid = teamid,project=project, teammembers=teammembers)


@app.route('/instructorlobby/<int:userid>')
def instructorlobby(userid):
    
    users=db.execute("SELECT u.* from teams t, users u where t.userid = u.userid and t.teamid=:teamid",{"teamid":-10}).fetchall()
    # print(sticky)
    return render_template('InstructorLobby.html', users=users, insid=userid)





@app.route("/catchmsg",  methods=['POST','GET'])
def catchmsg():
    # data = request.get_json()
    MESSAGE = request.args.get('MESSAGE', 0, type=str)
    rmsg = json.loads(MESSAGE)
    userid = int(rmsg["USERID"])
    teamid = int(rmsg["TEAMID"])
    msg = rmsg["MESSAGE"]
    
    db.execute("Insert into chats(userid,msg,teamid) values(:userid,:msg,:teamid)",{"userid":userid,"msg":msg,"teamid":teamid})
    db.commit()
    
    # print(rmsg)
    msgs = db.execute("select * from chats where teamid = :teamid",{"teamid":teamid}).fetchall()
    # print(msgs)
    li=[list(l1) for l1 in msgs]
    return jsonify(result=li)

@app.route("/fetchmsg",  methods=['POST','GET'])
def fetchmsg():
    # data = request.get_json()
    MESSAGE = request.args.get('MESSAGE', 0, type=str)
    rmsg = json.loads(MESSAGE)
    print(rmsg)
    userid = int(rmsg["USERID"])
    teamid = int(rmsg["TEAMID"])
    print(teamid)
    print(userid)
    
    msgs = db.execute("select * from chats where teamid = :teamid",{"teamid":teamid}).fetchall()
    
    # print(msgs)
    # li=[(1,2,3),(1,4,2),(1,"Jay",2)]
    li=[list(l1) for l1 in msgs]
    return jsonify(result=li)

# +++++++++++++++++++++++++++++++++++++++++++++++++  Sticky Notes  +++++++++++++++++++++++++++++++++++++++++++++++++++++

# @app.route('/addnewsticky', methods=['POST'])
# def addnewsticky():
    
#     sticky=db.execute("SELECT * from stickynotes ").fetchall()
#     # print(sticky)
#     return render_template('sticky.html', tasks=sticky)

@app.route('/sticky1/<int:teamid>')
def tasks_list1(teamid):
    
    
    sticky=db.execute("SELECT * from stickynotes where teamid=:teamid",{"teamid":teamid}).fetchall()
    # print(sticky)
    data = {}
    # data["tasks"]=sticky
  
    return render_template('sticky1.html', tasks=sticky, teamid=teamid)


@app.route('/sticky2/<int:teamid>')
def tasks_list2(teamid):
    # teamid = db.execute("select * from teams where userid = :userid",{"userid":userid}).fetchone()[2]
    sticky=db.execute("SELECT * from stickynotes where teamid=:teamid",{"teamid":teamid}).fetchall()
    # print(sticky)
    return render_template('sticky2.html', tasks=sticky , teamid=teamid)

@app.route('/sticky3/<int:teamid>')
def tasks_list3(teamid):
    
    # teamid = db.execute("select * from teams where userid = :userid",{"userid":userid}).fetchone()[2]
    sticky=db.execute("SELECT * from stickynotes where teamid=:teamid",{"teamid":teamid}).fetchall()
    # print(sticky)
    return render_template('sticky3.html', tasks=sticky, teamid=teamid)

@app.route('/sticky5/<int:teamid>')
def tasks_list4(teamid):
    
    # teamid = db.execute("select * from teams where userid = :userid",{"userid":userid}).fetchone()[2]
    sticky=db.execute("SELECT * from stickynotes where teamid=:teamid",{"teamid":teamid}).fetchall()
    # print(sticky)
    return render_template('sticky5.html', tasks=sticky, teamid=teamid)

@app.route('/sticky4/<int:teamid>')
def tasks_list5(teamid):
    
    # teamid = db.execute("select * from teams where userid = :userid",{"userid":userid}).fetchone()[2]
    
    pics=db.execute("SELECT id,image from picture where teamid=:teamid",{"teamid":teamid}).fetchall()

    # print(sticky)
    print(pics)
    return render_template('sticky4.html', pics=pics, teamid=teamid)



@app.route('/sticky/task/<int:teamid>', methods=['POST'])
def add_task(teamid):
    content = request.form['content']
    step = request.form['step']
   
    # teamid = db.execute("select * from teams where userid = :userid",{"userid":userid}).fetchone()[2]
    color="green"
    if not content:
        return 'Error'
    print(content)
    db.execute("INSERT INTO stickynotes(userid,step,content,color,teamid) VALUES(:userid,:step,:content,:color,:teamid)",
            {"userid":99,"step":step,"content":content,"color":color,"teamid":teamid})
    db.commit()
    # colo=["red","blue","greem"]
    return redirect('/sticky'+str(step)+"/"+str(teamid))


@app.route('/sticky/delete/<int:task_id>')
def delete_task(task_id):
    
    step=db.execute("SELECT step, teamid from stickynotes WHERE id=:task_id",{"task_id":task_id}).fetchone()
    db.execute("delete from stickynotes WHERE id=:task_id",{"task_id":task_id})
    
    db.commit()
    
    return redirect('/sticky'+str(step[0]) +"/"+str(step[1]))



@app.route('/sticky4/picdelete/<int:pic_id>')
def delete_pic(pic_id):
    
    team=db.execute("SELECT teamid from picture WHERE id=:pic_id",{"pic_id":pic_id}).fetchone()
    db.execute("delete from picture WHERE id=:pic_id",{"pic_id":pic_id})
    
    db.commit()
    
    return redirect('/sticky4/'+str(team[0]))

'''
@app.route('/picture/delete/<int:pic_id>')
def delete_picture(pic_id):
    
    pic=db.execute("SELECT step, teamid from  WHERE id=:task_id",{"task_id":task_id}).fetchone()
    db.execute("delete from stickynotes WHERE id=:task_id",{"task_id":task_id})
    
    db.commit()
    
    return redirect('/sticky'+str(step[0]) +"/"+str(step[1]))
'''

@app.route('/sticky/done/<int:task_id>')
def resolve_task(task_id):
    
    colo=["orchid","dodgerblue","darkturquoise","tomato","deeppink","yellow","LightSalmon","GreenYellow","Pink","Violet"]
 
    colonew= colo[random.randint(0,9)]
    # db.session.add(task)
   
    step=db.execute("SELECT step,teamid from stickynotes WHERE id=:task_id",{"task_id":task_id}).fetchone()
    db.execute(" UPDATE stickynotes SET color = :colonew WHERE id=:task_id",{"task_id":task_id, "colonew":colonew})
    print(step[0])
    db.commit()
    
    return redirect('/sticky'+str(step[0])+"/"+str(step[1]))


@app.route("/wall/<int:teamid>")
def wall(teamid):
     #teamid = session["teamid"]
     notes=db.execute("SELECT * from stickynotes where teamid=:teamid",{"teamid":teamid}).fetchall()
     #notes=db.execute("SELECT * from stickynotes where teamid=1").fetchall()
     pics=db.execute("SELECT image from picture where teamid=:teamid",{"teamid":teamid}).fetchall()
     print(pics)
     notelist=[]
     for n in notes:
         d={"content":n[3],"color":n[4],"step":n[2]}
         notelist.append(d)
         print(notelist)
    
     project=db.execute("SELECT title from teamdetails where teamid=:teamid",{"teamid":teamid}).fetchone()[0]
         


     return render_template("wall.html",notes=json.dumps(notelist),teamid=teamid,project=project,pics=pics)


@app.route("/showwalltoins" ,methods=['POST','GET'])
def showwalltoins():
     #teamid = session["teamid"]
     
     teamid=request.form.get("teamid")
     notes=db.execute("SELECT * from stickynotes where teamid=:teamid",{"teamid":teamid}).fetchall()
     #notes=db.execute("SELECT * from stickynotes where teamid=1").fetchall()
     pics=db.execute("SELECT image from picture where teamid=:teamid",{"teamid":teamid}).fetchall()
     print(pics)
     notelist=[]
     for n in notes:
         d={"content":n[3],"color":n[4],"step":n[2]}
         notelist.append(d)
         print(notelist)
    
     project=db.execute("SELECT title from teamdetails where teamid=:teamid",{"teamid":teamid}).fetchone()[0]

     return render_template("wall.html",notes=json.dumps(notelist),teamid=teamid,project=project,pics=pics)

@app.route("/forupload/<int:teamid>" ,methods=['POST','GET'] )
def forupload(teamid):
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        print('upload_image filename: ' + filename)
        fi=str(filename)
        print(teamid)
        db.execute('INSERT INTO picture(teamid,image) VALUES(:teamid,:image)',{"teamid":teamid,"image":fi})
       
        #db.execute('INSERT INTO picture(teamid,image) VALUES(1,"ab")')
        #db.commit()
        db.commit()
    return redirect('/sticky4/'+str(teamid))

        
        




# +++++++++++++++++++++++++++++++++++++++++++++++++  Sticky Notes Complete +++++++++++++++++++++++++++++++++++++++++++++++++++++


if __name__=="__main__":
    app.secret_key="rishurishu"
    app.run(debug=True)