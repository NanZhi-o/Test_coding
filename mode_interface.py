from flask import Flask, request, jsonify
import pymysql

app = Flask(__name__)

def get_conn():
    return pymysql.connect(host='localhost',user='root',password='123456',database='test_study', charset='utf8')

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    conn = get_conn()
    cursor = conn.cursor()
    sql = "SELECT * FROM users WHERE username=%s AND password=%s"
    cursor.execute(sql, (data['username'], data['password']))
    user = cursor.fetchone()
    conn.close()
    if data["username"] == "admin" and data["password"] == "123456":
        return jsonify({"code": 200, "msg": "Login success", "username": user[1]})
    return jsonify({"code": 401, "msg": "Login failed"})

if __name__ == '__main__':
    app.run(debug=True)
