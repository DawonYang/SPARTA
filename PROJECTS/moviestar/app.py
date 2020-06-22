from pymongo import MongoClient

from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.dbsparta


# HTML을 주는 부분
@app.route('/')
def home():
    return render_template('index.html')

# API 역할을 하는 부분
@app.route('/api/list', methods=['GET'])
def stars_list():
    stars = list(db.mystar.find({},{'_id':0}).sort('like', -1))
    # 1. mystar 목록 전체를 검색합니다. ID는 제외하고 like 가 많은 순으로 정렬합니다.
    # 참고) find({},{'_id':False}), sort()를 활용하면 굿!
    # 2. 성공하면 success 메시지와 함께 stars_list 목록을 클라이언트에 전달합니다.
    return jsonify({'result': 'success','all_star': stars})


@app.route('/api/like', methods=['POST'])
def star_like():
    name_receive = request.form['name_give']

    like = db.mystar.find_one({'name':name_receive},{'_id':0})['like']
    new_like = like +1

    db.mystar.update_one({'name':name_receive},{'$set':{'like':new_like}})

    return jsonify({'result': 'success','msg':'완료되었습니다 :)'})
    # 1. 클라이언트가 전달한 name_give를 name_receive 변수에 넣습니다.
    # 2. mystar 목록에서 find_one으로 name이 name_receive와 일치하는 star를 찾습니다.
    # 3. star의 like 에 1을 더해준 new_like 변수를 만듭니다.
    # 4. mystar 목록에서 name이 name_receive인 문서의 like 를 new_like로 변경합니다.
    # 참고: '$set' 활용하기!
    # 5. 성공하면 success 메시지를 반환합니다.
    


@app.route('/api/delete', methods=['POST'])
def star_delete():

    name_receive = request.form['name_give']

    db.mystar.delete_one({'name':name_receive})
        
    return jsonify({'result': 'success','msg':'삭제가 완료되었습니다 :)'})
    # 1. 클라이언트가 전달한 name_give를 name_receive 변수에 넣습니다.
    # 2. mystar 목록에서 delete_one으로 name이 name_receive와 일치하는 star를 제거합니다.
    # 3. 성공하면 success 메시지를 반환합니다.
	


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)