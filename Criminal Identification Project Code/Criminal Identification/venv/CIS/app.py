from flask import Flask, render_template, request,flash
from DBConnection import DBConnection
from flask import session
from werkzeug.utils import secure_filename
from random import randint
import sys
import os
from PIL import Image
import io
import base64
import shutil
from CriminalIdentification import predict,show_prediction_labels_on_image,train

app = Flask(__name__)
app.secret_key = "def"

@app.route('/')
def index():
    return render_template('index.html')



@app.route("/authority")
def authority():
    return render_template("authority.html")



@app.route("/users")
def users():
    return render_template("user.html")

@app.route("/authoritylogin",methods =["GET", "POST"])
def authoritylogin():

        uid = request.form.get("unm")
        pwd = request.form.get("pwd")
        database = DBConnection.getConnection()
        cursor = database.cursor()
        sql = "select count(*) from authority where uid='" + uid + "' and pwd='" + pwd + "'"
        cursor.execute(sql)
        res = cursor.fetchone()[0]
        if res > 0:
            session['auid'] = uid

            return render_template("authorityhome.html")
        else:

            return render_template("authority.html",msg="Invalid Credentials")



        return render_template("admin.html")

@app.route("/authority_reg")
def authority_reg():

    return render_template("authority_reg.html")

@app.route("/authority_reg2",methods =["GET", "POST"])
def authority_reg2():
    try:
        if request.method == 'POST':
            name = request.form.get('name')
            uid = request.form.get('uid')
            pwd = request.form.get('pwd')
            email = request.form.get('email')
            mno = request.form.get('mno')
            authid=str(randint(1000, 9999))

            database = DBConnection.getConnection()
            cursor = database.cursor()
            sql = "select count(*) from authority where uid='" + uid + "'"
            cursor.execute(sql)
            res = cursor.fetchone()[0]
            if res > 0:

                return render_template("authority_reg.html",messages="User Id already exists..!")

            else:
                sql = "insert into authority values(%s,%s,%s,%s,%s,%s)"
                values = (name, uid, pwd, email, mno,authid)
                cursor.execute(sql, values)
                database.commit()



        return render_template("authority.html",messages="Registered Successfully..! Login Here.")
    except Exception as e:
        print(e)


@app.route("/upload_photo")
def upload_photo():
    return render_template("upload_photo.html")


@app.route("/authority_search")
def authority_search():
    return render_template("authority_search.html")

@app.route("/authorityhome")
def authorityhome():
    return render_template("authorityhome.html")


@app.route("/upload_photo2",methods =["GET", "POST"])
def upload_photo2():
    try:
            auid=session['auid']
            cname = request.form.get('cname')
            rmrks = request.form.get('rmrks')
            adrs = request.form.get('adrs')
            image = request.files['file']
            imgdata = secure_filename(image.filename)

            cid = str(cname) + "_" + str(randint(1000, 9999))
            imgid = image.filename
            path = "../CIS/dataset/" + cid + "/"
            if not os.path.exists(os.path.dirname(path)):
                try:
                    os.makedirs(os.path.dirname(path))
                except OSError as exc:  # Guard against race condition
                    if exc.errno != errno.EEXIST:
                        raise

            image.save(os.path.join("dataset/"+cid+"/", imgdata))
            database = DBConnection.getConnection()
            cursor = database.cursor()
            query = "insert into criminal_details values(%s,%s,%s,%s,%s,%s)"
            values = (cname, rmrks, adrs,imgid,auid,cid)
            cursor.execute(query, values)
            database.commit()


            return render_template("upload_photo.html",message="Criminal Details Uploaded Successfully..!")

    except Exception as e:
           print(e)



@app.route("/authority_search2",methods =["GET", "POST"])
def authority_search2():
    try:
        image = request.files['file']
        imgdata = secure_filename(image.filename)
        filename=image.filename

        filelist = [ f for f in os.listdir("testing") ]
        for f in filelist:
            os.remove(os.path.join("testing", f))


        image.save(os.path.join("testing", imgdata))
        print("Training KNN classifier...")
        classifier = train("../CIS/dataset", model_save_path="trained_knn_model.clf", n_neighbors=1)
        print("Training complete!")
        namelist = []
        list=[]
        namelist.clear()
        list.clear()

        # STEP 2: Using the trained classifier, make predictions for unknown images
        for image_file in os.listdir("../CIS/testing"):
            full_file_path = os.path.join("../CIS/testing", image_file)

            print("Looking for faces in {}".format(image_file))

            # Find all people in the image using a trained classifier model
            # Note: You can pass in either a classifier file name or a classifier model instance
            predictions = predict(full_file_path, model_path="trained_knn_model.clf")

            # Print results on the console
            for name, (top, right, bottom, left) in predictions:
                namelist.append(name)
                print("- Found {} at ({}, {})".format(name, left, top))



        print(namelist)
        if len(namelist) == 0 or namelist[0] == "unknown":
            return render_template("authority_search.html", message="No Results Found")

        else:
            database = DBConnection.getConnection()
            cursor = database.cursor()

            #cursor.execute("update uploadphotos set status='Resolved' where cid='" + namelist[0] + "' ")
            #database.commit()

            sql2 = "select *from criminal_details where cid='" + namelist[0] + "' "
            cursor.execute(sql2)
            res = cursor.fetchall()

            for row in res:
                name1 = row[0]
                remarks = row[1]
                adrs = row[2]
                photo = row[3]
                unm = row[4]

                sql = "select mno,auth_id from authority where uid='" + unm + "' "
                print(sql)
                cursor.execute(sql)
                rcds = cursor.fetchall()
                for data in rcds:
                    cno=data[0]
                    authid=data[1]





                test_img= os.path.join("testing",filename)
                im = Image.open(test_img)
                data = io.BytesIO()
                im.save(data, "JPEG")
                encoded_img_data = base64.b64encode(data.getvalue())

                train_img = os.path.join("dataset/"+str( namelist[0])+"/", photo)
                im2 = Image.open(train_img)
                data2 = io.BytesIO()
                im2.save(data2, "JPEG")
                encoded_img_data2 = base64.b64encode(data2.getvalue())


                list.append(name1)
                list.append(remarks)
                list.append(adrs)
                list.append(unm)
                list.append(cno)
                list.append(authid)
                print(list)

            return render_template("results.html", list=list,img_data=encoded_img_data.decode('utf-8'),img_data2=encoded_img_data2.decode('utf-8'))



    except Exception as e:
        print(e.args[0])
        tb = sys.exc_info()[2]
        print(tb.tb_lineno)
        print(e)

@app.route("/userlogin",methods =["GET", "POST"])
def userlogin():
        uid = request.form.get("unm")
        pwd = request.form.get("pwd")
        database = DBConnection.getConnection()
        cursor = database.cursor()
        sql = "select count(*) from users where uid='" + uid + "' and pwd='" + pwd + "'"
        cursor.execute(sql)
        res = cursor.fetchone()[0]
        if res > 0:
            session['uid'] = uid

            return render_template("userhome.html")
        else:

            return render_template("user.html",msg="Invalid Credentials")



        return render_template("admin.html")


@app.route("/user_reg")
def user_reg():

    return render_template("user_reg.html")


@app.route("/user_reg2",methods =["GET", "POST"])
def user_reg2():
    try:
        name = request.form.get('name')
        uid = request.form.get('uid')
        pwd = request.form.get('pwd')
        email = request.form.get('email')
        mno = request.form.get('mno')

        database = DBConnection.getConnection()
        cursor = database.cursor()
        sql = "select count(*) from users where uid='" + uid + "'"
        cursor.execute(sql)
        res = cursor.fetchone()[0]
        if res > 0:

            return render_template("user_reg.html", messages="User Id already exists..!")

        else:
            sql = "insert into users values(%s,%s,%s,%s,%s)"
            values = (name, uid, pwd, email, mno)
            cursor.execute(sql, values)
            database.commit()





        return render_template("user.html",messages="Registered Successfully..! Login Here.")
    except Exception as e:
        print(e)

@app.route("/user_home")
def user_home():
    return render_template("userhome.html")


@app.route("/user_search")
def user_search():
    return render_template("user_search.html")



@app.route("/user_search2",methods =["GET", "POST"])
def user_search2():
    try:
        uid=session["uid"]
        image = request.files['file']
        imgdata = secure_filename(image.filename)
        filename=image.filename

        filelist = [ f for f in os.listdir("testing") ]
        for f in filelist:
            os.remove(os.path.join("testing", f))


        image.save(os.path.join("testing", imgdata))
        print("Training KNN classifier...")
        classifier = train("../CIS/dataset", model_save_path="trained_knn_model.clf", n_neighbors=1)
        print("Training complete!")
        namelist = []
        list=[]
        namelist.clear()
        list.clear()

        # STEP 2: Using the trained classifier, make predictions for unknown images
        for image_file in os.listdir("../CIS/testing"):
            full_file_path = os.path.join("../CIS/testing", image_file)

            print("Looking for faces in {}".format(image_file))

            # Find all people in the image using a trained classifier model
            # Note: You can pass in either a classifier file name or a classifier model instance
            predictions = predict(full_file_path, model_path="trained_knn_model.clf")

            # Print results on the console
            for name, (top, right, bottom, left) in predictions:
                namelist.append(name)
                print("- Found {} at ({}, {})".format(name, left, top))



        print(namelist)
        if len(namelist) == 0 or namelist[0] == "unknown":
            return render_template("user_search.html", message="No Results Found")

        else:
            database = DBConnection.getConnection()
            cursor = database.cursor()



            sql2 = "select *from criminal_details where cid='" + namelist[0] + "' "
            cursor.execute(sql2)
            res = cursor.fetchall()

            for row in res:
                name1 = row[0]
                remarks = row[1]
                adrs = row[2]
                photo = row[3]
                unm = row[4]


                sql = "select mno from authority where uid='" + unm + "' "
                print(sql)
                cursor.execute(sql)
                cno = cursor.fetchone()[0]



                test_img= os.path.join("testing",filename)
                im = Image.open(test_img)
                data = io.BytesIO()
                im.save(data, "JPEG")
                img_data = base64.b64encode(data.getvalue())

                train_img = os.path.join("dataset/"+str( namelist[0])+"/", photo)
                im2 = Image.open(train_img)
                data2 = io.BytesIO()
                im2.save(data2, "JPEG")
                img_data2 = base64.b64encode(data2.getvalue())

                list.append(name1)
                list.append(remarks)
                list.append(adrs)
                list.append(unm)
                list.append(cno)
                print(list)

            return render_template("viewresults.html", list=list,img_data=img_data.decode('utf-8'),img_data2=img_data2.decode('utf-8'))



    except Exception as e:
        print(e.args[0])
        tb = sys.exc_info()[2]
        print(tb.tb_lineno)
        print(e)





if __name__ == '__main__':
    app.run(host="localhost", port=1357, debug=True)