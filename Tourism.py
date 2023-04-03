from flask import Flask,render_template,request,session,jsonify
app = Flask(__name__)
from DBConnection import Db
from flask_mail import Mail, Message
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'tourismmanagement86@gmail.com'
app.config['MAIL_PASSWORD'] = 'Tourism@basil123'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
app.secret_key="helllo"






@app.route('/')
def login():
    return render_template('login.html')
@app.route('/login_post',methods=['POST'])
def login_post():
    username=request.form["textfield"]
    password=request.form["textfield2"]

    db=Db()
    qry="select * from login where `User Name`='"+username+"' and Password='"+password+"'"
    res=db.selectOne(qry)

    if res is not None:

        session['lid']=str(res["lid"])
        if res['Type']=="USER":
            return render_template('user/home.html')
        elif res['Type']=="admin":
            return render_template('admin/home.html')
        else:
            return "<script>alert('Invalid username or password');window.location='/'</script>"

    else:
        return "<script>alert('Invalid username or password');window.location='/'</script>"






    #
    # return render_template('login.html')



@app.route('/Enquiry')
def Enquiry():
    return render_template('Enquiry.html')
@app.route('/Enquiry_post',methods=['POST'])
def Enquiry_post():
    name=request.form["textfield"]
    Email=request.form["textfield2"]
    phone=request.form["textfield3"]
    District=request.form["textfield4"]
    enquiry=request.form["enq"]
    q = "insert into enquiry(Name,Email,Phone,District,enquiry,date)value('" + name + "','" + Email + "','" + phone + "','" + District + "','" + enquiry + "',curdate())"
    db = Db()
    db.insert(q)
    return '''<script>alert('Enquiry Added Successfully');window.location='/'</script>'''







@app.route('/user_registration')
def user_registration():
    return render_template('user registration.html')
@app.route('/user_registration_post',methods=['post'])
def user_registration_post():
    Image=request.files["fileField"]
    Name=request.form["textfield"]
    Gender=request.form["radio"]
    Place=request.form["textfield2"]
    Pin=request.form["textfield3"]
    Post=request.form["textfield4"]
    phone=request.form["textfield5"]
    Email=request.form["textfield6"]
    Password=request.form["textfield7"]


    from _datetime import datetime

    filename = str(datetime.now().year) + str(datetime.now().month) + str(datetime.now().day) + str(
        datetime.now().hour) + str(datetime.now().minute) + str(datetime.now().second)

    p = "C:\\Users\\BASIL\\PycharmProjects\\Tourism\\static\\user\\"
    Image.save(p + filename + ".jpg")
    p = "/static/user/" + filename + ".jpg"

    # qry1="select * from user where Email='"+Email+"'"
    # db = Db()
    # res=db.selectOne(qry1)
    # if res is not  None:

    qry="INSERT INTO login(`User Name`,Password,Type)VALUES('"+Name+"','"+Password+"','USER')"
    db = Db()
    lid = db.insert(qry)
    q="INSERT INTO user(Image,Name,Gender,Place,Pin,Post,Phone,Email,lid)values('"+p+"','"+ Name+"','"+Gender+"','"+Place+"','"+Pin+"','"+Post+"','"+phone+"','"+Email+"','"+str(lid)+"')"
    db.insert(q)
    return '''<script>alert('Successfully registred');window.location='/'</script>'''

    # else:
    #     return '''<script>alert('Already registred');window.location='/user_registration'</script>'''




@app.route('/check_Email')
def check_Email():
    id = request.args.get('id')
    qry="select * from user where Email='"+id+"'"
    db=Db()
    res=db.selectOne(qry)
    if res is not None:
        return jsonify(status="yes")
    else:
        return jsonify(status="no")









@app.route('/admin_index')
def admin_index():
    return render_template('admin/admin_index.html')




@app.route('/admin_Home_Page')
def admin_Home_Page():
    return render_template('admin/home.html')


@app.route('/admin_Add_tourist_place')
def admin_Add_tourist_place():
    return render_template('admin/Add tourist place.html')
@app.route('/admin_Add_tourist_place_post',methods=['post'])
def admin_Add_tourist_place_post():
    Place_name=request.form["textfield"]
    Description=request.form["textarea"]
    pic1=request.files["fileField"]
    pic2=request.files["fileField2"]
    District=request.form["textfield2"]
    Latitude=request.form["textfield3"]
    Longitude=request.form["textfield4"]
    from _datetime import datetime
    filename = str(datetime.now().year) + str(datetime.now().month) + str(datetime.now().day) + str(
        datetime.now().hour) + str(datetime.now().minute) + str(datetime.now().second)

    p = "C:\\Users\\BASIL\\PycharmProjects\\Tourism\\static\\touristplace\\"
    pic1.save(p+filename+"pic1.jpg")
    pic2.save(p+filename+"pic2.jpg")
    p1 = "/static/touristplace/" + filename + "pic1.jpg"
    p2 = "/static/touristplace/" + filename + "pic2.jpg"

    q=" INSERT INTO `tourist place`(`Place Name`,Description,`pic 1`,`pic 2`,District,latitude,longitude) VALUES('"+Place_name+"','"+Description+"','"+p1+"','"+ p2+"','"+District+"','"+Latitude+"','"+ Longitude+"')"
    db = Db()
    db.insert(q)
    return render_template('admin/Add tourist place.html')




@app.route('/admin_Edit_tourist_place/<tid>')
def admin_Edit_tourist_place(tid):

    qry="select * from `tourist place` where tid='"+tid+"'"
    db = Db()
    res = db.selectOne(qry)
    return render_template('admin/Edit tourist place.html',res=res)


@app.route('/admin_Edit_tourist_place_post',methods=['post'])
def admin_Edit_tourist_place_post():
    Place_name=request.form["textfield"]
    Description=request.form["textarea"]
    tid=request.form["tid"]
    District=request.form["textfield2"]
    Latitude=request.form["textfield3"]
    Longitude=request.form["textfield4"]



    from _datetime import datetime
    filename = str(datetime.now().year) + str(datetime.now().month) + str(datetime.now().day) + str(
        datetime.now().hour) + str(datetime.now().minute) + str(datetime.now().second)
    p = "C:\\Users\\BASIL\\PycharmProjects\\Tourism\\static\\touristplace\\"
    if 'fileField' in request.files and 'fileField2' in request.files:
        pic1 = request.files["fileField"]
        pic2 = request.files["fileField2"]
        if pic2.filename !="" and pic1.filename !="":

            pic1.save(p + filename + "pic1.jpg")
            pic2.save(p + filename + "pic2.jpg")
            p1 = "/static/touristplace/" + filename + "pic1.jpg"
            p2 = "/static/touristplace/" + filename + "pic2.jpg"
            qry = "update `tourist place` set `Place Name`='" + Place_name + "',Description='" + Description + "',`pic 1`='" + p1 + "',`pic 2`='" + p2 + "',District='" + District + "',latitude='" + Latitude + "',longitude='" + Longitude + "' where tid='"+tid+"'"
            db = Db()
            res = db.update(qry)

        else:
            qry = "update `tourist place` set `Place Name`='" + Place_name + "',Description='" + Description + "',District='" + District + "',latitude='" + Latitude + "',longitude='" + Longitude + "' where tid='"+tid+"'"
            db = Db()
            print(qry)
            res = db.update(qry)

    elif 'fileField' in request.files:
        pic1 = request.files["fileField"]
        if pic1.filename != "":
            pic1.save(p + filename + "pic1.jpg")
            p1 = "/static/touristplace/" + filename + "pic1.jpg"
            qry = "update `tourist place` set `Place Name`='" + Place_name + "',Description='" + Description + "',`pic 1`='" + p1 + "'District='" + District + "',latitude='" + Latitude + "',longitude='" + Longitude + "' where tid='tid'"
            db = Db()
            res = db.update(qry)

        else:
            qry = "update `tourist place` set `Place Name`='" + Place_name + "',Description='" + Description + "',District='" + District + "',latitude='" + Latitude + "',longitude='" + Longitude + "' where tid='tid'"
            db = Db()
            res = db.update(qry)
    elif 'fileField2' in request.files:
        pic2 = request.files["fileField2"]
        if pic2.filename != "":
            pic2.save(p + filename + "pic2.jpg")
            p2 = "/static/touristplace/" + filename + "pic2.jpg"
            qry = "update `tourist place` set `Place Name`='" + Place_name + "',Description='" + Description + "',`pic 2`='" + p2 + "',District='" + District + "',latitude='" + Latitude + "',longitude='" + Longitude + "' where tid='"+tid+"'"
            db = Db()
            res = db.update(qry)
        else:
            qry = "update `tourist place` set `Place Name`='" + Place_name + "',Description='" + Description + "',District='" + District + "',latitude='" + Latitude + "',longitude='" + Longitude + "' where tid='"+tid+"'"
            db = Db()
            res = db.update(qry)
    else:

        qry="update `tourist place` set `Place Name`='"+Place_name+"',Description='"+Description+"',District='"+District+"',latitude='"+Latitude+"',longitude='"+Longitude+"' where tid='"+tid+"'"

        db = Db()
        res = db.update(qry)
    return "<script>alert('Tourist place Update Successfully');window.location='/admin_view_tourist_place'</script>"




@app.route('/check_Place')
def check_Place():
    id = request.args.get('id')
    qry="select * from `tourist place` where `Place Name`='"+id+"'"
    db=Db()
    res=db.selectOne(qry)
    if res is not None:
        return jsonify(status="yes")
    else:
        return jsonify(status="no")






@app.route('/admin_view_tourist_place')
def admin_view_tourist_place():
    qry="select * from `tourist place`"
    db=Db()
    res=db.select(qry)
    return render_template('admin/view tourist place.html',res=res)


@app.route('/admin_delete_tourist_place/<tid>')
def admin_delete_tourist_place(tid):
    qry="delete from `tourist place` where tid='"+tid+"'"
    db = Db()
    res = db.delete(qry)
    return "<script>alert('Tourist Place Delete Successfully'); window.location='/admin_view_tourist_place'</script>"



@app.route('/admin_Add_vehicle')
def admin_Add_vehicle():
    return render_template('admin/Add vehicle.html')
@app.route('/admin_Add_vehicle_post',methods=['post'])
def admin_Add_vehicle_post():
    Vehicle_Number=request.form["textfield"]
    Vehicle_Name=request.form["textfield2"]
    Vehicle_Type=request.form["select"]
    Image=request.files["fileField"]
    Contact_Number=request.form["textfield3"]
    dist=request.form["district"]

    from _datetime import datetime

    filename = str(datetime.now().year) + str(datetime.now().month) + str(datetime.now().day) + str(
        datetime.now().hour) + str(datetime.now().minute) + str(datetime.now().second)

    p = "C:\\Users\\BASIL\\PycharmProjects\\Tourism\\static\\vehicle\\"
    Image.save(p + filename + ".jpg")
    p = "/static/vehicle/" + filename + ".jpg"

    q="INSERT INTO vehicle (`vehicle Number`,`Vehicle Name`,`Vehicle Type`,Pic,`Contact Number`,district)   VALUES('"+Vehicle_Number+"','"+ Vehicle_Name+"','"+Vehicle_Type+"','"+p+"','"+Contact_Number+"','"+dist+"')"
    db=Db()
    db.insert(q)



    return render_template('admin/Add vehicle.html')




@app.route('/check_Vehicle')
def check_Vehicle():
    id = request.args.get('id')
    qry="select * from vehicle where `vehicle Number`='"+id+"'"
    db=Db()
    res=db.selectOne(qry)
    if res is not None:
        return jsonify(status="yes")
    else:
        return jsonify(status="no")


@app.route('/check_Hotel')
def check_Hotel():
    id = request.args.get('id')
    qry="select* from hotel where `Hotel Licence`='"+id+"'"
    db=Db()
    res=db.selectOne(qry)
    if res is not None:
        return jsonify(status="yes")
    else:
        return jsonify(status="no")



@app.route('/admin_edit_vehicle/<vid>')
def admin_edit_vehicle(vid):
    qry="select * from vehicle where vid='"+vid+"'"
    db = Db()
    res = db.selectOne(qry)
    return render_template('admin/edit Vehicle.html',res=res)



@app.route('/admin_edit_vehicle_post',methods=['post'])
def admin_edit_vehicle_post():
    Vehicle_Number=request.form["textfield"]
    Vehicle_Name=request.form["textfield2"]
    Vehicle_Type=request.form["select"]
    Contact_Number=request.form["textfield3"]



    if 'fileField' in request.files:
        Image = request.files["fileField"]
        if Image.filename !="":
            from _datetime import datetime

            filename = str(datetime.now().year) + str(datetime.now().month) + str(datetime.now().day) + str(
                datetime.now().hour) + str(datetime.now().minute) + str(datetime.now().second)

            p = "C:\\Users\\BASIL\\PycharmProjects\\Tourism\\static\\vehicle\\"
            Image.save(p + filename + ".jpg")
            p = "/static/vehicle/" + filename + ".jpg"
            qry = "update vehicle set `vehicle Number`='" + Vehicle_Number + "',`Vehicle Name`='" + Vehicle_Name + "',`Vehicle Type`='" + Vehicle_Type + "',`Contact Number`='" + Contact_Number + "' where vid='vid'"
            db = Db()
            db.update(qry)
        else:
            qry = "update vehicle set `vehicle Number`='" + Vehicle_Number + "',`Vehicle Name`='" + Vehicle_Name + "',`Vehicle Type`='" + Vehicle_Type + "',`Contact Number`='" + Contact_Number + "' where vid='vid'"
            db = Db()
            res = db.update(qry)
    else:
        qry="update vehicle set `vehicle Number`='"+Vehicle_Number+"',`Vehicle Name`='"+Vehicle_Name+"',`Vehicle Type`='"+Vehicle_Type+"',Pic='"+p+"',`Contact Number`='"+Contact_Number+"' where vid='vid'"
        db = Db()
        res = db.update(qry)
    return "<script>alert('Vehicle Update Successfully');window.location='/admin_view_vehicle'</script>"




@app.route('/admin_view_vehicle')
def admin_view_vehicle():

    qry="select * from vehicle"
    db=Db()
    res=db.select(qry)
    return render_template('admin/view vehicle.html',res=res)





@app.route('/admin_delete_vehicle/<vid>')
def admin_delete_vehicle(vid):
    qry="delete from vehicle where vid='"+vid+"'"
    db = Db()
    res = db.delete(qry)
    return "<script>alert('Vehicle Delete Successfully');window.location='/admin_view_vehicle'</script>"


@app.route('/admin_Add_Hotel')
def admin_Add_Hotel():
    return render_template('admin/Add Hotel.html')
@app.route('/admin_Add_Hotel_post',methods=['post'])
def admin_Add_Hotel_post():
    Image=request.files["fileField"]
    Hotel_name=request.form["textfield"]
    Place=request.form["textfield2"]
    Pin=request.form["textfield3"]
    Post=request.form["textfield4"]
    District=request.form["textfield5"]
    Latitude=request.form["textfield6"]
    Longitude=request.form["textfield7"]
    Hotel_Licence=request.form["textfield8"]
    Hotel_Type=request.form["select"]
    Phone1=request.form["textfield9"]
    Phone2=request.form["textfield10"]
    Website=request.form["textfield11"]
    Email=request.form["textfield12"]



    from _datetime import datetime

    filename=str(datetime.now().year)+str(datetime.now().month)+str(datetime.now().day)+str(datetime.now().hour)+str(datetime.now().minute)+str(datetime.now().second)


    p="C:\\Users\\BASIL\\PycharmProjects\\Tourism\\static\\hotel\\"
    Image.save(p + filename + ".jpg")


    p="/static/hotel/"+ filename+".jpg"




    q="INSERT INTO hotel(Image,Name,Place,Pin,Post,District,latitude,longitude,`Hotel Licence`,`Hotel Type`,`Phone 1`,`Phone 2`,Website,Email) VALUES('"+p+"','"+Hotel_name+"','"+ Place+"','"+Pin+"','"+Post+"','"+ District+"','"+ Latitude+"','"+Longitude+"','"+ Hotel_Licence+"','"+Hotel_Type+"','"+Phone1+"','"+Phone2+"','"+Website+"','"+ Email+"')"
    db = Db()
    db.insert(q)

    return render_template('admin/Add Hotel.html')




@app.route('/admin_Edit_Hotel/<hid>')
def admin_Edit_Hotel(hid):
    qry =" select * from hotel where hid='"+hid+"'"
    db = Db()
    res = db.selectOne(qry)
    return render_template('admin/Edit Hotel.html',res=res)



@app.route('/admin_Edit_Hotel_post',methods=['post'])
def admin_Edit_Hotel_post():
    hid=request.form["hid"]
    Hotel_name=request.form["textfield"]
    Place=request.form["textfield2"]
    Pin=request.form["textfield3"]
    Post=request.form["textfield4"]
    District=request.form["textfield5"]
    Latitude=request.form["textfield6"]
    Longitude=request.form["textfield7"]
    Hotel_Licence=request.form["textfield8"]
    Hotel_Type=request.form["select"]
    Phone1=request.form["textfield9"]
    Phone2=request.form["textfield10"]
    Website=request.form["textfield11"]
    Email=request.form["textfield12"]

    if 'fileField' in request.files:
        Image = request.files["fileField"]
        if Image.filename != "":

            from _datetime import datetime

            filename = str(datetime.now().year) + str(datetime.now().month) + str(datetime.now().day) + str(
                datetime.now().hour) + str(datetime.now().minute) + str(datetime.now().second)

            p = "C:\\Users\\BASIL\\PycharmProjects\\Tourism\\static\\hotel\\"
            Image.save(p + filename + ".jpg")

            p = "/static/hotel/" + filename + ".jpg"

            qry="update hotel set Image='"+p+"',Name='"+ Hotel_name+"',Place='"+Place+"',Pin='"+Pin+"',Post='"+Post+"',District='"+District+"',latitude='"+Latitude+"',longitude='"+Longitude+"',`Hotel Licence`='"+Hotel_Licence+"',`Hotel Type`='"+Hotel_Type+"',`Phone 1`='"+Phone1+"',`Phone 2`='"+Phone2+"',Website='"+Website+"',Email='"+Email+"' where hid='"+hid+"'"
            db = Db()
            db.update(qry)
        else:
            qry = "update hotel set Name='" + Hotel_name + "',Place='" + Place + "',Pin='" + Pin + "',Post='" + Post + "',District='" + District + "',latitude='" + Latitude + "',longitude='" + Longitude + "',`Hotel Licence`='" + Hotel_Licence + "',`Hotel Type`='" + Hotel_Type + "',`Phone 1`='" + Phone1 + "',`Phone 2`='" + Phone2 + "',Website='" + Website + "',Email='" + Email + "' where hid='"+hid+"'"
            db = Db()
            db.update(qry)
    else:
        qry = "update hotel set Name='" + Hotel_name + "',Place='" + Place + "',Pin='" + Pin + "',Post='" + Post + "',District='" + District + "',latitude='" + Latitude + "',longitude='" + Longitude + "',`Hotel Licence`='" + Hotel_Licence + "',`Hotel Type`='" + Hotel_Type + "',`Phone 1`='" + Phone1 + "',`Phone 2`='" + Phone2 + "',Website='" + Website + "',Email='" + Email + "' where hid='"+hid+"'"
        db = Db()
        db.update(qry)
    return "<script>alert('Hotel Update Successfully');window.location='/admin_view_Hotel'</script>"




@app.route('/admin_view_Hotel')
def admin_view_Hotel():
    qry="select * from hotel"
    db=Db()
    res=db.select(qry)

    return render_template('admin/view hotel.html',res=res)



@app.route('/admin_delete_Hotel/<hid>')
def admin_delete_Hotel(hid):
    qry="delete  from  hotel where hid='"+hid+"'"
    db = Db()
    res = db.delete(qry)
    return "<script>alert('Hotel Delete Successfully');window.location='/admin_view_Hotel'</script>"


@app.route('/admin_View_Enquiry')
def admin_View_Enquiry():
    qry="select * from enquiry"
    db = Db()
    res = db.select(qry)
    return render_template('admin/View enquiry.html',res=res)


@app.route('/admin_View_Complaints')
def admin_View_Complaints():
    qry="select complaint.*,user.Name,user.Email from complaint inner join user on complaint.uid=user.lid"
    db = Db()
    res = db.select(qry)
    return render_template('admin/view complaint.html',res=res)


@app.route('/admin_View_Suggestions')
def admin_View_Suggestions():
    qry="select suggestions.*,user.Name,user.Email from suggestions inner join user on suggestions.uid=user.lid"
    db = Db()
    res = db.select(qry)
    return render_template('admin/View suggestions.html',res=res)


@app.route('/admin_Replay_Complaint/<cid>')
def admin_Replay_complaint(cid):
    session["cid"]=cid
    return render_template('admin/Replay complaint.html')


@app.route('/admin_Replay_Complaint_post',methods=['post'])
def admin_Replay_complaint_post():
    Replay=request.form["textarea"]
    qry="update complaint set replay='"+Replay+"',Status='ok'where cid='"+session["cid"]+"'"
    db = Db()
    res = db.update(qry)
    return admin_View_Complaints()



@app.route('/admin_View_hotel_review')
def admin_View_hotel_review():
    qry="select `review hotel`.*,user.Name,user.Email,hotel.Name as hname,hotel.Email as hemail from user inner join `review hotel` on `review hotel`.uid=user.lid inner join hotel on hotel.hid=`review hotel`.hid "
    db = Db()
    res = db.select(qry)
    return render_template('admin/view hotel review.html',res=res)


@app.route('/admin_delete_hotel_review/<rev_id>')
def admin_delete_hotel_review(rev_id):
    qry="delete from `review hotel` where rhid='"+rev_id+"'"
    db = Db()
    res = db.delete(qry)
    return '''<script>alert(' delete successfully');window.location='/admin_View_hotel_review'</script>'''



@app.route('/admin_View_place_review')
def admin_View_place_review():
    qry="select `review place`.*,user.Name,user.Email,`tourist place`.`Place Name`,`tourist place`.`pic 1` from user inner join `review place` on `review place`.uid=user.lid inner join `tourist place` on `tourist place`.tid=`review place`.placeid "
    print(qry)
    db = Db()
    res = db.select(qry)
    return render_template('admin/view place review.html',res=res)


@app.route('/admin_delete_place_review/<rev_id>')
def admin_delete_place_review(rev_id):
    qry="delete from `review place` where rpid='"+rev_id+"'"
    db = Db()
    res = db.delete(qry)
    return '''<script>alert(' delete successfully');window.location='/admin_View_place_review'</script>'''



@app.route('/admin_View_Users')
def admin_View_Users():
    qry="select * from user"
    db = Db()
    res = db.select(qry)
    return render_template('admin/view_registrate_users.html',res=res)




@app.route('/user_Home_Page')
def user_Home_Page():
    return render_template('user/home.html')



@app.route('/user_View_tourist_place')
def user_View_tourist_place():
    qry="select * from `tourist place`"
    db = Db()
    res = db.select(qry)
    return render_template('user/view tourist place.html',res=res)
@app.route('/user_View_tourist_place_post',methods=["post"])
def user_View_tourist_place_post():
    name=request.form["s"]
    qry="select * from `tourist place` where `Place Name` like '%"+name+"%'"
    db = Db()
    res = db.select(qry)
    return render_template('user/view tourist place.html',res=res)
@app.route('/user_View_vehicle')
def user_View_vehicle():
    qry="select * from vehicle"
    db = Db()
    res = db.select(qry)
    return render_template('user/view vehicle.html',res=res)
@app.route('/user_View_vehicle_search',methods=["post"])
def user_View_vehicle_search():
    dis=request.form["district"]
    qry="select * from vehicle where district='"+dis+"'"
    db = Db()
    res = db.select(qry)
    return render_template('user/view vehicle.html',res=res)
@app.route('/user_View_Hotel')
def user_View_Hotel():
    qry="select * from hotel"
    db = Db()
    res = db.select(qry)
    return render_template('user/view hotel.html',res=res)
@app.route('/user_View_Hotel_post',methods=["post"])
def user_View_Hotel_post():
    name=request.form["s"]
    qry="select * from hotel where Name like '%"+name+"%'"
    db = Db()
    res = db.select(qry)
    return render_template('user/view hotel.html',res=res)
@app.route('/user_Add_suggestion')
def user_Add_suggestion():
    return render_template('user/add suggestion.html')
@app.route('/user_Add_suggestion_post',methods=['post'])
def user_Add_suggestion_post():
    Suggestion=request.form["textarea"]
    Photos=request.files["fileField"]

    from _datetime import datetime

    filename = str(datetime.now().year) + str(datetime.now().month) + str(datetime.now().day) + str(
        datetime.now().hour) + str(datetime.now().minute) + str(datetime.now().second)

    p = "C:\\Users\\BASIL\\PycharmProjects\\Tourism\\static\\suggestions\\"
    Photos.save(p + filename + ".jpg")

    p = "/static/suggestions/" + filename + ".jpg"

    q=" INSERT INTO suggestions(uid,`Suggestion Details`,pic,date) VALUES('"+session['lid']+"','"+Suggestion+"','"+p+"',curdate())"
    db = Db()
    db.insert(q)

    return render_template('user/add suggestion.html')

@app.route('/user_View_suggestion')
def user_View_suggestion():
    qry="select * from suggestions WHERE uid='"+session['lid']+"'"
    db = Db()
    res = db.select(qry)
    return render_template('user/view suggestions.html',res=res)

@app.route('/user_Add_complaint')
def user_Add_complaint():
    return render_template('user/add complaint.html')

@app.route('/user_Add_complaint_post',methods=['post'])
def user_Add_complaint_post():
    Complaint=request.form["textarea"]
    q=" INSERT INTO complaint(uid,Complaint,date) VALUES('"+session['lid']+"','"+Complaint+"',curdate())"
    db = Db()
    db.insert(q)
    return render_template('user/add complaint.html')


@app.route('/user_view_complaint')
def user_view_complaint():
    qry="select * from complaint WHERE uid='"+session['lid']+"'"
    db = Db()
    res = db.select(qry)
    return render_template('user/view complaint.html',res=res)

@app.route('/user_Add_review_place/<tid>')
def user_Add_review_place(tid):
    return render_template('user/add review place.html',tid=tid)
@app.route('/user_Add_review_place_post',methods=['post'])
def user_Add_review_place_post():
    Image=request.files["fileField"]
    Review=request.form["textarea"]
    tid=request.form["tid"]


    from _datetime import datetime

    filename = str(datetime.now().year) + str(datetime.now().month) + str(datetime.now().day) + str(
        datetime.now().hour) + str(datetime.now().minute) + str(datetime.now().second)

    p = "C:\\Users\\BASIL\\PycharmProjects\\Tourism\\static\\Reviewplace\\"
    Image.save(p + filename + ".jpg")

    p = "/static/Reviewplace/" + filename + ".jpg"
    q="INSERT INTO `review place`(uid,`Review`,Image,date,placeid) VALUES('"+session['lid']+"','"+Review+"','"+p+"',curdate(),'"+tid+"')"
    db = Db()
    db.insert(q)
    return render_template('user/add review place.html')

@app.route('/user_view_review_place/<placeid>')
def user_view_review_place(placeid):

    session["pplaceid"]= placeid

    qry="select * from `review place` WHERE uid='"+session['lid']+"' and placeid='"+placeid+"'"
    db = Db()
    res = db.select(qry)


    resothers= db.select("select `review place`.*, user.* from `review place` , user  where  `review place`.uid=user.lid and `review place`.placeid='"+placeid+"' and user.lid !='"+session['lid']+"'")






    return render_template('user/view place review.html',res=res,resothers=resothers)


@app.route('/user_delete_review_place/<rid>')
def user_delete_review_place(rid):
    qry="delete from `review place` where rpid='"+rid+"'"
    db = Db()
    res = db.delete(qry)
    return "<script>alert('Deleted Successfully');window.location='/user_view_review_place/"+session["pplaceid"]+"'</script>"







@app.route('/user_Add_review_hotel/<hid>')
def user_Add_review_hotel(hid):
    return render_template('user/add review hotel.html',hid=hid)
@app.route('/user_Add_review_hotel_post',methods=['post'])
def user_Add_review_hote_post():
    Image=request.files["fileField"]
    Review=request.form["textarea"]
    hid=request.form["hid"]



    from _datetime import datetime

    filename = str(datetime.now().year) + str(datetime.now().month) + str(datetime.now().day) + str(
        datetime.now().hour) + str(datetime.now().minute) + str(datetime.now().second)

    p = "C:\\Users\\BASIL\\PycharmProjects\\Tourism\\static\\Reviewhotel\\"
    Image.save(p + filename + ".jpg")

    p = "/static/Reviewhotel/" + filename + ".jpg"
    q="INSERT INTO `review hotel`(uid,hid,Review,Image,date) VALUES('"+session['lid']+"','"+hid+"','"+Review+"','"+p+"',curdate())"
    db = Db()
    db.insert(q)
    return render_template('user/add review hotel.html')


@app.route('/user_view_review_hotel/<hid>')
def user_view_review_hotel(hid):
    session["photelid"]=hid
    qry="select * from `review hotel` WHERE uid='"+session['lid']+"' and hid='"+hid+"'"
    db = Db()
    res = db.select(qry)

    resothers=db.select("select `review hotel`.*, user.* from `review hotel` , user  where  `review hotel`.uid=user.lid and `review hotel`.hid='"+hid+"' and user.lid !='"+session["lid"]+"'")



    return render_template('user/view hotel review.html',res=res,resothers=resothers)

@app.route('/user_delete_review_hotel/<rhid>')
def user_delete_review_hotel(rhid):
    qry="delete from `review hotel` where rhid='"+rhid+"'"
    db = Db()
    res = db.delete(qry)
    return "<script>alert('Deleted Successfully');window.location='/user_view_review_hotel/"+session['photelid']+"';</script>"

@app.route('/admin_connect/<rhid>')
def admin_connect(rhid):
    qry="select * from enquiry where eid='"+rhid+"'"
    db = Db()
    res = db.selectOne(qry)
    return render_template('admin/Replay enquiry.html', data=res)



@app.route('/admin_connect_post',methods=['post'])
def admin_connect_post():
    email = request.form["email"]
    id = request.form["id"]
    reply = request.form["reply"]
    msg = Message('Hello', sender='tourismmanagement86@gmail.com', recipients=[email])
    msg.body = str(reply)
    mail.send(msg)
    qry="update enquiry set status='ok',reply='"+reply+"'  where eid='"+str(id)+"'"
    db = Db()
    res = db.update(qry)
    return '''<script>alert('ok');window.location='/admin_View_Enquiry'</script>'''









if __name__ == '__main__':
    app.run(debug=True)
