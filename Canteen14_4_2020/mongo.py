import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId
from pprint import pprint
import re,json
import datetime
from datetime import datetime,timezone
client = pymongo.MongoClient("localhost",27017)
db = client["canteensystem"]

sorder = db["student orders"]
oorder = db["owner orders"]


client = pymongo.MongoClient("	")
# print(client.get_database('canteensystem'))

db = client["canteensystem"]
owners = db["owners"]
print(owners.find_one())
owners = db["owners"]	
print(client.list_database_names())



# json={
#     "name":"hell",
#     "id":1
# }

# id = collection.insert_one(json)

# print(id.inserted_id)
# print(db.list_collection_names())
# # print(collection.find({},{"name":"hell"}))
# x = collection.find_one({"_id":ObjectId("5e999b3d0a87757b216649ac")})
# for i in x:
#     print(x[i])
# print(collection.find().count())
#
# x = collection.find_one({"_id":9842598260})
# print(x)

#         var products = '<div class="row">';
	# for (var i in addtocart){
	#   i = Number(i);
	#   if (cache.includes(i) == true){
	#     continue;
	#   }
	#  else{
	#     products += '<div class="column" ><div class="card"><div class="card-body" style="color:red"><h5 class="card-title"> '+addtocart[i]["item"]+' It"s not available</h5></div></div></div>'
	#     delete addtocart[i];
	#   }
	# }
	# products +='</div>'
	# $/('#cartviewid').append(products);for i in collection.find():
#     print(i['_id'])


# _id = owners.find_one({"_id":9842598260})
# print(_id)
# print(_id["_id"])
# print(owners.count())
# owners.update_one({"_id":1,"name.age":10},{"$set":{"age":5}})
# owners.update_one({'_id':1},{"$set":{"name.3.age":100}})
# owners.insert_one({"name.1":1 })

# a = [[{"id":"a"},1,2,3],[4,5,6],[7,8,9]]
# owners.update_one({"_id":5},{"$set":{"a":a}})

# a = [1,2,34,4]
# for i in owners.find():
#     pprint(i)
# b = []
# a.append(b)
# print(a)
# a = owners.find_one({"_id":1},{"name":True})["name"][3]["age"]
# print(a)

# owners.update_one({"_id":1},{"$push":{"name":{"$each":a}}})
# re_=""
# for i in :
#     pprint(type(i))
#     re +=str(i)
# print(re_)
# re.match(re_, "^canteen")

# for i in owners.find({"_id":9842598260,"juice.product_id":}):
#     pprint(i)
# x = owners.find_one({"_id":9842598260})

# for i in owners.find({"tiffen.id":9842598260}):
#     print(i)
# print("******************************************")
# owners.find_and_modify(
#     {"query":{"tiffen.product_id":"canteen_1tiffen1"}},
#     {"update":{"$set":{"$tiffen.0.item":"bread"}}}
# )
# for i in owners.find({"tiffen.id":9842598260}):
#     print(i)
# json_ = {
# "name":5,
# {
#     1:2,3:4
# },{
#     5:6
# }
# }
# example.insert(json_)


# for i in example.find():
#     pprint(i)

# # example.update({"_id":9842598260},{"$pop":{"snacks":{'product_id': 'canteen_1snacks2'}}})
# x = example.find_one(
#     {
#         "snacks":{
#             "$eleMatch":{"product_id":"canteen_1snacks2"}
#             }
#     }
#     ,
#     {
#         "snacks.product_id":1
#     }
# )
# x = example.update({
#     "_id":9842598260},
#     {
#         "$set":{
#             "inc.snacks":0
#         }
#     }
# )

# print(x)

# juicecheck = {
# "p1":{
# "name":1
# },
# "p2":{
# "name":2
# },
# "p3":{
# "name":3
# },
# "p4":{
# "name":4
# }
# }

# example.update({"_id":9842598260},
# {
#     "$set":{ "juicecheck":juicecheck }
# }
# )
# example.update({"_id":9842598260},{
# "$pull  ":{
#     "juicecheck":{
#         "$eleMatch":{}
#     }
# }
# }
# )
# example.update({"_id":9842598260},
# {
#     "$set":{
#         "juice":{'product_id': 'canteen_1juice1'}
#     }
# }
# )
# example.update({
# "_id":9842598260,
# "fastfood.product_id":"canteen_1fastfood1"
# },
# {
#     "$set":{
#         "fastfood.$.available":0
#     }
# }
# )
# for i in example.find():
#     pprint(i)
#//////////////////////////////////////////////////////////
# example.update(
# {
#     "_id":9842598260 ,
# },
# {
#     "$pull":{
#         "fastfood":{"product_id": "canteen_1fastfood1"}
#         }
# }
# )
# example.update(
# {
#     "_id":9842598260 ,
# },
# {
#     "$pull":{"product_id": "canteen_1tiffen1"}
# }
# )
# for i in example.find():
#     pprint(i)
# print(example.find().count())

# x = example.find(
# { "$or": [ { "tiffen.available": { "$gt": 0 } }, { "juice.available": { "$gt": 0 } },{ "snacks.available": { "$gt": 0 } },{ "fastfood.available": { "$gt": 0 } } ] },
# {
#    {"$or":[{"tiffen.$":1},{"juice.$":1},{"fastfood.$":1},{"snacks.$":1}]}
# }
# )
# print(x)
# for i in x:
#     pprint(i)
# l = []
# x = l.append(example.find({"tiffen.available":{"$gt" : 0}},{"tiffen.$":1}))
# y = l.append(example.find({"tiffen.available":{"$gt" : 0}},{"tiffen.$":1}))

# for i in l:
#     for j in i:
#         # for k in j["tiffen"]:
#         pprint(j)

# available_products = []
# items = ["tiffen","fastfood","juice","snacks"]
# for item in items:
#     var = example.find({item+".available":{"$gt" : 0}},{item+".$":1})
#     for each in var:
#         for i in each[item]:
#             available_products.append(i)
# for i in available_products:
#     pprint(i)
# json = {
#   "_id": 611216104042,
# }
# array_ =[{   
#             "id":611216104042,
#             "otp":False,
#             "payment":False,
#             "status":0
#         }]

# example.update(
#     {"_id":611216104042},
#     {
#         "$push":{"order_id" : "array_"}
#     }
# )


# print(example.count({"_id":"611216104042","name":"jeeva","email": "jevvjeeva@gmail.com"}))
# x = example.find_one({"_id":611216104042},{})
# print(x)

# js = {
#         "name":"jeeva"
# }
# pprint(js)
# js["age"] = 22
# pprint(js)

# example.insert({"_id": "canteen_1"})
# example.insert({"_id": "canteen_2"})
# print(datetime.datetime.utcnow())
# now = datetime.now()
# print(datetime.timestamp(now))

# j = {
#         "_id":9,
#         "ts":datetime.timestamp(now)
# }
# example.insert(j)

# for i in sorder.find():
# 	pprint(i)
# for i in oorder.find():
# 	pprint(i)

# for i in example.find().sort("$.0.ts",-1):
#     pprint(i)

# example.update({"_id":611216104042},
# {
# 	"$pull":{
# 		'611216104042GV9UJ':1
# 		}
# }
# # )
# example.update({"_id":611216104042},
# {"$pull":{'611216104042GV9UJ.1':{'product_id':'canteen_2snacks1'}}}
# )
# for i in example.find().sort("$.ts",-1):
# 	pprint(i)
# pprint(example.find_one({"_id":611216104042}))
# x= example.find_one({"_id":611216104042},{"611216104042KU0VX":True})
# pprint(x["611216104042KU0VX"])
# sorder.update({"_id":611216104042},{
# "$unset":{'611216104042KU0VX':True}
# })
# oorder.update({"_id":"canteen_1"},{
# "$unset":{'611216104042KU0VX':True}
# })
# for i in sorder.find():
# 	pprint(i)
# for i in oorder.find():
# 	pprint(i)
# print(oorder.update({"_id":"canteen_2"},
# {"$inc":{"6112161040418E02U.0.total cost":-10}}
# ))
# for i in oorder.find():
# 	pprint(i)


# n = 6

# for i in range(1,n):