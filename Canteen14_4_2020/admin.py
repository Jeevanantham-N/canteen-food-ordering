from flask import Flask,render_template,url_for,request,jsonify,session,g,redirect,Response
import pymongo
from pymongo import MongoClient
import sys,json
from pprint import pprint
import random,time
import secrets 
import string
import datetime
from datetime import datetime,timezone

app = Flask(__name__)
json_ = open("secret_key.json","r")
json_ = json.loads(json_.read())
app.secret_key = json_["secret_key"]

client = pymongo.MongoClient("mongodb+srv://JeevananthamN:JeevananthamN100@cluster0-v6j0k.gcp.mongodb.net/canteensystem?retryWrites=true&w=majority")
db = client["canteensystem"]
owners = db["owners"]
products = db["products"]
payment = db["payment"]
students = db["students"]
student_orders = db["student orders"]
owner_orders = db["owner orders"]

@app.before_request
def before_request():
    try:
        owner = owners.find_one({"_id":session["_id"]})
        g.owner = json.dumps(owner)
    except:
        pass

@app.route('/adminlogin')
def adminlogin():
    return render_template("adminlogin.html")

@app.route('/dashboard')
def dashboard():
    if "_id" in session:
        owner = owners.find_one({"_id":session["_id"]},{"pwd":False})
        items = products.find_one({"_id":session["_id"]},{"inc":False})
        canteen_ids = []
        canteen_idsdb = products.find_one({"_id":session["_id"]})
        for i in canteen_idsdb:
            if "_id" == i or "inc" == i:
                continue
            else:
                for j in canteen_idsdb[i]:
                    canteen_ids.append([j["product_id"],j["type"]])
        return render_template('dashboard.html',owner = json.dumps(owner),items=json.dumps(items),canteen_ids=json.dumps(canteen_ids))
    else:
        return redirect(url_for('adminlogin'))

@app.route('/logindb',methods = ["POST"])
def logindb():
    session.pop('canteen_id', None)
    form = request.form
    owner = owners.find_one({"_id":int(form["phone"])})
    try:
        if int(form["phone"]) == owner["_id"]:
            if int(form["pwd"]) == owner["pwd"]:
                session["canteen_id"] = owner["canteen_id"]
                session["_id"] = owner["_id"]
                return redirect(url_for('dashboard'))
            else:
                return render_template("adminlogin.html",error="password wrong")
        else:
            return render_template("adminlogin.html",error="not yet registered")
    except:
        return render_template("adminlogin.html",error="not yet registered")

@app.route('/adminadd')
def adminadd():
    session.pop('_id', None)
    oname = request.args.get('oname',0,type=str)
    phone = request.args.get('phone',type=int)
    pwd = request.args.get('pwd',type=int)
    canteen_id = "canteen_"+str(owners.find().count()+1)
    oid = {
        "name":oname,
        "_id":phone,
        "pwd":pwd,
        "canteen_id":canteen_id
    }
    pid = {
        "_id":phone,
        "inc":{
            "tiffen":0,
            "fastfood":0,
            "snacks":0,
            "juice":0
        },
        "tiffen":[],
        "fastfood":[],
        "snacks":[],
        "juice":[]
    }
    try:
        owners.insert_one(oid)
        products.insert(pid)
        owner_orders.insert({"_id":canteen_id})
    except:
        return jsonify(result = "already registered")
    return jsonify(result="registerd...")

@app.route('/addproducts')
def addproducts():
    oid = request.args.get('oid',type=int)
    items = request.args.get('items',type=str)
    items = json.loads(items)
    category = []
    snacks = []
    juice = []
    fastfood = []
    tiffen = []
    for i in items:
        if i["type"] == 'snacks':
            snacks.append(i)
        elif i["type"] == 'juice':
            juice.append(i)
        elif i["type"] == 'fastfood':
            fastfood.append(i)
        else:
            tiffen.append(i)
    if len(snacks)!=0:
        category.append(snacks)
    if len(juice)!=0:
        category.append(juice)
    if len(fastfood)!=0:
        category.append(fastfood)
    if len(tiffen)!=0:
        category.append(tiffen)
    for i in category:
        type_ = i[0]["type"]
        inc = products.find_one({"_id":oid},{"inc":True,"_id":False})["inc"][type_]
        for j in i:
            inc +=1
            j["product_id"] = j["product_id"] + str(inc)
        products.update_one({"_id":session["_id"]},{"$push":{type_:{"$each":i}}})
        products.update({"_id":session["_id"]},{"$set":{"inc."+type_:inc}})
    return jsonify(json=0)

@app.route('/updateproducts')
def updateproducts():
    product_id = request.args.get('product_id',type=str)
    type_ = request.args.get('type',type=str)
    item = request.args.get('item',type=str)
    price = request.args.get('price',type=str)
    quantity = request.args.get('qty',type=str)
    for i in products.find():
        print(i)
    products.update({
    "_id":session["_id"],
    type_+".product_id":product_id
    },
    {
        "$set":{
            type_+".$.item":item,
            type_+".$.price":price,
            type_+".$.quantity":quantity,
            type_+".$.available":quantity
        }
    }
    )
    for i in products.find():
        print(i)
    return jsonify(json=0)

@app.route('/deleteproducts')
def deleteproducts():
    product_id = request.args.get('product_id',type=str)
    type_ = request.args.get('item',type=str)
    print(product_id,type_)
    products.update(
    {
        "_id":session["_id"] ,
    },
    {
        "$pull":{
            type_:{"product_id": product_id}
            }
    }
    )
    return jsonify(json = 0)

@app.route('/ownerlogout')
def ownerlogout():
    session.pop("_id",None)
    return redirect(url_for("adminlogin"))

@app.route("/ownerorderstatus")
def ownerorderstatus():
    def vieworders_sse(canteen_id):
        order = owner_orders.find_one({"_id":canteen_id})
        order = json.dumps(order)
        yield f"data:{order}\n\n\n\n"   
    return Response(vieworders_sse(session['canteen_id']), mimetype="text/event-stream")

@app.route("/admincancel")
def admincancel():
    orderid = request.args.get("orderid",type=str)
    regid = request.args.get("regid",type=int)
    student_orders.update({"_id":regid},
    {"$set":{orderid+".0.level":-1}}
    )
    owner_orders.update({"_id":session["canteen_id"]},
    {"$set":{orderid+".0.level":-1}}
    )
    return jsonify(result = 1)

@app.route("/adminaccept")
def adminaccept():
    orderid = request.args.get("orderid",type=str)
    regid = request.args.get("regid",type=int)
    len_ = 4
    otp = ''.join(secrets.choice(string.ascii_uppercase + string.digits)for i in range(len_))
    student_orders.update({"_id":regid},
    {"$set":{orderid+".0.level":1,orderid+".0.otp":otp}}
    )
    owner_orders.update({"_id":session["canteen_id"]},
    {"$set":{orderid+".0.level":1,orderid+".0.otp":otp}}
    )
    return jsonify(result = 1)

@app.route("/verifyorder")
def verifyorder():
    def verifyorder_sse(canteen_id):
        order = owner_orders.find_one({"_id":canteen_id})
        order = json.dumps(order)
        yield f"data:{order}\n\n\n\n"
        time.sleep(4)
    return Response(verifyorder_sse(session["canteen_id"]), mimetype="text/event-stream")

#############################################################canteen

@app.route("/studentlogin")
def studentlogin():
    return render_template("studentlogin.html")

@app.route("/studentvalidate" , methods = ['POST','GET'])
def studentvalidate():
    session.pop("regid",None)
    form = request.form
    if form["regid"] != None:
        value = students.count({"_id":int(form["regid"])})
        if value == 1:
            session["regid"] = int(form["regid"])
            return redirect(url_for('canteen'))
        else:
            return render_template("studentlogin.html",error = "Enter valid register number")
    else:
        return render_template("studentlogin.html",error = "Enter valid register number")

@app.route("/updatestudent")
def updatestudent():
    name = request.args.get('name',type=str)
    email = request.args.get('email',type=str)
    section = request.args.get('section',type=str)
    year = request.args.get('year',type=int)
    print(name,email,section,year)
    students.update_many(
        {"_id":session["regid"]},
        {"$set":{"name":name,"email":email,"section":section,"year":year}}
    )
    return jsonify(result = "Updated...")

@app.route("/")
def canteen():
    if "regid" in session:
        student = students.find_one({"_id":session["regid"]})
        return render_template("canteen.html",student = json.dumps(student))
    else:
        return redirect(url_for('studentlogin'))

@app.route("/send-products")
def send_products():
    available_products = []
    def send_products_sse(available_products):
        items = ["tiffen","fastfood","juice","snacks"]
        for item in items:
            var = products.find({item+".available":{"$gt" : 0}})
            print(var)
            for each in var:
                print(each)
                for i in each[item]:
                    print(i)
                    available_products.append(i)
        available_products = json.dumps(available_products)
        print(available_products)
        yield f"data:{available_products}\n\n\n\n"
        time.sleep(10)
    return Response(send_products_sse(available_products), mimetype="text/event-stream")

@app.route("/studentorders")
def studentorders():
    order = request.args.get('cart',type=str)
    order = json.loads(order)
    N=5
    list_1 = []
    list_2 = []
    total_cost_c1 = 0
    total_cost_c2 = 0
    for i in order:
        if(i["canteen_id"] == "canteen_1"):
            list_1.append(i)
            total_cost_c1 +=i["total cost"]
        else:
            list_2.append(i)
            total_cost_c2 +=i["total cost"]

    oid1 = ''.join(secrets.choice(string.ascii_uppercase + string.digits)for i in range(N))
    oid2= ''.join(secrets.choice(string.ascii_uppercase + string.digits)for i in range(N))
    order_id_1 = str(session["regid"])+oid1
    order_id_2 = str(session["regid"])+oid2

    canteen_1 = {
        "status":False,
        "regid":session["regid"],
        "canteen_id":"canteen_1",
        "orderid":order_id_1,
        "level":0,
        "otp":None,
        "payment":False,
        "total products":len(order)-1,
        "total cost":total_cost_c1
    }
    canteen_2 = {
        "status":False,
        "regid":session["regid"],
        "canteen_id":"canteen_2",
        "orderid":order_id_2,
        "level":0,
        "otp":None,
        "payment":False,
        "total products":len(order)-1,
        "total cost":total_cost_c2
    }
    canteen_1 = [canteen_1,list_1]
    canteen_2 = [canteen_2,list_2]

    if (len(list_1) > 0):
        student_orders.update(
            {"_id":session["regid"]},
            {
                "$set":{order_id_1:canteen_1}
            }
        )
        owner_orders.update({"_id":"canteen_1"},
        {
            "$set":{order_id_1:canteen_1}
        }
        )
    if (len(list_2) > 0):
        student_orders.update(
            {"_id":session["regid"]},
            {
                "$set":{order_id_2:canteen_2}
            }
        )
        owner_orders.update({"_id":"canteen_2"},
        {
            "$set":{order_id_2:canteen_2}
        }
        )
    return jsonify(result=1)

@app.route("/vieworders")
def vieworders():
    def vieworders_sse(id):
        order = student_orders.find_one({"_id":id})
        order = json.dumps(order)
        yield f"data:{order}\n\n\n\n"
    return Response(vieworders_sse(session["regid"]), mimetype="text/event-stream")

@app.route("/canceloneorder")
def canceloneorder():
    orderid = request.args.get("orderid",type=str)
    product_id = request.args.get("product_id",type=str)
    canteen_id = request.args.get("canteen_id",type=str)
    price = request.args.get("price",type=int)

    student_orders.update({"_id":session["regid"]},
    {"$pull":{orderid+".1":{'product_id':product_id}}}
    )
    student_orders.update({"_id":session["regid"]},
    {"$inc":{orderid+".0.total cost":-price}}
    )
    owner_orders.update({"_id":canteen_id},
    {"$pull":{orderid+".1":{'product_id':product_id}}}
    )
    owner_orders.update({"_id":canteen_id},
    {"$inc":{orderid+".0.total cost":-price}}
    )
    len_ = student_orders.find_one({"_id":session["regid"]},{orderid:True})
    
    if (len(len_[orderid][1])==0):
        student_orders.update({"_id":session["regid"]},{
            "$unset":{orderid:True}
        })
        owner_orders.update({"_id":canteen_id},{
            "$unset":{orderid:True}
        })
    return jsonify(result = 1)

@app.route("/cancelorder")
def cancelorder():
    orderid = request.args.get("orderid",type=str)
    canteen_id = request.args.get("canteen_id",type=str)
    student_orders.update({"_id":session["regid"]},
    {"$unset":{orderid:True}}
    )
    owner_orders.update({"_id":canteen_id},
        {"$unset":{orderid:True}}
    )
    return jsonify(result = 1)

if __name__ == "__main__":
    app.run(debug=True,port=5000)