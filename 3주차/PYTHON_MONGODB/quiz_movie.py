
from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbsparta 

target = db.movies.find_one({'title':'매트릭스'})
target_star = target['star']

db.movies.update_many({'star':target_star},{'$set':{'star':0}})



